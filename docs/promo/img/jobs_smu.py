# 상명대 학생부종합 상명인재전형(면접 모집단위) 블로그 글 이미지. python jobs_smu.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SE = pdf("상명대학교")          # 서울캠퍼스 (인쇄 쪽 = PDF 쪽 - 2)
CA = pdf("상명대학교(천안)")    # 천안캠퍼스 (인쇄 쪽 = PDF 쪽 - 3)
US, UC = "상명대학교 서울캠퍼스", "상명대학교 천안캠퍼스"
LS = LC = "2027학년도 수시모집요강"


def jobs_smu():
    make_thumb(HERE / "thumb-smu.png", "상명대 면접", line2="상명인재전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "smu-2027-talent-seoul-units.png", SE, 17, "2. 학생부종합(상명인재전형)", ("after", "1단계 성적"),
                 US, f"{LS} 15쪽(PDF 17쪽)", "면접은 스포츠건강관리 7 · 조형예술 9 · 5배수 → 60 + 면접 40",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "smu-2027-talent-cheonan-units.png", CA, 14, "2. 학생부종합(상명인재전형)", ("after", "면접고사 기간은 단축될 수 있음"),
                 UC, f"{LC} 11쪽(PDF 14쪽)", "예체능계(AR·VR·문화예술경영 제외) 면접 · 11/7~8",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "smu-2027-talent-tie.png", SE, 18, "아. 동점자 처리기준", "3. 학생부종합(기회균형전형)",
                 US, f"{LS} 16쪽(PDF 18쪽)", "2단계 동점자는 면접 총점 → 진로 → 공동체 → 학업 순",
                 start_pad=4, end_pad=8)
    make_capture(HERE / "smu-2027-talent-seoul-schedule.png", SE, 9, "1단계 통과자 발표", 656,
                 US, f"{LS} 7쪽(PDF 9쪽)", "1단계 발표 10/30(금) 14:00 · 면접평가 11/7(토)",
                 start_pad=6)
    make_capture(HERE / "smu-2027-talent-cheonan-schedule.png", CA, 8, "고사시행 안내", 533,
                 UC, f"{LC} 5쪽(PDF 8쪽)", "1단계 발표 10/29(목) 14:00 · 면접고사 11/7(토)~8(일)",
                 start_pad=12)
    make_capture(HERE / "smu-2027-talent-interview.png", SE, 35, "2. 면접평가", ("after", "공감과 수용"),
                 US, f"{LS} 33쪽(PDF 35쪽)", "면접위원 2인 개별면접 10분 내외 · 학업 20 · 진로 50 · 공동체 30",
                 start_pad=10, end_pad=12)
    make_capture(HERE / "smu-2027-talent-exam-rules.png", SE, 39, "5. 고사 유의사항", "6. 선발기준",
                 US, f"{LS} 37쪽(PDF 39쪽)", "수험표 + 사진 있는 신분증(폰 속 신분증 사진 불가)",
                 start_pad=10, end_pad=8)
    make_structure(HERE / "structure-smu.png", [
        "스포츠건강관리전공에 지원한 이유는 운동을 처음 시작하는 사람이 다치지 않고 꾸준히 하도록 돕는 방법을 배우고 싶어서입니다.",
        "2학년 체육 시간에 줄넘기 기록 측정을 도우면서, 준비운동을 건너뛴 친구들이 발목을 자주 접질린다는 것을 봤습니다.",
        "그 뒤로 체육부장으로서 수업 전 5분 스트레칭 순서를 만들어 친구들과 같이 했고, 한 학기 동안 다친 친구가 눈에 띄게 줄었습니다.",
        "스포츠건강관리전공에서 운동처방과 운동생리학을 배워, 생활체육 현장에서 운동 프로그램을 짜는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_smu()
