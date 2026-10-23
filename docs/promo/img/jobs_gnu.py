# 경상국립대 학생부종합(일반전형)_면접 블로그 글 이미지. python jobs_gnu.py
# PDF: 인쇄 쪽수 = PDF 쪽수 - 2 (PDF 3쪽 = 인쇄 1쪽 ~ PDF 103쪽 = 인쇄 101쪽).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

G = pdf("경상국립대학교")
U, LBL = "경상국립대학교", "2027학년도 수시모집요강"


def jobs_gnu():
    make_thumb(HERE / "thumb-gnu.png", "경상국립대", line2="일반전형(면접)", line3="질문 7개 총정리")
    make_capture(HERE / "gnu-2027-change.png", G, 9, "전형 신설 및 변경", ("after", "동법 시행령"),
                 U, f"{LBL} 7쪽(PDF 9쪽)", "학생부종합(일반전형) 일괄·면접 분리 · 지역의사선발전형 신설",
                 start_pad=12, end_pad=8, lr=45)
    make_capture(HERE / "gnu-2027-units.png", G, 10, "학생부종합전형 면접고사 시행", ("after", "신설된 지역의사선발전형"),
                 U, f"{LBL} 8쪽(PDF 10쪽)", "면접 모집단위 · 의예과·약학과 5배수 · 그 외 3배수 · 행정학과 미시행",
                 start_pad=14, end_pad=8, lr=45)
    make_capture(HERE / "gnu-2027-method.png", G, 36, "학생부종합(일반전형)", "4) 서류평가",
                 U, f"{LBL} 34쪽(PDF 36쪽)", "1단계 서류 100% · 2단계 1단계 80% + 면접 20% · 수능최저",
                 start_pad=12, end_pad=8, lr=45)
    make_capture(HERE / "gnu-2027-schedule.png", G, 15, "기간(일시)", 527,
                 U, f"{LBL} 13쪽(PDF 15쪽)", "1단계 11/13(금) 16시 · 면접 11/25(수)~26(목) · 발표 12/18(금)",
                 start_pad=10, lr=45)
    make_capture(HERE / "gnu-2027-interview.png", G, 60, "나. 평가기준", ("after", "고사장으로 이동"),
                 U, f"{LBL} 58쪽(PDF 60쪽)", "공개 문항(예시) 4개 · 3인 1조 · 15분 내외 개별면접",
                 start_pad=8, end_pad=12, lr=45)
    make_capture(HERE / "gnu-2027-blind.png", G, 61, "면접 응시생 유의사항", ("after", "평가에 불이익을 받을 수 있음"),
                 U, f"{LBL} 59쪽(PDF 61쪽)", "면접조 변경 불가 · 신분증·수험표 · 교복 불허 · 블라인드",
                 start_pad=10, end_pad=14, lr=45)
    make_structure(HERE / "structure-gnu.png", [
        "물리교육과에 지원하며 가장 오래 붙잡은 탐구는 진자의 주기가 무엇에 따라 달라지는지였습니다.",
        "추의 무게와 줄 길이를 바꿔 가며 열 번씩 잰 결과, 무게는 거의 상관이 없고 줄 길이가 주기를 바꾼다는 것을 확인했습니다.",
        "처음에는 한 번만 재서 값이 들쭉날쭉했는데, 열 번 잰 평균을 쓰자 공식과 가까워져 측정을 반복하는 이유를 알게 됐습니다.",
        "물리교육과에서 학생들이 직접 재 보며 개념을 확인하는 실험 수업을 설계하는 법을 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_gnu()
