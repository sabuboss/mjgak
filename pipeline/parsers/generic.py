"""대교협 표준 '문항카드' 형식 범용 파서 (고려대 파서를 일반화).

대부분의 대학 선행학습 영향평가 보고서는 부록에 아래 형식의 문항카드를 싣는다.
  [○○대학교 문항정보] / 문항 정보
  1. 일반 정보  (유형 □논술고사 ■면접 및 구술고사 □선다형고사 / 전형명 / 계열·문항번호 / 교육과정 과목명 / 핵심개념 / 예상 소요 시간)
  2. 문항 및 제시문
  3. 출제 의도 / 4. 출제 근거 / 5. 문항 해설 / 6. 채점 기준 / 7. 예시 답안
카드 시작 표식과 섹션 제목의 변형(번호 유무, 띄어쓰기)을 허용한다. 면접 및 구술고사 카드만 레코드로 만든다.
"""
from __future__ import annotations

import re
from pathlib import Path

import pymupdf

from mjgak_pipeline.models import QuestionRecord
from parsers.snu import Block, Line

PARSES_REPORTS = True

CARD_START_RE = re.compile(
    r"^\s*\[?\s*(?:[가-힣A-Za-z()·\s]{2,24})?문항\s*정보\s*\]?\s*$"  # [○○대학교 문항정보] / 경희대학교 문항정보
    r"|^\s*(?:\d{1,2}[.)]\s*)?문항\s*카드\s*(?:\d+|[①-⑳]|\(\d+\))?(?:\s*[–\-]\s*.{0,40})?\s*$"  # 문항카드 / 1. 문항카드 1 – 인문계열 1차 1번
)
SECTION_RE = re.compile(r"^\s*(?:\d\s*[.)]\s*|[①-⑨]\s*)?(일반\s*정보|문항\s*및\s*제시문|문항\s*(?:및|과)?\s*제시문|제시문\s*및\s*문항|출제\s*의도|출제\s*근거|문항\s*해설|채점\s*기준|예시\s*답안|모범\s*답안|자료\s*출처)\s*$")
Q_RE = re.compile(r"^\s{0,4}(?:\[?문[제항]\s*(\d{1,2}(?:[-–]\d)?)\]?[.)]?\s*|(\d{1,2})[.)]\s+)(.{6,})$")
PASSAGE_RE = re.compile(r"^\s*(?:\(([가-힣])\)|\[([가-힣])\]|제시문\s*\(?([가-힣0-9])\)?)\s*")
NOISE = (re.compile(r"^\s*-\s*\d+\s*-\s*$"), re.compile(r"^\s*\d+\s*$"))
INTERVIEW_RE = re.compile(r"[■▣☑✔●]\s*면접|면접\s*(?:및|·)\s*구술\s*고사\s*[■▣☑✔●]|\[■\]\s*면접")


def norm(s: str) -> str:
    return re.sub(r"\s", "", s)


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
    blocks: list[Block] = []
    cur: Block | None = None
    for ln in _lines(pdf_path):
        if CARD_START_RE.match(ln.text):
            cur = Block(field="", subtype="", page=ln.page)
            blocks.append(cur)
            continue
        if cur is not None:
            cur.lines.append(ln)
    return blocks


def _sections(block: Block) -> dict[str, list[str]]:
    sec: dict[str, list[str]] = {"head": []}
    key = "head"
    for ln in block.lines:
        m = SECTION_RE.match(ln.text)
        if m:
            k = norm(m.group(1))
            key = {"문항제시문": "문항및제시문", "문항과제시문": "문항및제시문", "제시문및문항": "문항및제시문", "모범답안": "예시답안"}.get(k, k)
            sec.setdefault(key, [])
            continue
        sec.setdefault(key, []).append(ln.text)
    return sec


def _info(lines: list[str]) -> dict[str, str]:
    info: dict[str, str] = {}
    joined = "\n".join(lines)
    for label in ("전형명", "교육과정 과목명", "핵심개념 및 용어", "예상 소요 시간", "핵심 개념"):
        m = re.search(rf"{label}\s*[:：]?\s*(.+)", joined)
        if m:
            info[label] = m.group(1).strip()
    m2 = re.search(r"([가-힣A-Z]+계열\([^)]*\)|[가-힣A-Z·]+계열|[가-힣]+대학\([^)]*\)|[가-힣]+(?:학과|학부)(?:\([^)]*\))?)\s*/\s*([\d\-~, ]+번)", joined)
    if m2:
        info["계열"] = m2.group(1).strip()
        info["문항번호"] = m2.group(2).strip()
    return info


def _body(lines: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    qs: list[tuple[str, str]] = []
    passage: list[str] = []
    i = 0
    while i < len(lines):
        t = lines[i]
        m = Q_RE.match(t)
        if m:
            num = (m.group(1) or m.group(2)).replace("–", "-")
            txt = m.group(3).strip()
            i += 1
            while i < len(lines) and not Q_RE.match(lines[i]) and not PASSAGE_RE.match(lines[i]) and not re.search(r"(시오|보시오|하라|나요|까요|\?)\s*$", txt):
                txt += " " + lines[i].strip()
                i += 1
            qs.append((num, txt))
            continue
        passage.append(t.strip())
        i += 1
    return qs, passage


def _intent_for(num: str, intent: list[str]) -> str:
    joined = "\n".join(l.strip() for l in intent)
    parts = re.split(r"(?=(?:§|○|◦|-|•)\s*)", joined)
    base = num.split("-")[0]
    hit = [p.strip("§○◦-• \n") for p in parts if re.search(rf"^\S?\s*(?:\[?문[제항]\s*)?{base}\s*번", p)]
    general = [p.strip("§○◦-• \n") for p in parts if p.strip() and not re.search(r"^\S?\s*(?:\[?문[제항]\s*)?\d+\s*번", p)]
    return "\n".join((general[:1] + hit))[:800]


def _is_interview(head_lines: list[str]) -> bool:
    """'유형 ■ 논술고사 □ 면접 및 구술고사 □ 선다형고사' 줄에서 면접 칸이 채워져 있는지 본다.
    유형 줄이 없으면 전형명에 '면접/구술'이 있고 '논술'이 없을 때만 면접으로 본다."""
    for l in head_lines:
        t = re.sub(r"\s+", " ", l)
        if re.search(r"유\s*형\s*[:：]?\s*[□■▣☑✔●]", t):
            return bool(re.search(r"[■▣☑✔●]\s*면접", t))
    joined = "\n".join(head_lines)
    m = re.search(r"전형명\s*[:：]?\s*(.+)", joined)
    adm = m.group(1) if m else ""
    return ("면접" in adm or "구술" in adm) and "논술" not in adm


def parse_cards(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    recs: list[QuestionRecord] = []
    for b in segment(pdf_path, meta):
        sec = _sections(b)
        head_lines = sec.get("일반정보", []) + sec.get("head", [])
        if not _is_interview(head_lines):
            continue
        info = _info((sec.get("일반정보", []) + sec.get("head", [])))
        qs, passage = _body(sec.get("문항및제시문", []))
        if not qs and not passage:
            continue
        adm = info.get("전형명", "면접 및 구술고사")
        unit = info.get("계열", "")
        rubric = "\n".join(l.strip() for l in sec.get("채점기준", [])[:40])[:1500]
        hint = "\n".join(l.strip() for l in (sec.get("문항해설", []) or sec.get("예시답안", []))[:60])[:2000]
        subjects = info.get("교육과정 과목명", "")
        if subjects:
            rubric = f"교육과정 근거: {subjects}\n" + rubric
        cat = "mmi" if re.search(r"인[·・]?적성|인성", adm) else "essay_based"
        for num, q in qs or [("1", " ".join(passage[:2])[:400])]:
            if len(q.strip()) < 6:
                continue
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name=adm[:60],
                category=cat,
                unit=unit[:120],
                year=meta["year"],
                kind="actual",
                text=f"[문항 {num}] {q}"[:1500],
                presented_material="\n".join(passage)[:6000],
                intent=_intent_for(num, sec.get("출제의도", [])),
                rubric=rubric,
                model_answer_hint=hint,
                source_url=meta.get("url") or meta.get("page_url"),
                source_page=b.page,
            ))
    return recs


def parse(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    return parse_cards(pdf_path, meta)
