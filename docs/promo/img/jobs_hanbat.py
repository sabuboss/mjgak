# 국립한밭대 학생부종합 지역인재(종합)전형 면접 블로그 글(naver-107) 이미지. python jobs_hanbat.py
# PDF: src/m_국립한밭대학교.pdf (2027학년도 신입생 수시모집요강(최종), 96쪽, 2026-06-01 작성)
#      출처: https://www.hanbat.ac.kr/prog/dataDetail/IPSI1/view.do?detailNo=138 첨부파일
# 인쇄 쪽수 = PDF 쪽수 (PDF 4쪽에 '04' 인쇄).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

HB = pdf("국립한밭대학교")
U, LBL = "국립한밭대학교", "2027학년도 신입생 수시 모집요강"


def jobs_hanbat():
    make_thumb(HERE / "thumb-hanbat.png", "한밭대 면접", line2="지역인재(종합)전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "hanbat-2027-units.png", HB, 27, "6. 학생부종합: 지역인재(종합)전형", "지방대학 및 지역균형인재",
                 U, f"{LBL} 27쪽", "지역인재(종합) 179명 · 충청권 고교 3년 전 과정 이수자",
                 start_pad=10, end_pad=12, lr=30)
    make_capture(HERE / "hanbat-2027-method.png", HB, 28, "3. 전형방법", ("after", "수험표와 신분증을 지참하여야 함"),
                 U, f"{LBL} 28쪽", "1단계 서류 100% 5배수 · 2단계 70 + 면접 30 · 최저 없음",
                 start_pad=10, end_pad=10, lr=30)
    make_capture(HERE / "hanbat-2027-schedule.png", HB, 8, "실기우수자", ("after", "만학도전형(야간)"),
                 U, f"{LBL} 8쪽", "1단계 11/6(금) 15시 이후 · 면접 11/20(금) 유성덕명캠퍼스",
                 start_pad=-12, end_pad=3, lr=30)
    make_capture(HERE / "hanbat-2027-eval.png", HB, 74, "1. 서류평가 기준", ("after", "*해당전형"),
                 U, f"{LBL} 74쪽", "면접 성실 150 · 창조 150 · 인화 100 · 진학 의지 100",
                 start_pad=10, end_pad=10, lr=30, end_idx=-1)
    make_capture(HERE / "hanbat-2027-notice.png", HB, 69, "면접고사 유의사항", ("after", "본교 입학안내 홈페이지에 게시"),
                 U, f"{LBL} 69쪽", "입실시간 이후 입실 불가 · 휴대폰 등 소지 금지",
                 start_pad=12, end_pad=10, lr=30)
    make_capture(HERE / "hanbat-2027-tie.png", HB, 58, "나. (1단계) 1단계 성적 70%", ("after", "모두 선발함"),
                 U, f"{LBL} 58쪽", "2단계 동점자: 서류 → 면접 → 도전적 세계인 → 창조",
                 start_pad=10, end_pad=10, lr=30, end_idx=-1)
    make_capture(HERE / "hanbat-2027-summary.png", HB, 4, "학생부종합(일반)", "실기(일반)",
                 U, f"{LBL} 4쪽", "면접 전형: 지역인재(종합) · 소프트웨어인재 · 야간 등",
                 start_pad=14, end_pad=8, lr=30)
    make_structure(HERE / "structure-hanbat.png", [
        "전자공학과에 지원한 이유는 작은 회로 하나로 생활의 불편을 줄일 수 있다는 것을 학교에서 직접 확인했기 때문입니다.",
        "2학년 물리 시간에 센서를 배운 뒤, 동아리에서 조도 센서로 복도가 어두울 때만 불이 켜지는 장치를 만들었습니다.",
        "처음에는 낮에도 불이 깜빡였는데, 센서 값을 일주일 동안 기록해 켜지는 기준을 다시 정하자 깜빡임이 사라졌습니다.",
        "입학하면 회로와 센서를 기초부터 배워, 산업 현장에서 쓰는 전자 장치를 만드는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_hanbat()
