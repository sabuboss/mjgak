# 강남대 학생부종합 학교생활우수자전형2 블로그 글(naver-83) 이미지. python jobs_kangnam.py
# 강남대 PDF 는 인쇄 쪽수 = PDF 쪽수 (PDF 3쪽 = 인쇄 "- 3 -", PDF 72쪽까지 같은 관계).
# 기존 kangnam-2027-ece-*, kangnam-2027-sped-* (학과 글 02·26·37) 와 겹치지 않게 s2 를 붙인다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_강남대학교.pdf")
U, LBL = "강남대학교", "2027학년도 수시모집요강"


def jobs_kangnam():
    make_thumb(HERE / "thumb-kangnam.png", "강남대 면접", line2="학교생활우수자2", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kangnam-2027-s2-units.png", P, 26, "모집단위 및 모집인원", "전형방법",
                 U, f"{LBL} 26쪽", "55명 · 유아교육 20 · 교육학 16 · 초등특수 8 · 중등특수 8 · 디자인 3",
                 start_pad=10, end_pad=12, lr=45)
    make_capture(HERE / "kangnam-2027-s2-method.png", P, 26, "전형방법", ("after", "종합적 사고력 및 의사소통능력"),
                 U, f"{LBL} 26쪽", "1단계 서류 100% 3배수 · 2단계 1단계 70% + 면접 30% · 최저 없음",
                 start_pad=10, end_pad=12, lr=45)
    make_capture(HERE / "kangnam-2027-s2-tie.png", P, 27, "선발원칙", "전형일정",
                 U, f"{LBL} 27쪽", "면접 결시자 선발 제외 · 동점자는 면접 점수 → 인성적 자질 순",
                 start_pad=10, end_pad=12, lr=36)
    make_capture(HERE / "kangnam-2027-s2-schedule.png", P, 27, "전형일정", "제출서류",
                 U, f"{LBL} 27쪽", "1단계 10/30(금) · 면접 11/7(토)~11/8(일) 중 지정일 · 합격 12/18(금)",
                 start_pad=10, end_pad=12, lr=45)
    make_capture(HERE / "kangnam-2027-s2-interview.png", P, 49, "면접평가", "면접평가 일시",
                 U, f"{LBL} 49쪽", "면접관 3인 대 지원자 1인 · 15분 이내 · 블라인드 · 교복 금지",
                 start_pad=10, end_pad=14, lr=36)
    make_capture(HERE / "kangnam-2027-s2-date.png", P, 49, "면접평가 일시", ("after", "면접평가 참여 불가"),
                 U, f"{LBL} 49쪽", "1단계 발표 때 고사장 조회 · 개인별 면접일시 변경 불가",
                 start_pad=10, end_pad=12, lr=45)
    make_capture(HERE / "kangnam-2027-s2-disabled.png", P, 37, "모집단위 및 모집인원", "서류평가, 면접평가 방법",
                 U, f"{LBL} 37쪽", "장애인 등 대상자전형 14명 · 1단계 3배수 · 2단계 70 + 30 · 최저 없음",
                 start_pad=10, end_pad=6, lr=45)
    make_structure(HERE / "structure-kangnam.png", [
        "유아교육과에 지원한 이유는 놀이가 아이의 말을 끌어낸다는 것을 직접 봤기 때문입니다.",
        "2학년 진로 체험으로 유치원 보조교사를 했을 때, 말수가 적은 아이에게 질문만 계속하자 아이는 블록만 만졌습니다.",
        "질문을 멈추고 아이가 쌓은 모양을 따라 쌓자, 아이가 먼저 '이건 우리 집'이라고 말을 걸어 왔습니다.",
        "입학하면 놀이를 관찰하고 아이의 말을 기록하는 방법을 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kangnam()
