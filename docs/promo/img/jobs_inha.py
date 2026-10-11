# 인하대 인하미래인재(면접형) 블로그 글 이미지. python jobs_inha.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

INHA = pdf("인하대학교")
U, LBL = "인하대학교", "2027학년도 수시모집요강"


def jobs_inha():
    make_thumb(HERE / "thumb-inha.png", "인하대 면접", line2="인하미래인재 면접형", line3="예상 질문 6개 총정리")
    make_capture(HERE / "inha-2027-mirae-method.png", INHA, 14, "1. 모집단위 및 모집인원", ("after", "학교폭력 조치상황 반영방법은 46p 참고"),
                 U, f"{LBL} 11쪽(PDF 14쪽)", "939명 · 1단계 서류 100%로 3.5배수(의예과 3배수) · 2단계 70 + 면접 30", start_pad=12, end_pad=8)
    make_capture(HERE / "inha-2027-mirae-tie.png", INHA, 51, "동점자 처리기준", ("after", "면접평가 진로탐구역량영역 점수"),
                 U, f"{LBL} 48쪽(PDF 51쪽)", "2단계 동점자: 면접 총점 → 면접 의사소통역량 → 면접 진로탐구역량", start_pad=10, end_pad=10)
    make_capture(HERE / "inha-2027-mirae-schedule.png", INHA, 11, "조형예술학과(인물수채화)", ("after", "(충원일정 및 충원방법 안내 포함)"),
                 U, f"{LBL} 8쪽(PDF 11쪽)", "1단계 11월 17일(화) · 면접 11월 21일(토)·22일(일) · 최초 합격 12월 18일(금)", start_pad=3, end_pad=40, start_idx=1)
    make_capture(HERE / "inha-2027-mirae-date1121.png", INHA, 14, "모집단위별 면접고사 일정", ("after", "컴퓨터공학과"),
                 U, f"{LBL} 11쪽(PDF 14쪽)", "11월 21일(토): 경영·사범(수학교육 제외)·사회과학·문과·예체·소융", start_pad=5, end_pad=10)
    make_capture(HERE / "inha-2027-mirae-date1122.png", INHA, 15, "일시", "평가방식 및 진행 방식",
                 U, f"{LBL} 12쪽(PDF 15쪽)", "11월 22일(일): 공과·자연과학·수학교육·의예·간호·바이오 · 시간 변경 불가", start_pad=10, end_pad=10)
    make_capture(HERE / "inha-2027-mirae-interview.png", INHA, 15, "평가방식 및 진행 방식", ("after", "15분 내외(각 면접실별 7~8분 내외)"),
                 U, f"{LBL} 12쪽(PDF 15쪽)", "2:1 개별 · 서류 기반 블라인드 · 8~10분(의예과 2실 15분) · 3개 역량", start_pad=10, end_pad=12)
    make_capture(HERE / "inha-2027-mirae-docs.png", INHA, 13, "학생부종합전형 전형방법 및 평가 안내", 440,
                 U, f"{LBL} 10쪽(PDF 13쪽)", "면접형 서류평가 · 기초학업 30% + 진로탐구 50% + 공동체 20%", start_pad=10)
    make_structure(HERE / "structure-inha.png", [
        "기계공학과에 지원한 이유는 움직이는 물체가 왜 그렇게 움직이는지 계산으로 설명하고, 그 계산으로 더 나은 기계를 설계해 보고 싶어서입니다.",
        "2학년 물리 수행평가에서 종이 다리를 만들어 추를 올렸는데, 같은 종이라도 접는 모양에 따라 버티는 무게가 세 배 넘게 달랐습니다.",
        "재료가 같아도 힘이 어떻게 나뉘느냐가 결과를 바꾼다는 것을 배웠고, 그때부터 구조를 숫자로 따져 보는 공부에 관심이 생겼습니다.",
        "인하대 기계공학과에서 정역학과 재료역학을 배워, 가볍고 튼튼한 구조를 설계하는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_inha()
