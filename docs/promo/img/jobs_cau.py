# 중앙대 학생부종합 탐구형인재전형 블로그 글 이미지. python jobs_cau.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

CAU = pdf("중앙대학교")
U, LBL = "중앙대학교", "2027학년도 수시 모집요강"


def jobs_cau():
    make_thumb(HERE / "thumb-cau-tam.png", "중앙대 면접", line2="탐구형인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "cau-2027-tam-change.png", CAU, 3, "학생부종합전형", ("after", "의학부의 경우"),
                 U, f"{LBL} 1쪽(PDF 3쪽)", "CAU탐구형인재 → 탐구형인재 · 512명 · 면접 있음 · 수능최저 없음", start_pad=12, end_pad=8)
    make_capture(HERE / "cau-2027-tam-units.png", CAU, 22, "고교 교육과정을 바탕으로", ("after", "총계"),
                 U, f"{LBL} 20쪽(PDF 22쪽)", "탐구형인재 512명 · 경영학 26 · 영어영문·전자전기·약학부 각 20", start_pad=16, end_pad=10)
    make_capture(HERE / "cau-2027-tam-method.png", CAU, 24, "수능최저학력기준", "학교폭력조치사항",
                 U, f"{LBL} 22쪽(PDF 24쪽)", "1단계 서류 100%(3.5~5배수) · 2단계 1단계 70 + 면접 30", start_pad=12, end_pad=10)
    make_capture(HERE / "cau-2027-tam-rule.png", CAU, 24, "학교폭력조치사항", ("after", "적격자가 없는 경우"),
                 U, f"{LBL} 22쪽(PDF 24쪽)", "결시자 불합격 · 최종 동점자는 1단계 성적, 서류 진로역량 순", start_pad=8, end_pad=8)
    make_capture(HERE / "cau-2027-tam-schedule.png", CAU, 23, "전형 전체 일정", ("after", "상기 일정은"),
                 U, f"{LBL} 21쪽(PDF 23쪽)", "1단계 발표 11/26(목) 14시 · 면접 12/5(토)~6(일) · 최초 합격 12/18", start_pad=5, end_pad=8)
    make_capture(HERE / "cau-2027-tam-dates.png", CAU, 23, "모집단위별 면접 일정", ("after", "조정 방법 안내"),
                 U, f"{LBL} 21쪽(PDF 23쪽)", "모집단위별 면접일과 1단계 배수 · 같은 날 안에서 시간 조정 신청 가능", start_pad=10, end_pad=8)
    make_capture(HERE / "cau-2027-tam-interview.png", CAU, 96, "면접 방법", ("after", "공동체의 일원으로서"),
                 U, f"{LBL} 94쪽(PDF 96쪽)", "학생부 기반 · 사정관 2인 · 10분 이내 · 학업준비도 60 · 적합성 30 · 인성 10", start_pad=12, end_pad=10)
    make_structure(HERE / "structure-cau-tam.png", [
        "제가 고른 탐구는 축제 부스의 가격과 판매량 기록을 경제 시간에 배운 수요의 가격탄력성으로 분석한 것입니다.",
        "음료 가격을 시간대마다 두 가지로 정하고 판매량을 적었더니, 가격을 내린 시간대에 판매량이 크게 늘어 전체 매출도 많아졌습니다.",
        "그래프 위의 개념이 실제 판매 기록으로 확인된다는 것을 알았고, 날씨처럼 같이 바뀐 조건을 통제하지 못한 한계도 보였습니다.",
        "경영학부에서 데이터로 가격과 수요를 분석하는 방법을 배워, 조건을 더 엄밀하게 맞춘 분석을 해 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_cau()
