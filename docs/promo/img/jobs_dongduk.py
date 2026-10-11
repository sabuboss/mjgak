# 동덕여대 동덕창의리더전형 블로그 글 이미지. python jobs_dongduk.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

DD = pdf("동덕여자대학교")
U, LBL = "동덕여자대학교", "2027학년도 수시모집요강"


def jobs_dongduk():
    make_thumb(HERE / "thumb-dd.png", "동덕여대 면접", line2="동덕창의리더전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "dd-2027-cl-units.png", DD, 10, "1. 모집단위별 모집인원", ("after", "합계"),
                 U, f"{LBL} 6쪽(PDF 10쪽)", "동덕창의리더전형 25개 모집단위 255명 · 경영융합학부 33명", start_pad=10, end_pad=10)
    make_capture(HERE / "dd-2027-cl-method.png", DD, 10, "3. 전형요소 및 반영비율", ("after", "서류평가 자료"),
                 U, f"{LBL} 6쪽(PDF 10쪽)", "1단계 서류 100% 3배수(300%) · 2단계 1단계 40% + 면접 60%", start_pad=10, end_pad=10)
    make_capture(HERE / "dd-2027-cl-rule.png", DD, 11, "4. 대학수학능력시험 최저학력기준", "6. 평가방법",
                 U, f"{LBL} 7쪽(PDF 11쪽)", "면접 평균 40점 미만 불합격 · 동점자는 면접 성적 1순위 · 최저는 약학과만", start_pad=10, end_pad=10)
    make_capture(HERE / "dd-2027-cl-schedule.png", DD, 7, "구 분", 201,
                 U, f"{LBL} 3쪽(PDF 7쪽)", "1단계 10월 27일(화) 17:00 · 면접 10월 31일(토)~11월 1일(일)", start_pad=10)
    make_capture(HERE / "dd-2027-cl-result.png", DD, 39, "1. 최초합격자 발표", ("after", "나. 장소"),
                 U, f"{LBL} 35쪽(PDF 39쪽)", "최초합격 11월 17일(화) 17:00 · 약학과는 12월 18일(금) 17:00", start_pad=10, end_pad=10)
    make_capture(HERE / "dd-2027-cl-eval.png", DD, 11, "6. 평가방법", ("after", "협업과 소통능력, 나눔과 배려"),
                 U, f"{LBL} 7쪽(PDF 11쪽)", "2:1 면접 10분 내외 · 학업역량 35 + 진로역량 40 + 공동체역량 25", start_pad=10, end_pad=12, end_idx=-1)
    make_structure(HERE / "structure-dd.png", [
        "경영융합학부에 지원한 이유는 감이 아니라 기록과 데이터로 판단하는 경영을 제대로 배우고 싶어서입니다.",
        "2학년 학급 축제 부스에서 첫날 음료는 남고 간식은 모자라서, 둘째 날에는 첫날의 시간대별 판매 기록을 보고 준비량을 바꿨습니다.",
        "그 결과 남는 재고가 눈에 띄게 줄었고, 판단은 느낌이 아니라 기록에서 나와야 한다는 것을 배웠습니다.",
        "경영융합학부에서 마케팅과 경영 데이터 분석을 배워, 숫자로 근거를 대는 기획자가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dongduk()
