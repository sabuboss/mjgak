"""서울대학교 파서.

입력 PDF 3종:
  - 수시 일반전형 면접 및 구술고사 문항 (kind=questions, category=essay_based)
      [계열] 헤더 → "※ 제시문을 읽고 문제에 답하시오." 로 시작하는 문항 블록 반복.
      블록 안: 제시문 (가)(나)(다)… / [문제 N] … / 활용 모집단위 / 문항해설 / 출제의도 / 교육과정 출제근거 / 자료출처
  - 적성·인성면접 문항 (kind=questions, category=mmi)
      [단과대학] 헤더 → 제시문 [1] [2] … → "1. 질문" 번호 목록
  - 예시 문항 (kind=examples) : 일반전형과 같은 구조, 헤더가 "분석적 주제토론 [인문학]" 식.

1차: 규칙 기반으로 블록을 자르고 대략의 레코드(rough)를 만든다. API 키 없이도 end-to-end 동작.
2차(--llm): 블록 텍스트를 LLM 에 넣어 문항 단위로 정확히 구조화한다 (mjgak_pipeline.structure).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from mjgak_pipeline.extract import extract_pages
from mjgak_pipeline.models import QuestionRecord

PAGE_NOISE = (
    re.compile(r"^총 \d+쪽 중 \d+쪽$"),
    re.compile(r"^이 문서는 상업적인 목적으로"),
    re.compile(r"^\d{4}학년도 .*(면접 및 구술고사|적성 ?· ?인성면접|예시 문항)\s*$"),
    re.compile(r"^서울대학교 입학본부$"),
    re.compile(r"^SNU 역량평가 면접 예시 문항$"),
)
FOOTER_STARTS = (
    "서울대학교 면접 및 구술고사는 고등학교 교육과정",
    "아닌 종합적인 사고력을 평가",
    "사이의 자유로운 상호작용",
    "작용을 통해 문제 해결 능력",
)
HEADING_RE = re.compile(r"^(?:(?P<sub>[가-힣 ]{2,20}) )?\[(?P<name>[가-힣A-Za-z0-9·\s()]{2,40})\]$")
# 계열명 화이트리스트 + 단과대학/대학원/학부/학과 로 끝나는 이름만 헤더로 인정 ([결과], [그림 1] 등 제외)
KNOWN_FIELDS = ("인문학", "사회과학", "수학", "물리학", "물리", "화학", "생명과학", "지구과학", "과학", "영어", "인문", "자연", "융합")
FIELD_SUFFIX = ("대학", "대학원", "학부", "학과", "전공", "과정")
BLOCK_START = "※ 제시문을 읽고"
SECTION_KEYS = ("모집단위", "문항해설", "출제의도", "교육과정", "자료출처")
# "[문제 1]" 또는 "문제 1." 또는 "1-1." / "1–1." (과학 소문항)
Q_RE = re.compile(r"^(?:\[문제 (\d+(?:[-–]\d+)?)\]|문제 (\d+(?:[-–]\d+)?)\.|(\d+[-–]\d+)\.)\s*(.*)$")
PASSAGE_RE = re.compile(r"^\((가|나|다|라|마|바|사)\)\s*")
Q_END_RE = re.compile(r"(시오|하라|하시오|\?|\.)\s*$")
MMI_Q_RE = re.compile(r"^(\d+)\.\s+(.+)$")


@dataclass
class Line:
    page: int
    text: str


@dataclass
class Block:
    field: str            # 인문학 / 수학 / 간호대학 …
    subtype: str          # 분석적 주제토론 등 (예시문항)
    page: int             # 시작 페이지
    lines: list[Line] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(l.text for l in self.lines)


def clean_lines(pdf_path: Path) -> list[Line]:
    out: list[Line] = []
    for p in extract_pages(pdf_path):
        for raw in p.text.splitlines():
            t = raw.strip()
            if not t or any(r.match(t) for r in PAGE_NOISE) or t.startswith(FOOTER_STARTS):
                continue
            out.append(Line(p.page, t))
    return out


def _heading(line: str) -> tuple[str, str] | None:
    m = HEADING_RE.match(line)
    if not m:
        return None
    name = m.group("name").strip()
    base = name.split("(")[0].strip()
    if not base.startswith(KNOWN_FIELDS) and not base.endswith(FIELD_SUFFIX):
        return None
    return name, (m.group("sub") or "").strip()


def segment_general(lines: list[Line]) -> list[Block]:
    """일반전형/예시문항: ※ 제시문 블록 단위."""
    blocks: list[Block] = []
    cur_field, cur_sub = "", ""
    cur: Block | None = None
    for ln in lines:
        h = _heading(ln.text)
        if h:
            cur_field, cur_sub = h
            cur = None
            continue
        if ln.text.startswith(BLOCK_START):
            cur = Block(cur_field, cur_sub, ln.page)
            blocks.append(cur)
            continue
        if cur is not None:
            cur.lines.append(ln)
    return blocks


def segment_mmi(lines: list[Line]) -> list[Block]:
    """적성·인성면접: [단과대학] 헤더 단위."""
    blocks: list[Block] = []
    cur: Block | None = None
    for ln in lines:
        h = _heading(ln.text)
        if h:
            cur = Block(h[0], h[1], ln.page)
            blocks.append(cur)
            continue
        if cur is not None:
            cur.lines.append(ln)
    return blocks


def _split_sections(block: Block) -> dict[str, list[str]]:
    """블록을 본문/모집단위/문항해설/출제의도/교육과정/자료출처 로 나눈다."""
    sec: dict[str, list[str]] = {"body": []}
    key = "body"
    for ln in block.lines:
        t = ln.text
        if t == "활용":
            continue
        if t in SECTION_KEYS:
            key = t
            sec.setdefault(key, [])
            continue
        if key == "교육과정" and t == "출제근거":
            continue
        sec.setdefault(key, []).append(t)
    return sec


def _body_split(body: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """본문에서 [문제 N] 들과 제시문을 분리. 문제 줄은 문장 종결(시오/?/.)까지 이어붙인다."""
    questions: list[tuple[str, str]] = []
    passage: list[str] = []
    i = 0
    while i < len(body):
        m = Q_RE.match(body[i])
        if m:
            num, txt = (m.group(1) or m.group(2) or m.group(3)).replace("–", "-"), m.group(4)
            i += 1
            while (i < len(body) and not Q_RE.match(body[i]) and not PASSAGE_RE.match(body[i])
                   and not Q_END_RE.search(txt)):
                txt += " " + body[i]
                i += 1
            questions.append((num, txt.strip()))
            continue
        passage.append(body[i])
        i += 1
    return questions, passage


def _intent_for(num: str, intent_lines: list[str]) -> str:
    """출제의도에서 [문제 N] 항목만 뽑는다. 없으면 전체."""
    joined = "\n".join(intent_lines)
    parts = re.split(r"(?=\[문제 \d+(?:-\d+)?\])", joined)
    for p in parts:
        if p.startswith(f"[문제 {num}]"):
            return p.strip()
    return joined.strip()


def rough_records_general(blocks: list[Block], meta: dict) -> list[QuestionRecord]:
    kind = "example" if meta.get("kind") == "examples" else "actual"
    recs: list[QuestionRecord] = []
    for b in blocks:
        sec = _split_sections(b)
        questions, passage = _body_split(sec["body"])
        unit = " ".join(sec.get("모집단위", []))
        hint = "\n".join(sec.get("문항해설", []))
        rubric = "\n".join(sec.get("교육과정", []))
        if not questions:  # 문제 표식이 없으면 블록 전체를 한 문항으로
            questions = [("1", " ".join(passage[:3]))]
        label = b.field + (" · " + b.subtype if b.subtype else "")
        for num, q in questions:
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name="수시모집 일반전형" + (" (예시문항)" if kind == "example" else ""),
                category=meta.get("category", "essay_based"),
                unit=unit or b.field,
                year=meta["year"],
                kind=kind,
                text=f"[{label}] [문제 {num}] {q}",
                presented_material="\n".join(passage),
                intent=_intent_for(num, sec.get("출제의도", [])),
                rubric=rubric,
                model_answer_hint=hint,
                source_url=meta.get("page_url") or meta["url"],
                source_page=b.page,
            ))
    return recs


def rough_records_mmi(blocks: list[Block], meta: dict) -> list[QuestionRecord]:
    recs: list[QuestionRecord] = []
    for b in blocks:
        passage: list[str] = []
        questions: list[str] = []
        for l in b.lines:
            m = MMI_Q_RE.match(l.text)
            if m and len(m.group(2)) < 200:
                questions.append(m.group(2))
            else:
                passage.append(l.text)
        if not questions:
            questions = ["(제시문 기반 면접 — 문항 문구 미공개, 제시문만 공개)"]
        for q in questions:
            recs.append(QuestionRecord(
                university_code=meta["university_code"],
                admission_name="수시/정시모집 적성·인성면접",
                category="mmi",
                unit=b.field,
                year=meta["year"],
                kind="actual",
                text=q,
                presented_material="\n".join(passage),
                source_url=meta.get("page_url") or meta["url"],
                source_page=b.page,
            ))
    return recs


def segment(pdf_path: Path, meta: dict) -> list[Block]:
    lines = clean_lines(pdf_path)
    if meta.get("category") == "mmi":
        return segment_mmi(lines)
    return segment_general(lines)


def parse(pdf_path: Path, meta: dict) -> list[QuestionRecord]:
    """공통 인터페이스. 규칙 기반 rough 레코드."""
    blocks = segment(pdf_path, meta)
    if meta.get("category") == "mmi":
        return rough_records_mmi(blocks, meta)
    return rough_records_general(blocks, meta)
