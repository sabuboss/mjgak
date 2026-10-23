# 인천대 학생부종합 자기추천전형 블로그 글 이미지. python jobs_incheon.py
# 인천대 PDF: 인쇄 쪽수 = PDF 쪽수 (PDF 3쪽 = 인쇄 3쪽 ~ PDF 51쪽 = 인쇄 51쪽 확인).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_인천대학교.pdf")
U, LBL = "인천대학교", "2027학년도 수시모집요강"


def jobs_incheon():
    make_thumb(HERE / "thumb-incheon.png", "인천대 면접", line2="자기추천전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "incheon-2027-units.png", P, 20, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 20쪽", "자기추천 694명 · 기계공학과 31명 · 컴퓨터공학부 29명 · 전자공학부 28명",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "incheon-2027-method.png", P, 20, "2. 지원자격", ("after", "학교폭력 조치사항 처분별"),
                 U, f"{LBL} 20쪽", "1단계 서류 100% 3배수(사범대·스포츠의학부 4배수) · 2단계 면접 30%",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "incheon-2027-select.png", P, 21, "5. 선발원칙", "6. 전형일정",
                 U, f"{LBL} 21쪽", "면접 미응시자 불합격 · 2단계 동점 시 면접고사 총점 우선",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "incheon-2027-schedule.png", P, 21, "6. 전형일정", ("after", "충원합격자 통보"),
                 U, f"{LBL} 21쪽", "1단계 11/6(금) · 면접시간·장소 11/18(수) · 면접 11/21(토)",
                 start_pad=12, end_pad=14, lr=45)
    make_capture(HERE / "incheon-2027-interview.png", P, 43, "2. 면접평가", ("after", "표현의 정확성"),
                 U, f"{LBL} 43쪽", "2인 개별면접 · 10분 내외 · 진로30 · 발전30 · 공동체20 · 의사소통20",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "incheon-2027-multi.png", P, 6, "3. 복수지원", ("after", "타 대학 면접고사일"),
                 U, f"{LBL} 6쪽", "자기추천·특수교육대상자는 같은 그룹 · 둘 중 1개만 지원",
                 start_pad=12, end_pad=10, lr=45)
    make_structure(HERE / "structure-incheon.png", [
        "기계공학과에 지원한 이유는 작은 부품 하나가 기계 전체의 움직임을 바꾸는 것을 직접 확인했기 때문입니다.",
        "2학년 과학 동아리에서 고무줄 동력 자동차를 만들 때, 바퀴 축의 기어를 큰 것에서 작은 것으로 바꿔 가며 달린 거리를 쟀습니다.",
        "기어 크기만 바꿔도 거리와 속도가 서로 반대로 움직이는 것을 보고, 설계는 무엇을 얻고 무엇을 포기할지 정하는 일이라는 걸 알았습니다.",
        "입학하면 1학년 때 역학 기초를 탄탄히 다지고, 설계 과목에서 동력 전달 장치를 직접 만들어 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_incheon()
