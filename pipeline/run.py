"""면접각 파이프라인 CLI.

  python run.py fetch snu                          # PDF 수집 → raw/snu/{year}/
  python run.py parse snu [--year 2026] [--llm]    # 파싱 → out/snu.jsonl (+ out/snu_{year}_*.json)
  python run.py stats snu                          # out/snu.jsonl 요약

--llm 은 ANTHROPIC_API_KEY 가 있을 때만 동작. 없으면 규칙 기반 rough 레코드만 낸다.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mjgak_pipeline.fetch import ROOT, fetch_university, get_university, source_dest  # noqa: E402

OUT = ROOT / "pipeline" / "out"


def cmd_fetch(args):
    fetch_university(args.univ, args.year)


def cmd_parse(args):
    univ = get_university(args.univ)
    parser = importlib.import_module(f"parsers.{args.univ}")
    use_llm = args.llm
    if use_llm:
        from mjgak_pipeline import structure

        if not structure.has_api_key():
            print("[parse] ANTHROPIC_API_KEY 없음 → --llm 무시, 규칙 기반만 수행")
            use_llm = False
    all_recs = []
    for src in univ["sources"]:
        if args.year and src["year"] != args.year:
            continue
        if src["kind"] == "report":
            continue  # 보고서는 문항 원문이 없음(출제의도·검토의견). 별도 단계에서 활용.
        pdf = source_dest(args.univ, src)
        if not pdf.exists():
            print(f"[parse] 없음: {pdf.relative_to(ROOT)} (먼저 fetch)")
            continue
        meta = {**src, "university_code": args.univ}
        blocks = parser.segment(pdf, meta)
        recs = parser.parse(pdf, meta)
        if use_llm:
            from mjgak_pipeline import structure

            llm_recs = []
            for b in blocks:
                bmeta = {**meta, "source_page": b.page}
                rough = [r for r in recs if r.source_page == b.page]
                try:
                    llm_recs.extend(structure.structure_block(b.text, bmeta, field_hint=b.field, rough=rough))
                except Exception as e:  # noqa: BLE001
                    print(f"[parse] LLM 실패 p{b.page}: {e} → rough 사용")
                    llm_recs.extend(rough)
            recs = llm_recs
        mode = "llm" if use_llm else "rough"
        print(f"[parse] {pdf.name}: {len(blocks)} blocks → {len(recs)} records ({mode})")
        out_name = f"{args.univ}_{src['year']}_{pdf.stem.split('_', 2)[-1]}.json"
        (OUT / out_name).write_text(
            json.dumps([r.model_dump() for r in recs], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        all_recs.extend(recs)
    out = OUT / f"{args.univ}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in all_recs:
            f.write(json.dumps(r.model_dump(), ensure_ascii=False) + "\n")
    print(f"[parse] 총 {len(all_recs)} records → {out.relative_to(ROOT)}")


def cmd_stats(args):
    recs = [json.loads(l) for l in (OUT / f"{args.univ}.jsonl").read_text(encoding="utf-8").splitlines()]
    print("records:", len(recs))
    print("by year:", dict(sorted(Counter(r["year"] for r in recs).items())))
    print("by category:", dict(Counter(r["category"] for r in recs)))
    print("by kind:", dict(Counter(r["kind"] for r in recs)))
    print("missing source_url:", sum(1 for r in recs if not r["source_url"]))
    print("empty text:", sum(1 for r in recs if not r["text"].strip()))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("fetch", cmd_fetch), ("parse", cmd_parse), ("stats", cmd_stats)):
        p = sub.add_parser(name)
        p.add_argument("univ")
        p.add_argument("--year", type=int)
        p.add_argument("--llm", action="store_true")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
