# 국민대 학생부종합 국민프런티어전형 블로그 글 이미지. python jobs_kmu.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KMU = pdf("국민대학교")
U, LBL = "국민대학교", "2027학년도 수시모집요강"


def jobs_kmu():
    make_thumb(HERE / "thumb-kmu.png", "국민대 면접", line2="국민프런티어", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kmu-2027-units.png", KMU, 4, "[ 전형별 모집인원 및 지원자격 요약 ]", 268,
                 U, f"{LBL} 2쪽(PDF 4쪽)", "국민프런티어 724명 · 수능최저 없음 · 검정고시·국외고 지원 가능", start_pad=10)
    make_capture(HERE / "kmu-2027-method.png", KMU, 19, "3. 수능최저학력기준", "5. 선발기준",
                 U, f"{LBL} 17쪽(PDF 19쪽)", "1단계 서류 100% 3배수 · 2단계 1단계 70% + 면접 30% · 수능최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "kmu-2027-rule.png", KMU, 19, "5. 선발기준", ("after", "리더십 점수 상위자"),
                 U, f"{LBL} 17쪽(PDF 19쪽)", "결시·면접 F 판정은 불합격 · 2단계 동점자 1~3순위는 면접", start_pad=10, end_pad=8)
    make_capture(HERE / "kmu-2027-schedule.png", KMU, 12, "2. 전형일정", 300,
                 U, f"{LBL} 10쪽(PDF 12쪽)", "1단계 11/17(화) 14시 예정 · 면접 자연계 11/21(토) · 인문·예체능계 11/22(일)", start_pad=10)
    make_capture(HERE / "kmu-2027-exam.png", KMU, 72, "4. 면접/실기고사 및 논술고사 관련 사항", "라. 시각",
                 U, f"{LBL} 70쪽(PDF 72쪽)", "개별 통보 없음 · 지정 일시 변경 불가 · 시작 후 도착 시 입실 불가", start_pad=10, end_pad=4)
    make_capture(HERE / "kmu-2027-interview.png", KMU, 17, "나. 면접평가", ("after", "협업과 소통 능력"),
                 U, f"{LBL} 15쪽(PDF 17쪽)", "2:1 개별 블라인드 10분 이내 · 진로 40 · 학업 30 · 공동체 30", start_pad=10, end_pad=10)
    make_capture(HERE / "kmu-2027-blind.png", KMU, 17, "1. 공통사항", ("after", "착용할 수 없음"),
                 U, f"{LBL} 15쪽(PDF 17쪽)", "학생부 블라인드 평가 · 면접 때 교복·교표 등 착용 불가", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-kmu.png", [
        "경영학부에 지원한 이유는 작은 가게도 숫자를 보고 결정하면 결과가 달라진다는 것을 직접 확인했기 때문입니다.",
        "2학년 경제 수업에서 수요와 가격의 관계를 배운 뒤, 학교 축제 때 우리 반 음료 부스의 가격을 두 가지로 정해 시간대별 판매량을 기록했습니다.",
        "가격을 조금 내린 시간대에 전체 매출이 오히려 늘었고, 그 뒤로 동아리 행사 예산을 짤 때도 지난 기록부터 찾아보게 됐습니다.",
        "경영학부에서 마케팅과 회계를 배워, 기록을 근거로 결정하는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kmu()
