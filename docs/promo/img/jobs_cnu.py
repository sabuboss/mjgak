# 충남대 학생부종합Ⅰ(면접전형) 블로그 글 이미지. python jobs_cnu.py
# 충남대 PDF: 인쇄 쪽수 = PDF 쪽수 - 2.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_충남대학교.pdf")
U, LBL = "충남대학교", "2027학년도 수시모집요강"


def jobs_cnu():
    make_thumb(HERE / "thumb-cnu.png", "충남대 면접", line2="학생부종합Ⅰ(면접)", line3="예상 질문 7개 총정리")
    make_capture(HERE / "cnu-2027-hakjong1-method.png", P, 33, "1. 모집인원", "나. 동점자 선발 기준",
                 U, f"{LBL} 31쪽(PDF 33쪽)", "면접전형 433명 · 1단계 2배수(10명 미만·의과대학 3배수) · 서류 200 + 면접 100",
                 start_pad=6, end_pad=10, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-tie.png", P, 33, "나. 동점자 선발 기준", ("after", "의사소통능력 > 계열 적합성"),
                 U, f"{LBL} 31쪽(PDF 33쪽)", "동점자: 서류 점수 → 면접 점수 → 서류 요소별 → 면접 요소별",
                 start_pad=10, end_pad=12, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-min.png", P, 34, "다. 수능최저학력기준", "라. [학생부종합",
                 U, f"{LBL} 32쪽(PDF 34쪽)", "면접전형 최저는 사범·간호·의과·수의과대학만 적용",
                 start_pad=10, end_pad=10, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-schedule.png", P, 34, "라. [학생부종합", ("after", "동점자 모두 면접대상자로 선발함"),
                 U, f"{LBL} 32쪽(PDF 34쪽)", "1단계 11/20(금) 15시 이후 · 면접 12/1~12/4 단과대학별",
                 start_pad=10, end_pad=10, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-interview.png", P, 95, "2. 면접고사", "라. 면접고사 유의사항",
                 U, f"{LBL} 93쪽(PDF 95쪽)", "면접관 2 : 지원자 1 · 15분 이내 · 의사소통 37.8 · 계열 37.8 · 사회 24.4",
                 start_pad=10, end_pad=10, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-blind.png", P, 95, "라. 면접고사 유의사항", ("after", "불합격 처리됨"),
                 U, f"{LBL} 93쪽(PDF 95쪽)", "블라인드 · 명찰·교복 착용 금지 · 신분증·수험표 · 휴대폰 소지 불가",
                 start_pad=10, end_pad=10, lr=14)
    make_capture(HERE / "cnu-2027-hakjong1-fail.png", P, 17, "라. 불합격 처리에 관한 사항", "5) 제출기한",
                 U, f"{LBL} 15쪽(PDF 17쪽)", "면접 불참 불합격 · 학생부종합 면접 100점 중 40점 미만 과락",
                 start_pad=5, end_pad=3, lr=14)
    make_structure(HERE / "structure-cnu.png", [
        "행정학부에 지원한 이유는 좋은 정책도 주민에게 알려지지 않으면 쓰이지 않는다는 것을 직접 확인했기 때문입니다.",
        "1학년 통합사회 시간에 동네 청소년 지원 사업을 조사했는데, 반 친구 서른 명 가운데 그 사업을 아는 사람이 세 명뿐이었습니다.",
        "2학년 자율활동에서 구청 누리집의 청소년 사업 다섯 개를 한 장짜리 안내문으로 정리해 게시판에 붙였고, 한 달 뒤 두 명이 실제로 신청했습니다.",
        "행정학부에서 정책이 시민에게 닿는 과정을 공부하고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_cnu()
