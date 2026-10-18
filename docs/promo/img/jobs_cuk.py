# 가톨릭대 학생부종합 잠재능력우수자면접전형 블로그 글 이미지. python jobs_cuk.py
# 가톨릭대학교 PDF: 인쇄 쪽수 = PDF 쪽수 - 2.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_가톨릭대학교.pdf")
U, LBL = "가톨릭대학교", "2027학년도 수시모집요강"


def jobs_cuk():
    make_thumb(HERE / "thumb-cuk.png", "가톨릭대 면접", line2="잠재능력우수자면접", line3="예상 질문 7개 총정리")
    make_capture(HERE / "cuk-2027-units.png", P, 32, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 30쪽(PDF 32쪽)", "잠재능력우수자면접 277명 · 신학과 32명 · 10명 모집단위 8곳",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "cuk-2027-method.png", P, 32, "3. 대학수학능력시험", ("after", "(7쪽 참조)"),
                 U, f"{LBL} 30쪽(PDF 32쪽)", "최저 없음 · 1단계 서류 100% 4배수 · 2단계 1단계 70 + 면접 30",
                 start_pad=10, end_pad=8, lr=40)
    make_capture(HERE / "cuk-2027-eval.png", P, 33, "나. 서류종합평가", "라. 학생부종합전형 안내",
                 U, f"{LBL} 31쪽(PDF 33쪽)", "서류 학업 40 · 진로 35 · 공동체 25 / 면접 10분 내외 개별 면접",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "cuk-2027-schedule.png", P, 13, "‧학생부종합(잠재능력우수자면접전형)", 545,
                 U, f"{LBL} 11쪽(PDF 13쪽)", "면접 12/5(토) 08:30~ · 신학과 10/30(금) · 고사장은 3일 전 공지",
                 start_pad=12, lr=40)
    make_capture(HERE / "cuk-2027-blind.png", P, 77, "2. 면접평가", "라. 면접평가요소별",
                 U, f"{LBL} 75쪽(PDF 77쪽)", "평가자 2인 이상 · 10분 내외 · 블라인드(교복 착용 등 불이익)",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "cuk-2027-interview.png", P, 77, "라. 면접평가요소별", ("after", "참관이 진행될 수 있습니다"),
                 U, f"{LBL} 75쪽(PDF 77쪽)", "면접 학업역량 30 · 진로역량 50 · 공동체역량 20",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "cuk-2027-principal.png", P, 39, "1. 모집단위 및 모집인원", "4. 전형방법",
                 U, f"{LBL} 37쪽(PDF 39쪽)", "학교장추천 50명 · 약학 9 · 의예 25 · 간호 16 · 약학·의예 최저",
                 start_pad=12, end_pad=10, lr=40)
    make_structure(HERE / "structure-cuk.png", [
        "심리학과에 지원한 이유는 같은 질문에도 상황에 따라 사람들의 답이 달라지는 까닭을 알고 싶어졌기 때문입니다.",
        "2학년 사회·문화 시간에 질문 순서가 응답에 영향을 준다는 내용을 배우고, 반 친구 서른 명에게 같은 두 질문을 순서만 바꿔 물어봤습니다.",
        "순서에 따라 답이 눈에 띄게 달라지는 것을 보고, 사람의 판단은 생각보다 상황에 크게 흔들린다는 것을 알았습니다.",
        "심리학과에서 실험 설계와 통계를 배워, 사람의 판단을 정확하게 재는 연구를 해 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_cuk()
