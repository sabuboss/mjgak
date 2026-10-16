# 세종대 학생부종합 세종인재(면접형) 블로그 글 이미지. python jobs_sju.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SJ = pdf("세종대학교")
U, LBL = "세종대학교", "2027학년도 수시모집요강"


def jobs_sju():
    make_thumb(HERE / "thumb-sju.png", "세종대 면접", line2="세종인재(면접형)", line3="예상 질문 7개 총정리")
    make_capture(HERE / "sju-2027-change.png", SJ, 3, "모집인원 변경", 453.5,
                 U, f"{LBL} 3쪽", "세종인재(면접형) 338명 → 364명 · 1단계 전 모집단위 3배수", start_pad=10)
    make_capture(HERE / "sju-2027-units.png", SJ, 13, "모집단위 및 모집인원", "지원자격",
                 U, f"{LBL} 13쪽", "세종인재(면접형) 364명 · 창의소프트학부 두 전공 각 48명", start_pad=10, end_pad=10)
    make_capture(HERE / "sju-2027-method.png", SJ, 13, "지원자격", 760,
                 U, f"{LBL} 13쪽", "수능최저 없음 · 1단계 서류 100% 3배수 · 2단계 1단계 60 + 면접 40", start_pad=10)
    make_capture(HERE / "sju-2027-rule.png", SJ, 14, "선발원칙", "전형일정",
                 U, f"{LBL} 14쪽", "서류·면접 기준 점수 이하 제외 · 2단계 동점자 1순위 1단계 성적", start_pad=10, end_pad=10)
    make_capture(HERE / "sju-2027-schedule.png", SJ, 14, "전형일정", "제출서류",
                 U, f"{LBL} 14쪽", "1단계 11/13(금) 17시 이후 · 면접 11/21(토)·11/22(일)", start_pad=10, end_pad=10)
    make_capture(HERE / "sju-2027-interview.png", SJ, 26, "면접평가 방법", 626,
                 U, f"{LBL} 26쪽", "인문·자연 준비 없이 9분 내외 · 창의소프트 40분 준비 뒤 발표", start_pad=10)
    make_capture(HERE / "sju-2027-eval.png", SJ, 27, "면접평가 요소", 428,
                 U, f"{LBL} 27쪽", "탐구역량 40% · 성장역량 40% · 공동체역량 20%", start_pad=10)
    make_structure(HERE / "structure-sju.png", [
        "호텔관광외식경영학부에 지원한 이유는 손님이 다시 찾아오게 만드는 서비스가 무엇인지 공부하고 싶어서입니다.",
        "2학년 학교 축제에서 반 카페를 운영할 때, 주문이 밀리자 손님들이 줄을 서다 그냥 돌아가는 모습을 봤습니다.",
        "그래서 주문받는 사람과 만드는 사람을 나누고 메뉴판을 줄 앞에 미리 세웠더니, 다음 날에는 기다리다 돌아가는 손님이 눈에 띄게 줄었습니다.",
        "호텔관광외식경영학부에서 서비스 운영과 고객 경험을 배워, 손님의 기다림까지 설계하는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_sju()
