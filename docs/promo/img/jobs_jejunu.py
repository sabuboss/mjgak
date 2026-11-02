# 제주대 학생부종합(면접 있는 전형) 블로그 글(naver-123) 이미지. python jobs_jejunu.py
# m_제주대학교.pdf: 인쇄 쪽수 = PDF 쪽수 - 5 (PDF 6쪽 = 인쇄 1쪽, PDF 30쪽 = 인쇄 25쪽).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

JJ = str(SRC / "m_제주대학교.pdf")
U, LBL = "제주대학교", "2027학년도 수시모집요강"


def jobs_jejunu():
    make_thumb(HERE / "thumb-jejunu.png", "제주대 면접", line2="학생부종합 면접", line3="예상 질문 7개 총정리")
    make_capture(HERE / "jejunu-2027-units.png", JJ, 9, "수시모집", ("after", "간호학과"),
                 U, f"{LBL} 4쪽(PDF 9쪽)", "학생부종합 일반학생·지역인재 칸 · 초등 9·4 · 수의 2·3 · 간호 7",
                 start_pad=8, end_pad=8, lr=20)
    make_capture(HERE / "jejunu-2027-method.png", JJ, 36, "1. 학생부종합(일반학생)", ("after", "전형총점에 관계없이 불합격 처리"),
                 U, f"{LBL} 31쪽(PDF 36쪽)", "3배수 · 서류 700 + 면접 300 · 면접 150점 미만 불합격",
                 start_pad=10, end_pad=10, lr=30)
    make_capture(HERE / "jejunu-2027-local.png", JJ, 38, "2. 학생부종합(지역인재)", "2) 서류평가 방법",
                 U, f"{LBL} 33쪽(PDF 38쪽)", "지역인재 47명 · 3배수(의예·약학 5배수) · 제주 고교 전 과정",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "jejunu-2027-schedule.png", JJ, 6, "전형일정", ("after", "개별통보 하지 않음"),
                 U, f"{LBL} 1쪽(PDF 6쪽)", "1단계 11/13(금) 10:00 · 면접 12/4(금) · 발표 12/18(금)",
                 start_pad=12, end_pad=3, lr=30, end_idx=1)
    make_capture(HERE / "jejunu-2027-interview.png", JJ, 30, "2) 면접평가", ("after", "부모직업·직장·직위명"),
                 U, f"{LBL} 25쪽(PDF 30쪽)", "15분 내외 개별 블라인드 · 가번호 · 교복·명찰 블라인드",
                 start_pad=3, end_pad=10, lr=30)
    make_capture(HERE / "jejunu-2027-criteria.png", JJ, 32, "나. 일반학생(사범대학", "4. 다수-다단계",
                 U, f"{LBL} 27쪽(PDF 32쪽)", "면접 반영 학업 30% · 진로 30% · 인성·공동체 40%",
                 start_pad=10, end_pad=10, lr=30)
    make_structure(HERE / "structure-jejunu.png", [
        "초등교사가 되려는 이유는 아이가 직접 해 보며 '알겠다'고 말하는 순간을 곁에서 돕고 싶기 때문입니다.",
        "교육 동아리에서 초등학생 과학 체험 부스를 맡았을 때, 원리를 말로 먼저 설명하자 아이들이 금방 자리를 떠났습니다.",
        "풍선 로켓을 먼저 날려 보게 하고 왜 날아갔는지 묻는 순서로 바꾸자, 아이들이 더 오래 머물며 스스로 답을 찾았습니다.",
        "초등교육학부에서 아이의 발달에 맞는 수업 방법을 배워, 배우는 즐거움을 지켜 주는 교사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_jejunu()
