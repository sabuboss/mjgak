# 이화여대 학생부종합 미래인재전형-면접형 블로그 글 이미지. python jobs_ewha.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

EW = pdf("이화여자대학교")
U, LBL = "이화여자대학교", "2027학년도 수시모집요강"


def jobs_ewha():
    make_thumb(HERE / "thumb-ewha-mi.png", "이화여대 면접", line2="미래인재 면접형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "ewha-2027-mi-overview.png", EW, 5, "1.  입학전형 개요", "수시 소계",
                 U, f"{LBL} 6쪽(PDF 5쪽)", "면접형 209명 2단계 · 서류형 909명 서류 100% · 예체능서류 39명", start_pad=10, end_pad=-2)
    make_capture(HERE / "ewha-2027-mi-units.png", EW, 18, "1.  모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 19쪽(PDF 18쪽)", "미래인재-면접형 209명 · 국제학부 43명 · 인공지능데이터사이언스 12명", start_pad=-15, end_pad=8)
    make_capture(HERE / "ewha-2027-mi-method.png", EW, 19, "3. 전형방법 및 전형요소", ("after", "적용하지 않음"),
                 U, f"{LBL} 20쪽(PDF 19쪽)", "1단계 서류 100% 5배수 · 2단계 1단계 70 + 면접 30 · 수능최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "ewha-2027-mi-schedule.png", EW, 8, "2. 전형별 고사", ("after", "체육과학부"),
                 U, f"{LBL} 9쪽(PDF 8쪽)", "면접형 1단계 11/12(목) · 면접 11/21~22 · 최종 12/3(목)", start_pad=2, end_pad=8)
    make_capture(HERE / "ewha-2027-mi-dates.png", EW, 9, "3. 면접고사 및 논술고사", "나. 논술고사",
                 U, f"{LBL} 10쪽(PDF 9쪽)", "모집단위별 11/21(토) 또는 11/22(일) · 13:20~19:00", start_pad=10, end_pad=4)
    make_capture(HERE / "ewha-2027-mi-interview.png", EW, 39, "3. 학생부종합전형 면접 평가요소", 217,
                 U, f"{LBL} 40쪽(PDF 39쪽)", "면접 평가요소: 학업역량 · 진로역량 · 발전가능성", start_pad=10, end_pad=4)
    make_capture(HERE / "ewha-2027-mi-doc.png", EW, 38, "2. 학생부종합전형 서류 평가요소", 521,
                 U, f"{LBL} 39쪽(PDF 38쪽)", "서류 평가요소: 학업역량 · 학교활동의 우수성 · 발전가능성", start_pad=-8)
    make_structure(HERE / "structure-ewha-mi.png", [
        "경제학과에 지원한 이유는 같은 정책이라도 사람마다 받는 영향이 다른 까닭을 자료로 설명하고 싶어서입니다.",
        "1학년 통합사회 시간에 최저임금 기사를 읽고, 일하는 사람과 가게를 운영하는 사람의 입장이 정반대라는 점이 궁금해졌습니다.",
        "2학년에 경제를 선택해 두 입장을 수요·공급 그래프로 정리해 보니, 그래프만으로는 설명되지 않는 부분이 있다는 것을 알게 됐습니다.",
        "경제학과에서 경제 이론과 자료 분석 방법을 배워, 정책의 영향을 숫자로 따져 보는 공부를 이어 가고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_ewha()
