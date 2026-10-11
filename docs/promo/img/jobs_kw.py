# 광운대 참빛인재Ⅰ(면접형) 블로그 글 이미지. python jobs_kw.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KW = pdf("광운대학교")
U, LBL = "광운대학교", "2027학년도 수시모집요강"


def jobs_kw():
    make_thumb(HERE / "thumb-kw.png", "광운대 면접", line2="참빛인재Ⅰ 면접형", line3="예상 질문 6개 총정리")
    make_capture(HERE / "kw-2027-cb-units.png", KW, 19, "1. 모집단위 및 모집인원", ("after", "총계"),
                 U, f"{LBL} 19쪽", "광운참빛인재전형Ⅰ(면접형) 25개 모집단위 250명 · 수능최저 없음", start_pad=10, end_pad=16)
    make_capture(HERE / "kw-2027-cb-method.png", KW, 19, "3. 전형방법", ("after", "400점/0점"),
                 U, f"{LBL} 19쪽", "1단계 서류 100%로 3.5배수(350%) · 2단계 1단계 60% + 면접 40%", start_pad=10, end_pad=10)
    make_capture(HERE / "kw-2027-cb-rule.png", KW, 20, "4. 선발원칙", "5. 제출서류",
                 U, f"{LBL} 20쪽", "면접 결시는 불합격 · 최종 동점자는 면접 성적이 1순위", start_pad=10, end_pad=8)
    make_capture(HERE / "kw-2027-cb-schedule.png", KW, 18, "1단계 합격자발표", ("after", "공고함"),
                 U, f"{LBL} 18쪽", "1단계 10월 28일(수) 15:00 · 면접 10월 31일(토) 또는 11월 1일(일) · 장소·시간은 3일 전 공고", start_pad=1, end_pad=3)
    make_capture(HERE / "kw-2027-cb-dates.png", KW, 21, "6. 모집단위별 면접 일자", ("after", "국제통상학부"),
                 U, f"{LBL} 21쪽", "자연계열 10/31(토) · 인문계열 11/1(일) · [*] 표시 학과는 양일 중 하루 배정", start_pad=10, end_pad=10)
    make_capture(HERE / "kw-2027-cb-interview.png", KW, 46, "2. 면접평가 안내", ("after", "면접 태도"),
                 U, f"{LBL} 46쪽", "2인 개별 대면 10분 이내 · 문제 제시형 없음 · 발전가능성 45 + 종합적사고력 30 + 인성 25", start_pad=10, end_pad=12)
    make_structure(HERE / "structure-kw.png", [
        "전자공학과에 지원한 이유는 센서가 측정한 값을 회로가 어떻게 숫자로 바꾸는지 직접 확인해 보고 싶어서입니다.",
        "2학년 물리 탐구에서 온도 센서로 교실 온도를 기록했는데, 값이 계속 튀어서 원인을 찾다 보니 신호에 섞인 잡음 때문이라는 것을 알았습니다.",
        "측정값 하나도 회로 설계에 따라 믿을 수 있는 숫자가 되기도 하고 아니기도 하다는 것을 배웠고, 그때부터 아날로그 회로에 관심이 생겼습니다.",
        "광운대 전자공학과에서 전자회로와 신호처리를 배워, 정확하게 측정하는 센서 회로를 설계하는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kw()
