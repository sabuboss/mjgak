# 차의과학대학교 CHA학생부교과·CHA학생부종합 블로그 글 이미지. python jobs_cha.py
# 인쇄 쪽수 = PDF 쪽수 (PDF 1쪽 표지, PDF 2쪽 = 인쇄 2쪽 ~ PDF 37쪽 = 인쇄 37쪽).
# 선행학습 영향평가 보고서(pipeline/raw/cha/2026/)는 재배포 금지 폴더라 캡처하지 않는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_차의과학대학교.pdf")
U, LBL = "차의과학대학교", "2027학년도 수시모집요강"


def jobs_cha():
    make_thumb(HERE / "thumb-cha.png", "차의과대 면접", line2="CHA학생부교과·종합", line3="예상 질문 7개 총정리")
    make_capture(HERE / "cha-2027-kyogwa-method.png", P, 8, "1. 학생부교과(CHA학생부교과전형)", ("after", "*1단계 성적"),
                 U, f"{LBL} 8쪽", "CHA학생부교과 68명 · 1단계 교과 100% 5배수 · 2단계 70 + 면접 30",
                 start_pad=6, end_pad=8, lr=22)
    make_capture(HERE / "cha-2027-schedule.png", P, 6, "2026. 10. 27.(화) 16:00", "2026. 12. 21.(월)",
                 U, f"{LBL} 6쪽", "1단계 교과 10/27 · 종합 11/3 · 면접 10/30~11/1, 11/6~8, 약학 11/28",
                 start_pad=15, end_pad=15, lr=22)
    make_capture(HERE / "cha-2027-kyogwa-interview.png", P, 30, "2. 학생부교과전형 면접평가", ("after", "평가척도"),
                 U, f"{LBL} 30쪽", "교과 면접: 3인 이상 · 10분 내외 · 진로 20 · 인성 40 · 발전가능성 40",
                 start_pad=10, end_pad=10, lr=22)
    make_capture(HERE / "cha-2027-jonghap-method.png", P, 12, "3. 학생부종합(CHA학생부종합전형)", "마. 선발원칙",
                 U, f"{LBL} 12쪽", "CHA학생부종합 186명 · 1단계 서류 100% 3배수 · 2단계 70 + 면접 30",
                 start_pad=10, end_pad=10, lr=22)
    make_capture(HERE / "cha-2027-jonghap-interview.png", P, 27, "3. 학생부종합전형 면접평가", ("after", "평가척도"),
                 U, f"{LBL} 27쪽", "종합 면접: 서류 기반 확인 면접 · 진로 40 · 인성 40 · 발전가능성 20",
                 start_pad=10, end_pad=10, lr=22, end_idx=-1)
    make_capture(HERE / "cha-2027-jonghap-notice.png", P, 26, "1. 학생부종합전형 평가 안내", "2. 학생부종합전형 서류평가",
                 U, f"{LBL} 26쪽", "기재 금지사항·개인정보 암시 답변은 불이익",
                 start_pad=6, end_pad=10, lr=22)
    make_capture(HERE / "cha-2027-rules.png", P, 32, "나. 면접 유의사항", ("after", "합격 또는 입학 이후라도"),
                 U, f"{LBL} 32쪽", "시간 엄수 · 신분증 지참 · 휴대전화 등 전자기기 반입 불가",
                 start_pad=10, end_pad=10, lr=22)
    make_structure(HERE / "structure-cha.png", [
        "간호학을 공부하는 데 장점이 될 제 자질은 상대가 말하지 않은 불편을 먼저 묻는 습관입니다.",
        "생명과학 모둠 실험 때 말이 없던 친구에게 먼저 물어보니, 실험 순서를 놓쳐 따라오지 못하고 있었습니다.",
        "순서를 그림 카드로 나눠 붙였더니 그 친구가 다음 단계를 먼저 준비했고, 묻는 것이 돕는 일의 시작이라는 것을 배웠습니다.",
        "간호대학에서 환자가 말하기 어려운 불편을 알아차리는 의사소통을 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_cha()
