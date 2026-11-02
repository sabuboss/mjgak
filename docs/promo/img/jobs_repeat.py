# 재수생·N수생 대입 면접 질문 글(naver-124) 이미지. python jobs_repeat.py
# 서울대 PDF: 인쇄 쪽수 = PDF 쪽수 - 4 (인쇄 14쪽 = PDF 18쪽). 수원대 PDF: 인쇄 쪽수 = PDF 쪽수.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"


def jobs_repeat():
    make_thumb(HERE / "thumb-repeat.png", "재수생·N수생", line2="면접 질문 6가지", line3="답변 예시 총정리")
    make_capture(HERE / "snu-2027-repeat-local.png", pdf("서울대학교"), 18, "학생부종합전형(지역균형전형)",
                 ("after", "정성평가하여 서류평가에 반영함"),
                 "서울대학교", f"{LBL} 14쪽(PDF 18쪽)", "지역균형 = 2027년 2월 졸업예정자만 · 1단계 3배수 → 면접 30",
                 start_pad=14, end_pad=10, lr=45)
    make_capture(HERE / "suwon-2027-repeat-reco.png", pdf("수원대학교"), 33, "고교추천전형",
                 ("after", "115명"),
                 "수원대학교", f"{LBL} 33쪽", "고교추천 = 2019년 2월 졸업자부터 지원 · 검정고시 지원 불가",
                 start_pad=60, end_pad=12, lr=64)
    make_structure(HERE / "structure-repeat.png", [
        "작년에는 결과가 아쉬웠지만, 다시 지원한 이유는 점수보다 이 학과에서 배우고 싶은 것이 더 분명해졌기 때문입니다.",
        "재수를 시작하던 봄, 할머니 병원에서 간호사가 약 먹는 순서를 그림 카드로 다시 설명해 주는 모습을 봤습니다.",
        "같은 정보도 전달 방식에 따라 환자의 행동이 달라진다는 것을 그때 알았습니다.",
        "간호학과에서 환자 교육을 배워, 설명을 잘하는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_repeat()
