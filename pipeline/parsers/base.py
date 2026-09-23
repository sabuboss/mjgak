"""대학별 파서 공통 인터페이스. `parse(pdf_path, meta) -> list[QuestionRecord]`."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

from mjgak_pipeline.models import QuestionRecord


class SourceMeta(dict):
    """universities.json 의 source 항목 + university_code."""


class Parser(Protocol):
    def parse(self, pdf_path: Path, meta: SourceMeta) -> list[QuestionRecord]: ...
