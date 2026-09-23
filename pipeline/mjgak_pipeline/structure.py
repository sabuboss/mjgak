"""LLM 구조화: 블록 텍스트 → QuestionRecord 목록 (Anthropic Python SDK, structured outputs).

- 모델: ANTHROPIC_MODEL (기본 claude-sonnet-5). 키: ANTHROPIC_API_KEY (.env.local 또는 환경변수).
- 프롬프트: prompts/structure_questions.md (system, 프롬프트 캐시 대상).
- 한 블록당 1회 호출. 실패 시 예외를 올려 호출부가 rough 레코드로 폴백하게 한다.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from mjgak_pipeline.models import QuestionRecord, StructuredPage

ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / "prompts" / "structure_questions.md"

load_dotenv(ROOT / ".env.local")
load_dotenv(ROOT / ".env")

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")


def has_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


_client: anthropic.Anthropic | None = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def structure_block(
    block_text: str,
    meta: dict,
    field_hint: str = "",
    rough: list[QuestionRecord] | None = None,
) -> list[QuestionRecord]:
    system_prompt = PROMPT.read_text(encoding="utf-8")
    meta_json = json.dumps(
        {
            "university_code": meta["university_code"],
            "year": meta["year"],
            "category": meta.get("category", "essay_based"),
            "admission_name": meta.get("admission_name", ""),
            "kind_hint": "example" if meta.get("kind") == "examples" else "actual",
            "source_url": meta.get("page_url") or meta["url"],
            "source_page": meta.get("source_page"),
            "field_hint": field_hint,
        },
        ensure_ascii=False,
    )
    user = f"<meta>\n{meta_json}\n</meta>\n\n<block>\n{block_text}\n</block>"
    if rough:
        hint = json.dumps([r.model_dump(include={"text", "unit"}) for r in rough], ensure_ascii=False)
        user += "\n\n<rough_hint>\n규칙 기반 1차 추출 결과(참고용, 틀릴 수 있음):\n" + hint + "\n</rough_hint>"

    resp = client().messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
        output_format=StructuredPage,
    )
    if resp.stop_reason == "refusal":
        raise RuntimeError("model refused")
    page: StructuredPage = resp.parsed_output
    for q in page.questions:
        q.university_code = meta["university_code"]
        q.year = meta["year"]
        q.source_url = meta.get("page_url") or meta["url"]
        q.verified = False
    return page.questions
