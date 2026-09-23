"""문항 레코드 스키마. SPEC 4장 `questions` 테이블과 1:1 대응."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Kind = Literal["actual", "example", "predicted", "none"]
Category = Literal["student_record", "essay_based", "personality", "major", "english", "mmi"]


class QuestionRecord(BaseModel):
    university_code: str = Field(description="universities.json 의 code (예: snu)")
    admission_name: str = Field(description="전형명 (예: 일반전형, 지역균형전형)")
    category: Category = Field(description="면접 유형")
    unit: str = Field(default="", description="모집단위/계열 (예: 인문대학, 자연계열, 의예과)")
    year: int = Field(description="학년도 (예: 2026)")
    kind: Kind = Field(description="actual=실제 기출 원문, example=대학이 낸 예시질문, none=문항 미공개(평가영역만)")
    text: str = Field(description="문항 원문. 그대로 옮긴다")
    presented_material: str = Field(default="", description="제시문 (있으면 원문 그대로, 길면 앞 2000자)")
    intent: str = Field(default="", description="출제 의도 요약")
    rubric: str = Field(default="", description="채점 기준/평가 요소 요약")
    model_answer_hint: str = Field(default="", description="해설·예시 답안의 요점 요약")
    source_url: str = Field(description="원문 PDF 또는 게시글 URL")
    source_page: Optional[int] = Field(default=None, description="PDF 페이지 번호 (1-base)")
    verified: bool = False


class StructuredPage(BaseModel):
    """LLM 구조화 출력: 한 텍스트 청크에서 뽑은 문항들."""
    questions: list[QuestionRecord]
