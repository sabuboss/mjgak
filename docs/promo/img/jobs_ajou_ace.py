# 아주대 학생부종합 ACE전형 블로그 글 이미지. python jobs_ajou_ace.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

AJ = pdf("아주대학교")
U, LBL = "아주대학교", "2027학년도 수시모집요강"


def jobs_ajou_ace():
    make_thumb(HERE / "thumb-ajou-ace.png", "아주대 면접", line2="ACE전형 학생부종합", line3="질문 7개 총정리")
    make_capture(HERE / "ajou-2027-ace-units.png", AJ, 11, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 9쪽(PDF 11쪽)", "학생부종합 ACE전형 519명 · 모집단위별 인원", start_pad=8, end_pad=10)
    make_capture(HERE / "ajou-2027-ace-method.png", AJ, 11, "수능최저학력기준: 없음", ("after", "예비번호를 부여하지 않고"),
                 U, f"{LBL} 9쪽(PDF 11쪽)", "1단계 서류 100%(3배수) · 2단계 1단계 70% + 면접 30% · 최저는 의·약학과만", start_pad=3, end_pad=6)
    make_capture(HERE / "ajou-2027-ace-schedule.png", AJ, 13, "5. 전형일정", "6. 제출서류",
                 U, f"{LBL} 11쪽(PDF 13쪽)", "1단계 11/17(화) · 면접 11/22·28·29 · 의·약학과 12/14(월)", start_pad=8, end_pad=12)
    make_capture(HERE / "ajou-2027-ace-interview.png", AJ, 12, "나. 면접평가(의학과 제외)", "다. 면접평가(의학과)",
                 U, f"{LBL} 10쪽(PDF 12쪽)", "2인 이상 : 1인 개인면접 10분 내외 · 서류 신뢰도 80 + 의사소통능력·태도 20", start_pad=8, end_pad=14)
    make_capture(HERE / "ajou-2027-ace-blind.png", AJ, 54, "2. 면접평가", "다. 평가 항목 및 평가 내용",
                 U, f"{LBL} 52쪽(PDF 54쪽)", "가번호 블라인드 · 교복 착용 금지 · 과락이면 순위와 관계없이 불합격", start_pad=8, end_pad=12)
    make_capture(HERE / "ajou-2027-ace-questions.png", AJ, 55, "마. 면접 질문 예시", 727.0,
                 U, f"{LBL} 53쪽(PDF 55쪽)", "대학이 공개한 면접 질문 예시 · 서류 기반 면접과 의학과 제시문 면접", start_pad=8, end_pad=4)
    make_capture(HERE / "ajou-2027-ace-med.png", AJ, 12, "다. 면접평가(의학과)", "◎ 학교폭력",
                 U, f"{LBL} 10쪽(PDF 12쪽)", "의학과 20분 내외 · 서류 신뢰도 40 + 제시문 활용 면접 60", start_pad=8, end_pad=14)
    make_structure(HERE / "structure-ajou-ace.png", [
        "이 실험은 전체 질량은 그대로 두고 끄는 힘만 키웠을 때 가속도도 커지는지 확인하는 실험이었습니다.",
        "저는 수레에 실었던 추를 하나씩 줄 끝으로 옮겨 매달며 힘을 바꿨고, 손으로 잰 시간은 오차가 커서 스마트폰 영상으로 다시 측정했습니다.",
        "측정 방법을 바꾸자 그래프가 직선에 가까워졌고, 결과보다 측정 방법이 결론을 좌우한다는 것을 배웠습니다.",
        "기계공학과에서 동역학과 계측을 배우며, 측정의 정확도를 먼저 따지는 습관을 이어 가고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_ajou_ace()
