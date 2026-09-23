"""연세대학교(서울) 파서.

입력: 선행학습 영향평가 결과보고서 [별책] 대학별고사 기출문제 (kind=questions).
  별책은 논술 + 면접구술(학종 활동우수형/국제형, 특기자, 정시 의예과·국제계열, 재외국민) 순.
  면접 페이지는 "YYYY학년도 연세대학교 면접구술시험" 머리글 + 다음 줄에 전형[유형] 계열.
  제시문 [가][나][다][라] (또는 (가)…), 문제는 "<문제 N>" 또는 "[문제 N-M]".
  논술 페이지("논술시험")는 건너뛴다 — 면접 앱이므로.

본 보고서(kind=report) 는 출제의도·문항해설이 있지만 문항과 페이지 매칭이 필요해 LLM 단계에서 다룬다.
"""
from __future__ import annotations

import re
from pathlib import Path

from mjgak_pipeline.extract import extract_pages
from mjgak_pipeline.models import QuestionRecord
from parsers.snu import Block, Line

HEADER_RE = re.compile(r"^\d{4}학년도 연세대학교 (?P<exam>.+?시험)\s*$")
NOISE = (
    re.compile(r"^전체 \d+쪽 중 \d+쪽"),
    re.compile(r"^\d+쪽 중 \d+쪽"),
    re.compile(r"^- \d+ -$"),
)
PASSAGE_RE = re.compile(r"^(제시문 )?(\[[가-힣]\]|\([가-힣]\)|\[지문 [A-Z]\])\s*")
Q_RE = re.compile(r"^(?:<문제 (\d+(?:-\d+)?)>|\[문제 (\d+(?:-\d+)?)(?:,[^\]]*)?\]|문제 (\d+(?:-\d+)?)\.)\s*(.*)$")
Q_END_RE = re.compile(r"(시오|하라|하시오|\?|\.|\))\s*$")


def _blocks(pdf_path: Path) -> list[Block]:
    """면접 페이지들을 (전형·계열) 단위로 묶는다. 같은 전형 문구가 이어지는 연속 페이지는 한 블록."""
    blocks: list[Block] = []
    cur: Block | None = None
    for p in extract_pages(pdf_path):
        lines = [l.strip() for l in p.text.splitlines()]
        lines = [l for l in lines if l and not any(r.match(l) for r in NOISE)]
        if not lines:
            continue
        # "2024학년도 연세대학교" 와 "면접구술시험" 이 두 줄로 나뉜 페이지 처리
        if re.match(r"^\d{4}학년도 연세대학교$", lines[0]) and len(lines) > 1:
            lines = [lines[0] + " " + lines[1]] + lines[2:]
        m = HEADER_RE.match(lines[0])
        if m:
            exam = m.group("exam")
            if "면접" not in exam:
                cur = None  # 논술 등은 제외
                continue
            unit = lines[1] if len(lines) > 1 else ""
            body = lines[2:]
            if cur is None or cur.field != unit:
                cur = Block(field=unit, subtype=exam, page=p.page)
                blocks.append(cur)
        else:
            body = lines
            if cur is None:
                continue
        for l in body:
            cur.lines.append(Line(p.page, l))
    return blocks


def segment(pdf_path: Path, meta: dict) -> list[Block]:
    return _blocks(pdf_path)


def _split(block: Block) -> tuple[list[tuple[str, str]], list[str]]:
    qs: list[tuple[str, str]] = []
    passage: list[str] = []
    lines = [l.text for l in block.lines]
    i = 0
    while i < len(lines):
        m = Q_RE.match(lines[i])
        if m:
            num = (m.group(1) or m.group(2) or m.group(3)).replace("–", "-")
            txt = m.group(4)
            i += 1
            while i < len(lines) and not Q_RE.match(lines[i]) and not PASSAGE_RE.match(lines[i]) and not Q_END_RE.search(txt):
                txt += " " + lines[i]
                i += 1
            qs.append((num, txt.strip()))
            continue
        if lines[i].startswith("※"):
            i += 1
            continue
        passage.append(lines[i])
        i += 1
    return qs, passage


def _admission(unit: str) -> tuple[str, str]:
    """'학생부종합전형[활동우수형] 인문‧통합계열' → (전형명, category)."""
    if unit.startswith("재외국민") or unit.startswith("북한이탈"):
        return "재외국민/북한이탈주민전형 면접구술시험", "essay_based"
    if unit.startswith("정시"):
        return "정시모집 면접구술시험", "essay_based"
    if unit.startswith("특기자"):
        return "특기자전형 면접구술시험", "essay_based"
    return "학생부종합전형 면접구술시험", "essay_based"


def parse(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    recs: list[QuestionRecord] = []
    for b in _blocks(pdf_path):
        qs, passage = _split(b)
        adm, cat = _admission(b.field)
        if not qs:
            continue
        for num, q in qs:
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name=adm,
                category=cat,
                unit=b.field,
                year=meta["year"],
                kind="actual",
                text=f"[문제 {num}] {q}",
                presented_material="\n".join(passage),
                source_url=meta.get("page_url") or meta["url"],
                source_page=b.page,
            ))
    return recs
