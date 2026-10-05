# 약학과 블로그 이미지. python jobs_pharm.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure


def jobs_pharm():
    make_thumb(HERE / "thumb-pharm.png", "약학과")
    # 경희대 네오르네상스
    make_capture(HERE / "khu-2027-pharm-method.png", pdf("경희대학교"), 40, "※ 대학수학능력시험(수능) 최저학력기준", "※ 서류평가 및 면접평가 안내는",
                 "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", "네오르네상스 약학과 9명 · 최저 3개 합 4 + 한국사 5 · 1단계 4배수 · 70% + 면접 30%", start_pad=10, end_pad=8)
    make_capture(HERE / "khu-2027-pharm-interview.png", pdf("경희대학교"), 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적",
                 "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)", "공통질문 + 서류확인 면접 · 출제문항 없음 · 2:1 개인면접 10분 · 인성 50% + 전공적합성 50%", start_pad=10, end_pad=8)
    make_capture(HERE / "khu-2027-pharm-schedule.png", pdf("경희대학교"), 41, "5. 전형일정 및 면접평가 상세일정", ("after", "2026. 12. 18(금) 18:00"),
                 "경희대학교", "2027학년도 수시모집요강 39쪽(PDF 41쪽)", "1단계 발표 11월 25일(수) · 면접 12월 5~6일 · 약학대학은 12월 6일(일) 14:00 서울캠퍼스", start_pad=10, end_pad=10)
    # 아주대 ACE
    make_capture(HERE / "ajou-2027-pharm-method.png", pdf("아주대학교"), 11, "◇ 수능최저학력기준: 없음", ("after", "면접평가 30%"),
                 "아주대학교", "2027학년도 수시모집요강 9쪽(PDF 11쪽)", "ACE전형 약학과 15명 · 최저 3개 합 5 충족자 중 3배수 · 70% + 면접 30% · 서류 기반 10분", start_pad=4, end_pad=3)
    make_capture(HERE / "ajou-2027-pharm-schedule.png", pdf("아주대학교"), 13, "5. 전형일정", "6. 제출서류",
                 "아주대학교", "2027학년도 수시모집요강 11쪽(PDF 13쪽)", "의학과·약학과만 1단계 발표 12월 12일(토) · 면접 12월 14일(월) · 블라인드 · 순서 무작위", start_pad=10, end_pad=8)
    # 덕성여대 덕성인재Ⅱ
    make_capture(HERE / "duksung-2027-pharm-method.png", pdf("덕성여자대학교"), 29, "3. 전형방법", "4. 선발원칙",
                 "덕성여자대학교", "2027학년도 수시모집요강 29쪽", "덕성인재Ⅱ 약학과 25명 · 3배수 · 60% + 면접 40% · 수능 최저 없음 · 면접 11월 22일(일)", start_pad=10, end_pad=10, lr=50)
    make_capture(HERE / "duksung-2027-pharm-questions.png", pdf("덕성여자대학교"), 74, "다. 면접평가 운영방법", "4. 블라인드 평가 안내",
                 "덕성여자대학교", "2027학년도 수시모집요강 74쪽", "10분 개별 블라인드 면접 · 평가항목별 면접질문 예시 공개 · '비타민별 항산화 메커니즘' 보고서 질문", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-pharm.png", [
        "약사는 약을 내주는 사람이 아니라 환자가 약을 안전하게 쓰도록 마지막에 확인하는 사람이라고 생각해서 지원했습니다.",
        "할머니가 병원 세 곳에서 받은 약을 한꺼번에 드시다 어지럼증으로 쓰러지셨는데, 약국 약사님이 겹치는 성분을 찾아내 두 가지를 빼 드렸습니다.",
        "의사가 각자 옳은 처방을 해도 합치면 위험해질 수 있고, 그 사이를 보는 사람이 약사라는 것을 배웠습니다.",
        "약학과에서 약물 상호작용과 복약 지도를 제대로 배워, 그때 약사님처럼 환자의 약 전체를 보는 약사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    try:
        jobs_pharm()
        print("OK")
    except Exception:
        traceback.print_exc()
