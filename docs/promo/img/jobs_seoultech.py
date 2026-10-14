# 서울과기대 학생부종합 학교생활우수자전형 블로그 글 이미지. python jobs_seoultech.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

ST = pdf("서울과학기술대학교")
U, LBL = "서울과학기술대학교", "2027학년도 수시모집요강"


def jobs_seoultech():
    make_thumb(HERE / "thumb-seoultech.png", "서울과기대 면접", line2="학교생활우수자", line3="예상 질문 7개 총정리")
    make_capture(HERE / "seoultech-2027-life-units.png", ST, 30, "3. 학생부종합(학교생활우수자전형)", ("after", "수능최저학력기준: 없음"),
                 U, f"{LBL} 26쪽(PDF 30쪽)", "학교생활우수자 496명 · 기계공학과 39명 등 · 수능최저 없음", start_pad=10, end_pad=10)
    make_capture(HERE / "seoultech-2027-life-method.png", ST, 30, "■ 전형방법", ("after", "교복 착용 금지"),
                 U, f"{LBL} 26쪽(PDF 30쪽)", "1단계 서류 100% 3배수 · 2단계 1단계 70% + 면접 30%", start_pad=10, end_pad=10)
    make_capture(HERE / "seoultech-2027-life-rule.png", ST, 31, "■ 선발원칙", "■ 전형일정",
                 U, f"{LBL} 27쪽(PDF 31쪽)", "2단계 동점자 1순위는 서류평가 총점 · 4순위까지 동점이면 모두 선발", start_pad=10, end_pad=10)
    make_capture(HERE / "seoultech-2027-life-schedule.png", ST, 31, "■ 전형일정", ("after", "시간 변경 불가함"),
                 U, f"{LBL} 27쪽(PDF 31쪽)", "1단계 11/20(금) 14:00 · 면접 11/28(토) 08:30 / 14:00 · 시간 변경 불가", start_pad=10, end_pad=10)
    make_capture(HERE / "seoultech-2027-life-process.png", ST, 60, "■ 평가절차", "■ 평가요소 및 비율",
                 U, f"{LBL} 56쪽(PDF 60쪽)", "면접대상자 3배수 · 2인의 면접위원이 학생 1명당 10분 내외", start_pad=10, end_pad=12)
    make_capture(HERE / "seoultech-2027-life-eval.png", ST, 61, "면접평가 평가요소 및 비율", ("after", "상호작용을 이끌어가는 능력"),
                 U, f"{LBL} 57쪽(PDF 61쪽)", "면접 학업역량 35% · 진로역량 40% · 공동체역량 25%", start_pad=10, end_pad=10)
    make_capture(HERE / "seoultech-2027-life-howto.png", ST, 61, "(참고) 면접평가 더 알아보기", ("after", "참관할 수 있음"),
                 U, f"{LBL} 57쪽(PDF 61쪽)", "제출서류 기반 개별면접 · 면접위원 2인 · 블라인드 · 교복 착용 금지", start_pad=10, end_pad=12)
    make_structure(HERE / "structure-seoultech.png", [
        "기계공학과에 지원한 이유는 움직이는 기계가 왜 고장 나는지를 원리로 설명할 수 있는 엔지니어가 되고 싶어서입니다.",
        "1학년 때 자전거 체인이 자주 빠져 수리점에 갔는데, 체인이 늘어나 톱니와 맞지 않게 된 것이 원인이라는 말을 들었습니다.",
        "그 뒤 물리학에서 힘과 운동을 배우며 체인에 걸리는 힘을 직접 그려 봤고, 기어 모형을 만들어 톱니 수에 따라 회전 속도가 달라지는 것도 확인했습니다.",
        "서울과기대 기계공학과에서 기계가 움직이는 원리와 부품 설계를 제대로 배워, 고장의 원인을 찾아 고치는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_seoultech()
