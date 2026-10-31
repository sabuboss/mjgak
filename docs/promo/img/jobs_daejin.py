# 대진대 학생부종합 윈윈대진전형 면접 블로그 글(naver-104) 이미지. python jobs_daejin.py
# PDF: src/m_대진대학교.pdf (2027학년도 대진대학교 수시모집요강, 66쪽, 2026-06-03 작성, 글자 층 있음).
# 인쇄 쪽수 = PDF 쪽수 - 1 (예: 인쇄 30쪽 = PDF 31쪽). make_capture 의 page 인자는 PDF 쪽수.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

DJ = pdf("대진대학교")
U, LBL = "대진대학교", "2027학년도 수시모집요강"


def lbl(printed):
    return f"{LBL} {printed}쪽(PDF {printed + 1}쪽)"


def jobs_daejin():
    make_thumb(HERE / "thumb-daejin.png", "대진대 면접", line2="윈윈대진전형", line3="질문 7개 총정리")
    make_capture(HERE / "daejin-2027-winwin-units.png", DJ, 31, "1. 모집단위 및 모집인원", ("after", "수능최저학력기준"),
                 U, lbl(30), "윈윈대진 310명 · 간호 36 · 의생명·컴퓨터공학 15 · 최저 없음",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "daejin-2027-winwin-schedule.png", DJ, 31, "3. 전형일정", ("after", "2026.11.13.(금) 14:00"),
                 U, lbl(30), "1단계 11/3(화) 14:00 · 면접 11/7(토)~8(일) · 발표 11/13(금)",
                 start_pad=10, end_pad=12, lr=30)
    make_capture(HERE / "daejin-2027-winwin-method.png", DJ, 32, "4. 전형방법", ("after", "다른 전형에 중복 지원 가능"),
                 U, lbl(31), "1단계 서류 100% 3배수 · 2단계 1단계 70% + 면접 30%",
                 start_pad=6, end_pad=8, lr=30)
    make_capture(HERE / "daejin-2027-winwin-docs.png", DJ, 50, "1. 학생부종합 평가항목", "2. 서류평가 평가등급",
                 U, lbl(49), "서류평가 학업역량 40% · 진로역량 30% · 공동체역량 30%",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "daejin-2027-winwin-interview.png", DJ, 53, "2. 학생부종합 면접고사", ("after", "학교생활기록부 내용을 바탕으로"),
                 U, lbl(52), "2인 이상 · 10분 내외 · 학업 90 · 진로 90 · 공동체 120점",
                 start_pad=10, end_pad=14, lr=30)
    make_capture(HERE / "daejin-2027-blind.png", DJ, 51, "<블라인드 면접 안내 내용>", ("after", "일절 질문하지 않습니다"),
                 U, lbl(50), "교복·액세서리 착용 금지 · 가번호 · 개인정보 언급 시 불이익",
                 start_pad=14, end_pad=14, lr=40)
    make_capture(HERE / "daejin-2027-gyogwa-questions.png", DJ, 52, "1. 학생부교과 면접고사", ("after", "우리학과에 지원한 동기가"),
                 U, lbl(51), "교과 전형: 계열별 공개 문항 3개 중 추첨 1문항 + 지원 동기",
                 start_pad=10, end_pad=10, lr=30)
    make_capture(HERE / "daejin-2027-schedule-all.png", DJ, 13, "1단계", "실기/실적위주(실기우수자전형)",
                 U, lbl(12), "윈윈대진 11/7~8 · 학생부우수자·종단추천자 11/21(토)",
                 start_pad=10, end_pad=7, lr=30)
    make_structure(HERE / "structure-daejin.png", [
        "간호학과에 지원한 동기는 아픈 사람의 작은 변화를 가장 가까이에서 살피는 일이 간호라는 것을 봉사활동에서 느꼈기 때문입니다.",
        "2학년 때 요양원 봉사에서 식사 돕기를 맡았는데, 한 어르신이 매번 음식을 절반 넘게 남기셨습니다.",
        "선생님께 여쭤 보니 삼키기가 힘드셔서였고, 선생님 안내대로 한 숟가락 양을 줄여 천천히 드리자 남기는 양이 줄었습니다. 도움도 먼저 관찰해야 제대로 된다는 것을 배웠습니다.",
        "간호학과에서 환자를 관찰하고 기록하는 법을 제대로 배워, 작은 변화도 놓치지 않는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_daejin()
