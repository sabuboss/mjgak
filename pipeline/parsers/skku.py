"""성균관대학교 파서.

입력: 수시 학생부종합전형 면접시험 기출문항 PDF (3~4쪽, 모집단위별 "□ <모집단위> (2단계) (일시)" 섹션).
  각 섹션: "» 면접시험 (공통문항)" → 제시문 (가)~(다) → "물음 1> …", "물음 2> …" (+ <보기>).
  PDF 텍스트 추출 시 문장부호가 뒤섞이므로(폰트 문제) 규칙 기반 레코드는 '대략'이며 --llm 으로 정리해야 한다.
"""
from __future__ import annotations

import re
from pathlib import Path

from mjgak_pipeline.models import QuestionRecord
from parsers.snu import Block, Line

import pymupdf

NOISE = (
    re.compile(r"이 문서는 상업적인 목적으로"),
    re.compile(r"^\d+\s*$"),
)
# "□ 자유전공계열 (2단계) (…)" 또는 과학인재 "[ 1번 - 수학 ] (답변시간 3분)"
UNIT_RE = re.compile(r"^(?:□\s*(?P<unit>.+?)\s*(\(\d ?단계\).*)?|\[\s*(?P<num>\d+)번\s*-\s*(?P<subj>[가-힣 ]+?)\s*\].*)$")
# "물음 1> …", "질문) …", "[문제 1] …", "[1-ⅰ] …"
Q_RE = re.compile(r"^(?:물음\s*(\d+)>|질문\s*(\d*)\)|\[문제\s*(\d+)\]|\[(\d+-[ⅰⅱⅲⅳⅴ]+)\])\s*(.*)$")
PASSAGE_RE = re.compile(r"^\(\s*[가-힣]\s*\)")


def _lines(pdf_path: Path) -> list[Line]:
    out: list[Line] = []
    with pymupdf.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            for raw in page.get_text("text", sort=True).splitlines():
                t = re.sub(r"\s+", " ", raw).strip()
                if not t or any(r.search(t) for r in NOISE):
                    continue
                out.append(Line(i, t))
    return out


def segment(pdf_path: Path, meta: dict) -> list[Block]:
    blocks: list[Block] = []
    cur: Block | None = None
    for ln in _lines(pdf_path):
        m = UNIT_RE.match(ln.text)
        if m:
            unit = (m.group("unit") or "").strip() or f"과학인재전형 {m.group('num')}번 ({m.group('subj').strip()})"
            cur = Block(field=unit, subtype="", page=ln.page)
            blocks.append(cur)
            continue
        if cur is not None:
            cur.lines.append(ln)
    return blocks


def parse(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    recs: list[QuestionRecord] = []
    for b in segment(pdf_path, meta):
        passage: list[str] = []
        qs: list[tuple[str, str]] = []
        for l in b.lines:
            m = Q_RE.match(l.text)
            if m:
                num = m.group(1) or m.group(2) or m.group(3) or m.group(4) or str(len(qs) + 1)
                qs.append((num, m.group(5)))
            elif qs and not l.text.startswith("<") and len(l.text) < 120 and not PASSAGE_RE.match(l.text):
                qs[-1] = (qs[-1][0], (qs[-1][1] + " " + l.text).strip())
            else:
                passage.append(l.text)
        for num, q in qs:
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name=re.sub(r"\s*\(.*$", "", meta.get("title", "학생부종합전형 면접")),
                category=meta.get("category", "student_record"),
                unit=b.field,
                year=meta["year"],
                kind="actual",
                text=f"[물음 {num}] {q}",
                presented_material="\n".join(passage),
                source_url=meta.get("page_url") or meta["url"],
                source_page=b.page,
            ))
    return recs
