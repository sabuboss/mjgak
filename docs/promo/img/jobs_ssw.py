# 성신여대 학생부종합 자기주도인재전형 블로그 글 이미지. python jobs_ssw.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SS = pdf("성신여자대학교")
U, LBL = "성신여자대학교", "2027학년도 수시모집요강"


def jobs_ssw():
    make_thumb(HERE / "thumb-ssw.png", "성신여대 면접", line2="자기주도인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "ssw-2027-units.png", SS, 7, "1. 정원내 전형", ("after", "법학부"),
                 U, f"{LBL} 6쪽(PDF 7쪽)", "첫 열이 자기주도인재 · 법학부 30 · 경영학과 27 (합계 533명은 7쪽)", start_pad=10, end_pad=7)
    make_capture(HERE / "ssw-2027-method.png", SS, 17, "3. 전형요소별 반영비율", ("after", "면접평가 안내(p.40)"),
                 U, f"{LBL} 16쪽(PDF 17쪽)", "1단계 서류 100% 3배수 · 2단계 서류 60 + 면접 40 · 최저 없음", start_pad=10, end_pad=10)
    make_capture(HERE / "ssw-2027-tie.png", SS, 48, "동점자 처리기준", ("after", "면접평가 항목 중 교직적성"),
                 U, f"{LBL} 47쪽(PDF 48쪽)", "2단계 동점자 1순위 면접평가 점수, 2순위 면접 진로역량", start_pad=16, end_pad=6)
    make_capture(HERE / "ssw-2027-schedule.png", SS, 11, "구분", ("after", "논술우수자전형"),
                 U, f"{LBL} 10쪽(PDF 11쪽)", "1단계·고사장 발표 11/13(금) 10시 예정 · 면접 11/21~22, 11/28~29", start_pad=8, end_pad=3)
    make_capture(HERE / "ssw-2027-interview.png", SS, 41, "1. 학생부종합전형 면접평가 공통사항", "2. 전형별 평가항목 및 반영비율",
                 U, f"{LBL} 40쪽(PDF 41쪽)", "입학사정관 2명 : 지원자 1명 약 10분 · 자기소개 질문 없음", start_pad=10, end_pad=12)
    make_capture(HERE / "ssw-2027-eval-career.png", SS, 41, "2. 전형별 평가항목 및 반영비율", ("after", "진로 활동 참여 과정에서 나타나는"),
                 U, f"{LBL} 40쪽(PDF 41쪽)", "면접 진로역량 50%: 진로설계·진로학업·진로탐색역량", start_pad=10, end_pad=10)
    make_capture(HERE / "ssw-2027-eval-community.png", SS, 42, "고교 교육과정 내에서 이루어지는 학업 참여", ("after", "대안적 해결방법 모색"),
                 U, f"{LBL} 41쪽(PDF 42쪽)", "학업역량 30% · 공동체역량 20% · 사범대학은 교직 적성·인성 20%", start_pad=18, end_pad=10)
    make_structure(HERE / "structure-ssw.png", [
        "바이오신약의과학부에 지원한 이유는 약이 몸속에서 어떻게 작용하는지를 화학과 생명과학을 함께 써서 공부하고 싶어서입니다.",
        "1학년 통합과학의 효소 실험을 계기로 2학년에 화학과 생명과학을 함께 골랐고, 3학년에는 학교에 열리지 않은 심화 과목을 공동교육과정으로 들었습니다.",
        "화학에서 배운 분자 구조가 생명과학의 효소 작용을 이해하는 데 바로 쓰이는 것을 보고, 두 과목을 이어서 공부해야 한다는 것을 알았습니다.",
        "바이오신약의과학부에서 생화학과 약리학을 배워, 약이 몸속에서 작용하는 원리를 연구하고 싶습니다.",
    ])


if __name__ == "__main__" and "dates" not in sys.argv:
    jobs_ssw()


def jobs_ssw_dates():
    # 입학처 공지(2026-07-14) 「2027학년도 수시모집 학생부종합전형 면접고사 사전 안내」 2쪽 모집단위별 면접일자
    make_capture(HERE / "ssw-2027-unit-dates.png", pdf("성신여자대학교_면접안내"), 2, "모집단위별 면접일자", ("after", "사범"),
                 "성신여자대학교", "입학처 공지 「2027학년도 수시모집 학생부종합전형 면접고사 사전 안내」(2026.07.14) 2쪽",
                 "자기주도인재 모집단위별 면접일 · 11월 21·22·28·29일 중 하루",
                 start_pad=12, end_pad=12, end_idx=-1)


if __name__ == "__main__" and "dates" in sys.argv:
    jobs_ssw_dates()
