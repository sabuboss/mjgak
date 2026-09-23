"""고려대학교 파서.

입력: 선행학습 영향평가 자체평가보고서 (kind=report). 부록에 대교협 표준 '문항카드'가 들어 있다.
  카드 시작: "[고려대학교 문항정보]"
  1. 일반 정보 (유형 ■ 면접 및 구술고사 / 전형명 / 계열(과목)·문항번호 / 교육과정 과목명 / 핵심개념 / 예상 소요 시간)
  2. 문항 및 제시문  ((가)(나)… 제시문 뒤에 " 1. …", " 2. …" 번호 문항)
  3. 출제 의도 / 4. 출제 근거 / 5. 문항 해설 / 6. 채점 기준 …
논술고사 카드는 제외하고 면접 및 구술고사 카드만 레코드로 만든다.
이 카드 형식은 다른 대학도 많이 쓰므로 `parse_cards()` 는 재사용 가능하게 두었다.
"""
from __future__ import annotations

import re
from pathlib import Path

import pymupdf

from mjgak_pipeline.models import QuestionRecord
from parsers.snu import Block, Line

PARSES_REPORTS = True  # 보고서 부록의 문항카드를 파싱한다
CARD_START = "[고려대학교 문항정보]"
SECTION_RE = re.compile(r"^\s*(\d)\.\s+(일반 ?정보|문항 및 제시문|출제 ?의도|출제 ?근거|문항 ?해설|채점 ?기준|예시 ?답안|자료 ?출처|교육과정[가-힣 ]*)\s*$")
Q_RE = re.compile(r"^\s{0,4}(\d{1,2})\.\s+(.+)$")
PASSAGE_RE = re.compile(r"^\s*\(([가-힣])\)\s*")
NOISE = (re.compile(r"^\s*- \d+ -\s*$"),)


def _lines(pdf_path: Path) -> list[Line]:
    out: list[Line] = []
    with pymupdf.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            for raw in page.get_text("text", sort=True).splitlines():
                if not raw.strip() or any(r.match(raw) for r in NOISE):
                    continue
                out.append(Line(i, raw.rstrip()))
    return out


def segment(pdf_path: Path, meta: dict) -> list[Block]:
    """문항카드 단위 블록. field 에는 전형명/계열 요약을 넣는다."""
    blocks: list[Block] = []
    cur: Block | None = None
    for ln in _lines(pdf_path):
        if ln.text.strip() == CARD_START:
            cur = Block(field="", subtype="", page=ln.page)
            blocks.append(cur)
            continue
        if cur is not None:
            cur.lines.append(ln)
    return blocks


def _sections(block: Block) -> dict[str, list[str]]:
    sec: dict[str, list[str]] = {}
    key = "head"
    for ln in block.lines:
        m = SECTION_RE.match(ln.text)
        if m:
            key = re.sub(r"\s", "", m.group(2))
            sec.setdefault(key, [])
            continue
        sec.setdefault(key, []).append(ln.text)
    return sec


def _info(lines: list[str]) -> dict[str, str]:
    """'1. 일반 정보' 표에서 라벨 → 값 (같은 줄에 라벨과 값이 있는 단순 케이스만)."""
    info: dict[str, str] = {}
    joined = "\n".join(lines)
    for label in ("유형", "전형명", "교육과정 과목명", "핵심개념 및 용어", "예상 소요 시간"):
        m = re.search(rf"{label}\s+(.+)", joined)
        if m:
            info[label] = m.group(1).strip()
    m = re.search(r"문항번호|해당 대학의 계열", joined)
    # 계열/문항번호 줄: '인문계열(오전) / 1-3번' 형태
    m2 = re.search(r"([가-힣]+계열\([^)]*\)|[가-힣]+계열|의과대학[^\n]*)\s*/\s*([\d\-~, ]+번)", joined)
    if m2:
        info["계열"] = m2.group(1).strip()
        info["문항번호"] = m2.group(2).strip()
    return info


def _body(lines: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    qs: list[tuple[str, str]] = []
    passage: list[str] = []
    seen_passage = False
    i = 0
    while i < len(lines):
        t = lines[i]
        if PASSAGE_RE.match(t):
            seen_passage = True
        m = Q_RE.match(t)
        # 제시문이 나온 뒤의 번호 줄만 문항으로 본다 (제시문 안의 '1.' 나열과 구분)
        if m and seen_passage and len(m.group(2)) > 8:
            num, txt = m.group(1), m.group(2).strip()
            i += 1
            while i < len(lines) and not Q_RE.match(lines[i]) and not PASSAGE_RE.match(lines[i]) and not re.search(r"(시오|보시오|하라|\?)\s*$", txt):
                txt += " " + lines[i].strip()
                i += 1
            qs.append((num, txt))
            continue
        passage.append(t.strip())
        i += 1
    return qs, passage


def _intent_for(num: str, intent: list[str]) -> str:
    joined = "\n".join(l.strip() for l in intent)
    parts = re.split(r"(?=§)", joined)
    hit = [p.strip("§ \n") for p in parts if re.match(rf"§\s*{num}번", p)]
    general = [p.strip("§ \n") for p in parts if p.strip() and not re.match(r"§\s*\d+번", p)]
    return "\n".join(general[:1] + hit)


def parse_cards(pdf_path: Path, meta: dict, card_start: str = CARD_START) -> list[QuestionRecord]:
    recs: list[QuestionRecord] = []
    for b in segment(pdf_path, meta):
        sec = _sections(b)
        info = _info(sec.get("일반정보", []) + sec.get("head", []))
        if "■ 면접" not in info.get("유형", "") and "■ 면접" not in "\n".join(sec.get("일반정보", [])):
            continue  # 논술·선다형 카드 제외
        qs, passage = _body(sec.get("문항및제시문", []))
        adm = info.get("전형명", "면접 및 구술고사")
        unit = info.get("계열", "")
        rubric = "\n".join(l.strip() for l in sec.get("채점기준", [])[:40])
        hint = "\n".join(l.strip() for l in sec.get("문항해설", [])[:60])
        subjects = info.get("교육과정 과목명", "")
        if subjects:
            rubric = f"교육과정 근거: {subjects}\n" + rubric
        cat = "mmi" if "인·적성" in adm or "인적성" in adm else "essay_based"
        for num, q in qs or [("1", " ".join(passage[:2]))]:
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name=adm,
                category=cat,
                unit=unit,
                year=meta["year"],
                kind="actual",
                text=f"[문항 {num}] {q}",
                presented_material="\n".join(passage),
                intent=_intent_for(num, sec.get("출제의도", [])),
                rubric=rubric,
                model_answer_hint=hint,
                source_url=meta.get("page_url") or meta["url"],
                source_page=b.page,
            ))
    return recs


def parse(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    return parse_cards(pdf_path, meta)
