# 한국항공대 학생부종합 미래인재전형 블로그 글 이미지. python jobs_kau.py
# 인쇄 쪽수 = PDF 쪽수 - 2
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KAU = pdf("한국항공대학교")
U, LBL = "한국항공대학교", "2027학년도 수시모집요강"


def jobs_kau():
    make_thumb(HERE / "thumb-kau.png", "항공대 면접", line2="한국항공대 미래인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kau-2027-future-units.png", KAU, 27, "1. 모집단위 및 모집인원", "2. 자격기준",
                 U, f"{LBL} 25쪽(PDF 27쪽)", "미래인재 146명 · 공과 52 · AI융합 52 · 항공경영 32 · 항공운항 10",
                 start_pad=12, end_pad=10)
    make_capture(HERE / "kau-2027-future-method.png", KAU, 27, "3. 전형요소", ("after", "최저학력기준 : 미적용"),
                 U, f"{LBL} 25쪽(PDF 27쪽)", "1단계 서류 100% 3배수 · 2단계 1단계 70 + 면접 30 · 수능최저 없음",
                 start_pad=12, end_pad=10)
    make_capture(HERE / "kau-2027-schedule.png", KAU, 6, "Ⅲ. 전형일정", ("after", "12. 23.(수) 14:00"),
                 U, f"{LBL} 4쪽(PDF 6쪽)", "미래인재 1단계 10/30(금) 09:00 · 면접 11/7(토) · 최초합격 12/18",
                 start_pad=12, end_pad=12)
    make_capture(HERE / "kau-2027-interview.png", KAU, 28, "나. 일반면접", ("after", "퇴실 조치하며"),
                 U, f"{LBL} 26쪽(PDF 28쪽)", "면접위원 2인 : 수험생 1명 · 11/7 오전 9시/오후 2시 · 교복 금지",
                 start_pad=12, end_pad=10)
    make_capture(HERE / "kau-2027-interview-eval.png", KAU, 29, "면접고사 평가 기준", "다. 항공운항학과 신체검사",
                 U, f"{LBL} 27쪽(PDF 29쪽)", "면접 평가 학업역량 30% · 진로역량 40% · 공동체역량 30%",
                 start_pad=12, end_pad=14)
    make_capture(HERE / "kau-2027-doc-eval.png", KAU, 28, "가. 서류종합평가 방법", "나. 일반면접",
                 U, f"{LBL} 26쪽(PDF 28쪽)", "서류 평가 학업역량 30% · 진로역량 50% · 공동체역량 20%",
                 start_pad=7, end_pad=14)
    make_capture(HERE / "kau-2027-flight-check.png", KAU, 35, "Ⅵ. 항공운항학과 신체검사 안내", ("after", "기준을 만족하여야 합니다"),
                 U, f"{LBL} 33쪽(PDF 35쪽)", "항공운항학과 항공신체검사 1종 · 적합 판정 서류 12/8(화)까지",
                 start_pad=12, end_pad=10)
    make_structure(HERE / "structure-kau.png", [
        "AI융합대학에 지원한 이유는 컴퓨터가 사진 속 사물을 어떻게 구별하는지 직접 만들어 보며 배우고 싶어서입니다.",
        "2학년 정보 시간에 손글씨 숫자를 분류하는 프로그램을 따라 만들었는데, 제 글씨로 쓴 7을 자꾸 1로 읽었습니다. 그래서 친구들에게 숫자를 받아 학습 자료를 늘렸습니다.",
        "자료를 늘리자 틀리는 경우가 줄었고, 결과는 프로그램보다 자료에 따라 크게 달라진다는 것을 배웠습니다.",
        "AI융합대학에서 인공지능 전공을 골라, 학습 자료를 고르고 점검하는 방법부터 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kau()
