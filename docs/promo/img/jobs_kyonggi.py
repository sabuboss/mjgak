# 경기대 KGU학생부종합전형 블로그 글(naver-86) 이미지. python jobs_kyonggi.py
# 경기대 PDF(90쪽)는 인쇄 쪽수 = PDF 쪽수 - 4 (PDF 5쪽 = 인쇄 "- 1 -", PDF 19 = 15, PDF 46 = 42).
# 기존 kyonggi-2027-tour-* (학과 글 32) 와 겹치지 않게 kgu 를 붙인다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_경기대학교.pdf")
U, LBL = "경기대학교", "2027학년도 수시모집요강"


def jobs_kyonggi():
    make_thumb(HERE / "thumb-kyonggi.png", "경기대 면접", line2="KGU학생부종합", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kyonggi-2027-kgu-method.png", P, 19, "가. 모집단위 및 모집인원", "라. 선발원칙",
                 U, f"{LBL} 15쪽(PDF 19쪽)", "678명 · 1단계 서류 100% 3배수 · 2단계 70 + 면접 30 · 최저 미적용",
                 start_pad=10, end_pad=10, lr=18)
    make_capture(HERE / "kyonggi-2027-kgu-rule.png", P, 19, "라. 선발원칙", "기타 사항은 본교의",
                 U, f"{LBL} 15쪽(PDF 19쪽)", "1단계 50점·면접 15점 미만 불선발 · 동점자는 면접 성적부터",
                 start_pad=10, end_pad=8, lr=18)
    make_capture(HERE / "kyonggi-2027-kgu-schedule.png", P, 13, "마. 학생부종합(KGU", "바. 학생부종합(SW",
                 U, f"{LBL} 9쪽(PDF 13쪽)", "1단계 11/20(금) · 면접 11/29 · 12/5 · 12/6 · 모두 수원캠퍼스",
                 start_pad=10, end_pad=12, lr=18)
    make_capture(HERE / "kyonggi-2027-kgu-interview.png", P, 46, "라. 학생부종합전형 면접평가 방법", "디자인학부-아이디어스케치",
                 U, f"{LBL} 42쪽(PDF 46쪽)", "면접 30% · 잠재역량 15 · 사회역량 10 · 소통역량 5",
                 start_pad=10, end_pad=10, lr=18)
    make_capture(HERE / "kyonggi-2027-kgu-design.png", P, 46, "디자인학부-아이디어스케치", ("after", "질문에 대한 바른 태도와 성의"),
                 U, f"{LBL} 42쪽(PDF 46쪽)", "디자인학부 · 아이디어스케치 작성 → 발표 → 질의응답",
                 start_pad=10, end_pad=10, lr=18, end_idx=-1)
    make_capture(HERE / "kyonggi-2027-kgu-blind.png", P, 47, "마. 학생부종합전형 공정성", ("after", "개인정보제공 동의여부 확인"),
                 U, f"{LBL} 43쪽(PDF 47쪽)", "블라인드 면접 · 교복 착용 금지 · 녹화·녹음",
                 start_pad=10, end_pad=10, lr=18)
    make_capture(HERE / "kyonggi-2027-kgu-document.png", P, 44, "다. 학생부종합전형 서류평가 방법", "서류 신뢰도 검증을 위해",
                 U, f"{LBL} 40쪽(PDF 44쪽)", "서류평가 · 학업성취 30 · 계열적합 30 · 자기주도 20 · 공동체 20",
                 start_pad=10, end_pad=8, lr=18)
    make_structure(HERE / "structure-kyonggi.png", [
        "수업에서 발표한 주제는 2학년 경제 시간의 '편의점 1+1 행사는 정말 이득일까'입니다.",
        "처음에는 가격만 비교해 늘 이득이라고 했는데, 친구가 다 먹지 못하고 버리는 경우는 어떠냐고 물었습니다.",
        "그래서 반 친구 스무 명에게 다 먹었는지 물어 버린 양까지 넣어 다시 계산했고, 사람마다 이득이 다르다는 결론으로 고쳤습니다.",
        "경제학부에서 사람들의 실제 선택을 데이터로 분석하는 방법을 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kyonggi()
