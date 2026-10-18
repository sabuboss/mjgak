# 강원대 학생부종합 미래인재면접전형 블로그 글 이미지. python jobs_kwnu.py
# 강원대 PDF: 인쇄 쪽수 = PDF 쪽수 - 2 (PDF 3쪽 = 인쇄 1쪽).
# 약자 kwnu (kw-* 는 광운대).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

KW = str(SRC / "m_강원대학교.pdf")
U, LBL = "강원대학교", "2027학년도 수시모집요강"


def jobs_kwnu():
    make_thumb(HERE / "thumb-kwnu.png", "강원대 면접", line2="미래인재면접전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kwnu-2027-summary.png", KW, 4, "캠퍼스", ("after", "학생부종합(기회균형전형)"),
                 U, f"{LBL} 2쪽(PDF 4쪽)", "춘천 347명 · 지역인재면접 15명 · 1단계 서류 100% · 2단계 서류 60% + 면접 40%",
                 start_pad=13, end_pad=5, lr=45)
    make_capture(HERE / "kwnu-2027-method.png", KW, 24, "3. 전형방법", ("after", "수능최저학력기준: 미적용"),
                 U, f"{LBL} 22쪽(PDF 24쪽)", "1단계 400% 이내(춘천 6명 이상 300%) · 서류 60% + 면접 40%",
                 start_pad=10, end_pad=8, lr=40)
    make_capture(HERE / "kwnu-2027-schedule.png", KW, 5, "학생부종합(미래인재면접전형)", ("after", "개별 통보하지 않음"),
                 U, f"{LBL} 3쪽(PDF 5쪽)", "1단계 11/20(금) 15시 · 면접 11/27(금) · 지역인재 11/28(토)",
                 start_pad=7.5, end_pad=4, lr=45)
    make_capture(HERE / "kwnu-2027-interview.png", KW, 35, "2. 면접평가", "바. 평가요소 및 평가항목",
                 U, f"{LBL} 33쪽(PDF 35쪽)", "입학사정관 2인 · 서류 확인 면접 · 10분 내외 · 학업30 진로50 공동체20",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "kwnu-2027-criteria.png", KW, 35, "바. 평가요소 및 평가항목", ("after", "나누어 주고자"),
                 U, f"{LBL} 33쪽(PDF 35쪽)", "면접 평가항목: 학업 수행 노력 · 탐구력 · 진로 관련 지식 확장 노력 등",
                 start_pad=10, end_pad=10, lr=45, end_idx=-1)
    make_capture(HERE / "kwnu-2027-rules.png", KW, 20, "6. 면접평가 및 실기고사 유의사항", "7. 장애학생",
                 U, f"{LBL} 18쪽(PDF 20쪽)", "대기실 위치·시간 홈페이지 공고 · 수험표·신분증 지참 · 전자기기 불가",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "kwnu-2027-regional.png", KW, 3, "면접평가 방법 변경", "수능최저학력기준 반영방법 변경",
                 U, f"{LBL} 1쪽(PDF 3쪽)", "의예과 지역인재면접: MMI → 학생부 기반 확인 1개 면접실",
                 start_pad=10, end_pad=14, lr=45)
    make_structure(HERE / "structure-kwnu.png", [
        "컴퓨터공학과에 지원한 이유는 2학년 정보 시간에 만든 프로그램을 친구들이 실제로 쓰는 것을 보고 진로를 정했기 때문입니다.",
        "반 친구들의 수행평가 마감일을 알려 주는 프로그램을 만들었는데, 처음에는 날짜를 잘못 입력하면 프로그램이 멈춰서 입력값을 먼저 확인하는 코드를 넣어 고쳤습니다.",
        "고치는 과정에서 프로그램은 쓰는 사람이 실수할 것까지 생각해서 만들어야 한다는 것을 배웠습니다.",
        "컴퓨터공학과에서 자료구조와 알고리즘을 배워, 많은 사람이 오류 없이 쓰는 프로그램을 만들고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kwnu()
