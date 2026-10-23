# 덕성여대 학생부종합 덕성인재전형Ⅱ 블로그 글 이미지. python jobs_dsw.py
# 덕성여자대학교 PDF: 인쇄 쪽수 = PDF 쪽수 (표지 PDF 1쪽, 인쇄 03쪽 = PDF 3쪽 확인).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

DS = str(SRC / "m_덕성여자대학교.pdf")
U, LBL = "덕성여자대학교", "2027학년도 수시모집요강"


def jobs_dsw():
    make_thumb(HERE / "thumb-dsw.png", "덕성여대 면접", line2="덕성인재전형Ⅱ", line3="공개 질문 답변법")
    make_capture(HERE / "dsw-2027-units.png", DS, 29, "1. 모집단위 및 모집인원", "3. 전형방법",
                 U, f"{LBL} 29쪽", "덕성인재전형Ⅱ 240명 · 약학과 25명 · 인문사회 74명 · 자유전공 64명",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "dsw-2027-method.png", DS, 29, "3. 전형방법", ("after", "합니다(p.80 참고)."),
                 U, f"{LBL} 29쪽", "1단계 서류 100% 3~4배수 · 2단계 1단계 60% + 면접 40% · 최저 없음",
                 start_pad=10, end_pad=8, lr=40)
    make_capture(HERE / "dsw-2027-schedule.png", DS, 30, "5. 전형일정", "6. 제출서류",
                 U, f"{LBL} 30쪽", "1단계 11/12(목) · 면접 11/21(토)·11/22(일) 모집단위별 · 발표 12/18",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "dsw-2027-unit-eval.png", DS, 73, "모집단위별 평가 방안", "3. 면접평가 주요사항",
                 U, f"{LBL} 73쪽", "모집단위별 평가 방안(탐구역량) · 내 모집단위 항목을 확인",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "dsw-2027-interview.png", DS, 73, "3. 면접평가 주요사항", ("after", "자기효능감을 판단할 수 있는가?"),
                 U, f"{LBL} 73쪽", "면접 서류 신뢰성 50 · 종합적 사고력 30 · 공동체역량 20",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "dsw-2027-blind.png", DS, 74, "다. 면접평가 운영방법", "라. 평가항목별",
                 U, f"{LBL} 74쪽", "10분 내외 개별면접 · 면접위원 2인 · 가번호 블라인드 · 교복 등 금지",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "dsw-2027-questions.png", DS, 74, "라. 평가항목별", "4. 블라인드 평가 안내",
                 U, f"{LBL} 74쪽", "대학이 공개한 평가항목별 면접질문 예시 13개",
                 start_pad=10, end_pad=10, lr=40)
    make_structure(HERE / "structure-dsw.png", [
        "가장 흥미로웠던 주제는 '사람은 왜 처음 본 정보에 끌려가는가'였습니다.",
        "판단의 오류를 다룬 책을 읽고 사회문화 시간에 설문 문항의 순서만 바꿔 두 반에 돌렸더니, 앞 문항에 따라 같은 질문의 답이 달라졌습니다.",
        "그 뒤로 기사의 숫자를 볼 때 무엇을 먼저 보여 줬는지부터 확인하는 습관이 생겼습니다.",
        "글로벌융합대학에서 심리학과 사회학을 함께 배우며 사람의 판단이 어떻게 만들어지는지 더 탐구하고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dsw()
