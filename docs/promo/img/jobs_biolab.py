# 임상병리학과 학과 글(naver-85) 이미지. python jobs_biolab.py
# 쪽수: 남서울대·을지대·청주대 모두 인쇄 쪽수 = PDF 쪽수 (남서울 '- 33 -', 을지 '17', 청주 '- 18 -' 확인).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"


def jobs_biolab():
    make_thumb(HERE / "thumb-biolab.png", "임상병리학과")
    # 남서울대 학생부종합 면접형: 전형방법·모집인원(임상병리 4명)·지원자격(최저 없음)
    make_capture(HERE / "namseoul-2027-biolab-method.png", pdf("남서울대학교"), 33, "학생부종합 면접형", 470,
                 "남서울대학교", f"{LBL} 33쪽", "학종 면접형 임상병리학과 4명 · 1단계 6배수 · 70% + 면접 30%",
                 start_pad=10, lr=30)
    # 남서울대 면접평가: 공동체역량 40 · 진로역량 60 · 2대1 10분 내외
    make_capture(HERE / "namseoul-2027-biolab-interview.png", pdf("남서울대학교"), 37, "면접평가", "면접고사 유의사항",
                 "남서울대학교", f"{LBL} 37쪽", "공개 5문항 중 당일 2문항 + 학생부 기반 · 2대1 10분 내외",
                 start_pad=10, end_pad=1, lr=30)
    # 을지대 EU면접형: 전형방법·면접일·평가항목
    make_capture(HERE / "eulji-2027-biolab-interview.png", pdf("을지대학교"), 17, "1. EU면접형", ("after", "제출서류 진위여부"),
                 "을지대학교", f"{LBL} 17쪽", "EU면접형 · 1단계 4배수 · 70% + 면접 30% · 11월 21일(토)",
                 start_pad=12, end_pad=8)
    # 을지대 전년도 면접 문항: 첫 문항부터 '비예기항체' 문항까지
    make_capture(HERE / "eulji-2027-biolab-questions.png", pdf("을지대학교"), 18, "라. 전년도(2026학년도) 면접문항 예시", ("after", "비예기항체"),
                 "을지대학교", f"{LBL} 18쪽", "전년도(2026학년도) 실제 면접 문항 공개(일부)",
                 start_pad=10, end_pad=4)
    # 청주대 교과면접전형: 반영비율·평가영역
    make_capture(HERE / "cheongju-2027-biolab-interview.png", pdf("청주대학교"), 18, "4. 교과면접전형", "5) 항공서비스학과 면접고사 반영 및 평가내용",
                 "청주대학교", f"{LBL} 18쪽", "교과면접전형 · 교과 70% + 면접 30%",
                 start_pad=12, end_pad=8)
    make_structure(HERE / "structure-biolab.png", [
        "임상병리사는 의사가 진단하기 전에 몸속 상태를 숫자로 보여 주는 사람이라고 생각해서 지원했습니다.",
        "할머니 건강검진 결과지에서 혈당 수치 하나 때문에 재검사를 받으셨는데, 그 숫자를 만든 사람이 임상병리사라는 것을 알게 됐습니다.",
        "검사 결과 하나가 치료 방향을 바꾸기 때문에, 검체 확인과 기록을 정확히 하는 일이 환자 안전과 바로 이어진다는 것을 배웠습니다.",
        "임상병리학과에서 진단검사의 원리와 정도관리를 제대로 배워, 믿을 수 있는 결과를 내는 임상병리사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_biolab()
