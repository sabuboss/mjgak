# 숙명여대 숙명인재(면접형) 블로그 글 이미지. python jobs_sm_talent.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SM = pdf("숙명여자대학교")
U, LBL = "숙명여자대학교", "2027학년도 수시모집요강"


def jobs_sm_talent():
    make_thumb(HERE / "thumb-sm-talent.png", "숙명여대 면접", line2="숙명인재 면접형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "sm-2027-talent-change.png", SM, 5, "수시모집 주요 변경사항", 566.5,
                 U, f"{LBL} 1쪽(PDF 5쪽)", "391명→361명 · 1단계 3배수→4배수 · 2단계 면접 40%→30%", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-talent-method.png", SM, 18, "라. 전형방법", "마. 전형요소별",
                 U, f"{LBL} 14쪽(PDF 18쪽)", "1단계 서류 100% 4배수 · 2단계 1단계 70 + 면접 30 · 수능최저 없음", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-talent-rule.png", SM, 54, "마. 서류평가, 면접평가", 359.0,
                 U, f"{LBL} 50쪽(PDF 54쪽)", "면접 결시는 불합격 · 2단계 동점자는 면접평가 성적이 1순위", start_pad=10, end_pad=8)
    make_capture(HERE / "sm-2027-talent-schedule.png", SM, 18, "다. 전형일정", "라. 전형방법",
                 U, f"{LBL} 14쪽(PDF 18쪽)", "1단계 11/19(목) 18시 · 전형료 11/20 17시까지 · 면접 11/28~29", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-talent-interview.png", SM, 19, "2) 면접평가", "※ 자세한 내용은",
                 U, f"{LBL} 15쪽(PDF 19쪽)", "평가위원 2인 개별면접 · 블라인드 · 12분 내외 제출서류 기반", start_pad=10, end_pad=6)
    make_capture(HERE / "sm-2027-talent-blind.png", SM, 51, "3) 평가항목 및 평가내용", ("after", "유의하시기 바랍니다"),
                 U, f"{LBL} 47쪽(PDF 51쪽)", "진로역량 · 의사소통능력 및 태도 · 교복 착용 금지", start_pad=10, end_pad=12)
    make_structure(HERE / "structure-sm-talent.png", [
        "경영학부에 지원한 이유는 소비자가 실제로 무엇을 보고 고르는지 자료로 확인하는 일을 계속하고 싶어서입니다.",
        "1학년 때는 광고 기획에 관심이 있었지만, 2학년 학교 매점 설문에서 친구들이 광고보다 가격표 위치를 보고 고른다는 응답이 많아 놀랐습니다.",
        "그때 진로를 광고 하나가 아니라 소비자 행동 전체로 넓혔고, 3학년에는 확률과 통계를 선택해 설문 결과를 직접 분석했습니다.",
        "숙명여대 경영학부에서 마케팅과 경영통계를 배워, 고객 자료로 근거를 대는 마케터가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_sm_talent()
