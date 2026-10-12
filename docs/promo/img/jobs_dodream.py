# 동국대 학생부종합 Do Dream전형 블로그 글 이미지. python jobs_dodream.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

DG = pdf("동국대학교")
U, LBL = "동국대학교", "2027학년도 수시모집요강"


def jobs_dodream():
    make_thumb(HERE / "thumb-dodream.png", "동국대 면접", line2="Do Dream전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "dongguk-2027-dodream-units.png", DG, 18, "모집인원 : 655명", ("after", "영화영상학과"),
                 U, f"{LBL} 16쪽(PDF 18쪽)", "Do Dream전형 49개 모집단위 655명 · 경영대학 65명, 컴퓨터·AI학부 64명", start_pad=10, end_pad=8)
    make_capture(HERE / "dongguk-2027-dodream-method.png", DG, 18, "전형방법", 752,
                 U, f"{LBL} 16쪽(PDF 18쪽)", "1단계 서류 100% · 2단계 1단계 70% + 면접 30% · 수능최저 미적용", start_pad=12)
    make_capture(HERE / "dongguk-2027-dodream-rule.png", DG, 19, "선발원칙 및 동점자", ("after", "인성 및 사회성> 항목"),
                 U, f"{LBL} 17쪽(PDF 19쪽)", "면접 결시·면접 점수 일정 수준 이하는 불합격 · 동점자는 면접 순", start_pad=12, end_pad=8)
    make_capture(HERE / "dongguk-2027-dodream-schedule.png", DG, 20, "전형일정", 614,
                 U, f"{LBL} 18쪽(PDF 20쪽)", "1단계 11/13 · 2단계 전형료 11/16 16:00까지 · 면접 12/11~13", start_pad=12)
    make_capture(HERE / "dongguk-2027-dodream-dates.png", DG, 21, "면접일정", ("after", "사회복지학과"),
                 U, f"{LBL} 19쪽(PDF 21쪽)", "모집단위별 면접일 지정 · 오전 / 오후Ⅰ / 오후Ⅱ · 변경 불가", start_pad=3, end_pad=8)
    make_capture(HERE / "dongguk-2027-dodream-items.png", DG, 84, "평가방법", ("after", "등을 종합적으로 평가"),
                 U, f"{LBL} 82쪽(PDF 84쪽)", "Do Dream 2인 1조 10분 내외 · 학생부 기반 질의응답 4개 항목", start_pad=10, end_pad=8, end_idx=-1)
    make_capture(HERE / "dongguk-2027-dodream-interview.png", DG, 85, "전형별 평가기준(배점)", ("after", "변경 불가"),
                 U, f"{LBL} 83쪽(PDF 85쪽)", "배점 20·30·30·20 · 블라인드 · 교복·체육복 금지 · 언급 불이익", start_pad=10, end_pad=2)
    make_structure(HERE / "structure-dodream.png", [
        "경제학과에 지원한 이유는 가격이 사람들의 선택을 어떻게 바꾸는지 자료로 확인하는 공부를 하고 싶어서입니다.",
        "2학년 경제 수업에서 학교 매점의 음료 할인 전후 판매량을 2주씩 기록했는데, 할인한 음료가 늘어난 만큼 다른 음료가 줄어 있었습니다.",
        "판매량이 늘었다는 숫자만 보면 안 되고, 어디서 옮겨 온 수요인지까지 봐야 한다는 것을 배웠습니다.",
        "동국대 경제학과에서 미시경제학과 계량경제학을 배워, 정책이나 가격 변화의 효과를 자료로 따지는 연습을 하고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dodream()
