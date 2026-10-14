# 명지대 학생부종합 명지인재면접전형 블로그 글 이미지. python jobs_mju.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

MJU = pdf("명지대학교")
U, LBL = "명지대학교", "2027학년도 수시모집요강"


def jobs_mju():
    make_thumb(HERE / "thumb-mju.png", "명지대 면접", line2="명지인재면접전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "mju-2027-int-units.png", MJU, 49, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 47쪽(PDF 49쪽)", "379명 · 인문캠퍼스(서울) 203명 · 자연캠퍼스(용인) 176명", start_pad=4, end_pad=8)
    make_capture(HERE / "mju-2027-int-method.png", MJU, 50, "4. 전형방법", "라. 서류평가",
                 U, f"{LBL} 48쪽(PDF 50쪽)", "1단계 서류 100% 4배수 · 2단계 1단계 성적 70 + 면접 30 · 최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "mju-2027-int-rule.png", MJU, 51, "바. 선발원칙 및 동점자 처리기준", "5. 제출서류",
                 U, f"{LBL} 49쪽(PDF 51쪽)", "면접 결시자는 선발 제외 · 2단계 동점자 1·2순위는 면접 성적", start_pad=10, end_pad=10)
    make_capture(HERE / "mju-2027-int-schedule.png", MJU, 49, "3. 전형일정", ("after", "전형일정 상세내용은 p. 10 참조"),
                 U, f"{LBL} 47쪽(PDF 49쪽)", "1단계 11/20(금) 15시 · 면접 자연 11/28 · 인문 11/29 · 모두 서울", start_pad=10, end_pad=8)
    make_capture(HERE / "mju-2027-int-interview.png", MJU, 50, "마. 면접고사", ("after", "pp. 84~86 참조"),
                 U, f"{LBL} 48쪽(PDF 50쪽)", "면접위원 2명 개별면접 · 약 10분 · 제출서류 기반 심층면접", start_pad=10, end_pad=8)
    make_capture(HERE / "mju-2027-int-eval.png", MJU, 86, "2. 면접평가", ("after", "해결책을 가지고 극복하고자"),
                 U, f"{LBL} 84쪽(PDF 86쪽)", "공동체역량 30 · 진로역량 40 · 발전가능성 30 · 6등급 평가", start_pad=10, end_pad=8)
    make_capture(HERE / "mju-2027-int-blind.png", MJU, 88, "2. 블라인드 면접 유의사항", ("after", "무역업에 종사하는"),
                 U, f"{LBL} 86쪽(PDF 88쪽)", "교복 착용 금지 · 가번호 · 부모 직업 답변 금지 · 녹화·녹음 가능", start_pad=10, end_pad=10)
    make_structure(HERE / "structure-mju.png", [
        "문헌정보학전공에 지원한 이유는 필요한 정보를 필요한 사람에게 찾기 쉽게 이어 주는 일을 하고 싶어서입니다.",
        "1학년 때 도서부에서 대출 기록을 정리하다가, 같은 책이 분류 번호 때문에 엉뚱한 서가에 꽂혀 거의 대출되지 않는 것을 봤습니다.",
        "2학년 때 한국십진분류법을 공부해 사서 선생님과 주제별 책 위치 안내판을 만들며, 정보는 찾을 수 있어야 쓰인다는 것을 배웠습니다.",
        "명지대 문헌정보학전공에서 정보조직과 이용자 서비스를 배워, 이용자가 길을 잃지 않는 도서관을 만들고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_mju()
