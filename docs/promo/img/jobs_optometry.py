# 안경광학과 학과 글(naver-95) 이미지. python jobs_optometry.py
# 쪽수: 서울과기대 인쇄 쪽 = PDF 쪽 - 4 (PDF 30쪽 상단 '26'), 을지대 인쇄 = PDF (PDF 17쪽 '17'),
#       백석대 인쇄 = PDF - 2 (PDF 20쪽 '- 18 -'), 신한대 인쇄 = PDF - 2 (PDF 26쪽 '- 24 -', 캡처 없음).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"


def jobs_optometry():
    make_thumb(HERE / "thumb-optometry.png", "안경광학과")
    # 서울과기대 학교생활우수자: 전형방법(3배수, 70+30) · 면접 평가요소(35·40·25) · 블라인드·교복 금지
    make_capture(HERE / "seoultech-2027-optometry-method.png", pdf("서울과학기술대학교"), 30, "■ 전형방법", ("after", "교복 착용 금지"),
                 "서울과학기술대학교", f"{LBL} 26쪽(PDF 30쪽)", "1단계 서류 100% 3배수 · 2단계 70% + 면접 30% · 최저 없음",
                 start_pad=10, end_pad=10)
    # 을지대 EU면접형: 4배수 · 70+30 · 11/21 · 서류기반 일반면접 · 평가항목
    make_capture(HERE / "eulji-2027-optometry-interview.png", pdf("을지대학교"), 17, "1. EU면접형", ("after", "제출서류 진위여부"),
                 "을지대학교", f"{LBL} 17쪽", "EU면접형 · 1단계 4배수 · 70% + 면접 30% · 11월 21일(토)",
                 start_pad=12, end_pad=8)
    # 을지대 전년도 면접 문항: 첫 문항부터 '눈과 안경렌즈 위치' 문항까지
    make_capture(HERE / "eulji-2027-optometry-questions.png", pdf("을지대학교"), 18, "라. 전년도(2026학년도) 면접문항 예시", ("after", "시야의 왜곡"),
                 "을지대학교", f"{LBL} 18쪽", "전년도(2026학년도) 실제 면접 문항 공개(일부)",
                 start_pad=10, end_pad=4)
    # 백석대 백석인재 면접고사: 고사일정(안경광학과) · 평가영역 40·30·30 · 2대1 5분 내외
    make_capture(HERE / "baekseok-2027-optometry-interview.png", pdf("백석대학교"), 20, "라. 면접고사", "4) 유의사항",
                 "백석대학교", f"{LBL} 18쪽(PDF 20쪽)", "백석인재 면접 · 인·적성 문제 · 2대1 5분 내외 · 10월 15일(종료)",
                 end_pad=8)
    make_structure(HERE / "structure-optometry.png", [
        "안경사는 약제를 쓰지 않는 굴절검사로 눈에 맞는 교정을 책임지는 사람이라고 생각해서 지원했습니다.",
        "중학교 2학년 때 처음 안경을 맞추러 갔는데, 칠판 글씨가 번진다고 하자 안경사 선생님이 검사를 몇 번 더 하고 생활 습관까지 물어보셨습니다.",
        "찾아보니 안경사는 안경 조제·판매, 콘택트렌즈 판매, 약제를 쓰지 않는 굴절검사를 맡는다는 것을 알았고, 검사가 정확해야 맞는 교정이 나온다는 것을 배웠습니다.",
        "안경광학과에 입학하면 굴절검사의 원리부터 정확하게 배워, 손님의 눈을 꼼꼼히 확인하는 안경사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_optometry()
