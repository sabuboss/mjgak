"""PDF → 페이지별 텍스트. pymupdf 사용."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pymupdf as fitz


@dataclass
class PageText:
    page: int  # 1-base
    text: str


def extract_pages(pdf_path: Path) -> list[PageText]:
    out: list[PageText] = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            out.append(PageText(page=i, text=page.get_text("text")))
    return out


def chunk_pages(pages: list[PageText], max_chars: int = 12000) -> list[list[PageText]]:
    """LLM 한 번에 넣을 페이지 묶음. 페이지 경계는 유지."""
    chunks: list[list[PageText]] = []
    cur: list[PageText] = []
    size = 0
    for p in pages:
        if cur and size + len(p.text) > max_chars:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(p)
        size += len(p.text)
    if cur:
        chunks.append(cur)
    return chunks
