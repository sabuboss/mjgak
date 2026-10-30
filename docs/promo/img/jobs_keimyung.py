# 계명대 학생부교과(면접전형) 블로그 글(naver-101) 이미지. python jobs_keimyung.py
# PDF: 계명대 입학처(www.gokmu.ac.kr) 2027학년도 신입생 수시모집요강. 인쇄 쪽수 = PDF 쪽수.
# 약자 keimyung: img/ 의 kmu 파일은 국민대(naver-61) 것이라 겹치지 않게 했다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KM = pdf("계명대학교")
U, LBL = "계명대학교", "2027학년도 신입생 수시모집요강"


def jobs_keimyung():
    make_thumb(HERE / "thumb-keimyung.png", "계명대 면접", line2="교과 면접전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "keimyung-2027-summary.png", KM, 6, "전형요약표", "지원자격 및 제출서류",
                 U, f"{LBL} 6쪽", "면접전형 393명 · 1단계 학생부 20배수 · 2단계 1단계 70% + 면접 30%",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "keimyung-2027-method.png", KM, 21, "학생부교과(면접전형)", ("after", "교과 성적 80% + 출결 20%"),
                 U, f"{LBL} 21쪽", "393명 · 20배수 · 수능최저 충족자 중 1단계 70% + 면접 30%",
                 start_pad=10, end_pad=8, lr=40)
    make_capture(HERE / "keimyung-2027-change.png", KM, 7, "학생부교과(일반, 지역, 지역기회균형, 면접전형)",
                 ("after", "문예창작학과 면접전형"),
                 U, f"{LBL} 7쪽", "10배수 → 20배수 · 면접 20% → 30% · 모집단위 29개 → 56개",
                 start_pad=10, end_pad=8, lr=40)
    make_capture(HERE / "keimyung-2027-schedule.png", KM, 15, "전형일정 안내", ("after", "충원 합격자의 차수별"),
                 U, f"{LBL} 15쪽", "면접전형 1단계 11/14(토) · 면접 12/5(토) · 합격 12/18(금)",
                 start_pad=10, end_pad=8, lr=40, start_idx=1)
    make_capture(HERE / "keimyung-2027-notice.png", KM, 14, "입학원서의 작성오류", 771.5,
                 U, f"{LBL} 14쪽", "면접 결시자 불합격 · 오전·오후 분반 · 개인별 일자·시간 변경 불가",
                 start_pad=5, end_pad=5, lr=40)
    make_capture(HERE / "keimyung-2027-interview.png", KM, 21, "면접 평가 요소 및 항목", 541,
                 U, f"{LBL} 21쪽", "면접위원 2명 · 10분 내외 · 기본·학업·사고력·종합평가",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "keimyung-2027-minimum.png", KM, 21, "수능 최저학력기준", "제출서류",
                 U, f"{LBL} 21쪽", "기본 2개 영역 합 12 · 간호·경찰행정 합 8 · 문예창작 없음",
                 start_pad=10, end_pad=10, lr=40, start_idx=1)
    make_structure(HERE / "structure-keimyung.png", [
        "간호학과에 지원한 이유는 아픈 사람의 작은 변화를 먼저 알아채는 일이 돌봄의 시작이라는 것을 직접 봤기 때문입니다.",
        "2학년 체육대회 날, 더위에 어지러워하는 친구와 보건실에 갔고, 보건 선생님은 체온과 맥박을 잰 뒤 친구의 얼굴색을 계속 살피셨습니다.",
        "그 모습을 보고 관찰이 곧 돌봄이라는 것을 알았습니다.",
        "간호학과에서 건강 상태를 정확히 살피는 방법을 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_keimyung()
