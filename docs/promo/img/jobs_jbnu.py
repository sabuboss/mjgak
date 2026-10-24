# 전북대 학생부종합 큰사람전형(지역인재1·2유형 비교) 블로그 글(naver-88) 이미지. python jobs_jbnu.py
# 전북대 PDF(138쪽)는 인쇄 쪽수 = PDF 쪽수 (PDF 3쪽 = 인쇄 3, PDF 16·17·19·20·21·97쪽에서도 같음 확인).
# 기존 jbnu-2027-voc-* (naver-45 특성화고 글) 와 겹치지 않게 kps(큰사람) 를 붙인다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_전북대학교.pdf")
U, LBL = "전북대학교", "2027학년도 수시모집요강"


def jobs_jbnu():
    make_thumb(HERE / "thumb-jbnu.png", "전북대 면접", line2="큰사람전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "jbnu-2027-kps-summary.png", P, 8, "전형 개요", ("after", "학생부종합"),
                 U, f"{LBL} 8쪽", "큰사람 524명 · 지역인재1유형 107명 · 2유형 6명 · 1단계 3배수",
                 start_pad=10, end_pad=1, lr=40)
    make_capture(HERE / "jbnu-2027-kps-method.png", P, 17, "가. 전형 방법", ("after", "학교폭력 가해학생 조치사항 반영"),
                 U, f"{LBL} 17쪽", "1단계 서류 100% 3배수 · 2단계 1단계 800점 + 면접 200점",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "jbnu-2027-kps-schedule.png", P, 16, "1단계 합격자발표", 492.5,
                 U, f"{LBL} 16쪽", "1단계 11/20(금) 14:00 · 면접 11/26(목)·11/28(토) · 합격 12/18",
                 start_pad=4, end_pad=0, lr=40)
    make_capture(HERE / "jbnu-2027-kps-interview.png", P, 19, "나. 면접", ("after", "학업계획의 구체성 및 실현가능성"),
                 U, f"{LBL} 19쪽", "면접위원 3인 · 10분 내외 · 블라인드 · 공동체 30% · 진로 70%",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "jbnu-2027-kps-rules.png", P, 20, "면접당일 개인정보를", ("after", "8순위: 학생부 교과 성적이 높은 자"),
                 U, f"{LBL} 20쪽", "교복 금지 · 인적사항 언급 금지 · 2단계 동점자는 면접 점수 먼저",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "jbnu-2027-kps-minimum.png", P, 21, "수능최저학력기준 적용", ("after", "간호대학 간호학과의 경우 탐구영역"),
                 U, f"{LBL} 21쪽", "최저는 간호·수의예·약학·의예·치의예만 · 그 외 모집단위 없음",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "jbnu-2027-kps-local.png", P, 10, "2. 수시 학생부종합전형 지역인재1유형", ("after", "융합자율전공학부2"),
                 U, f"{LBL} 10쪽", "지역인재1유형 107명 · 2유형 6명(수의예과 2 · 의예과 4) 신설",
                 start_pad=10, end_pad=3, lr=40)
    make_structure(HERE / "structure-jbnu.png", [
        "공학계열1을 고른 이유는 움직이는 장치가 왜 멈추는지 끝까지 확인해 보고 싶었기 때문입니다.",
        "2학년 과학 동아리에서 고무줄 동력 자동차를 만들 때, 바퀴가 자꾸 헛돌아 3미터도 못 갔습니다.",
        "바퀴에 고무 밴드를 감고 축을 짧게 바꾸며 다섯 번 다시 달려 보니, 이동 거리가 두 배 가까이 늘었습니다.",
        "입학하면 동역학을 배워, 그때 감으로 바꾼 것을 계산으로 설명해 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_jbnu()
