# 울산대 학생부종합 잠재역량 특별전형 면접 블로그 글(naver-100) 이미지. python jobs_ulsan.py
# PDF: src/m_울산대학교.pdf (src/ulsan.pdf 와 같은 파일, 2027학년도 수시모집 신입생 모집요강, 55쪽).
# 인쇄 쪽수 = PDF 쪽수 (표지 1쪽부터 같은 번호).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

US = pdf("울산대학교")
U, LBL = "울산대학교", "2027학년도 수시모집 신입생 모집요강"


def jobs_ulsan():
    make_thumb(HERE / "thumb-ulsan.png", "울산대 면접", line2="잠재역량전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "ulsan-2027-jamjae-units.png", US, 24, "1. 모집인원", ("after", "2. 지원자격"),
                 U, f"{LBL} 24쪽", "잠재역량 428명 · 면접은 자율전공 20 · 간호 18 · 의예 10",
                 start_pad=4, end_pad=8, lr=30)
    make_capture(HERE / "ulsan-2027-jamjae-method.png", US, 24, "4. 전형방법", ("after", "기준 점수 이하인 경우"),
                 U, f"{LBL} 24쪽", "자율·간호 1단계 4배수 · 서류 50 + 면접 50 · 최저 없음",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "ulsan-2027-jamjae-schedule.png", US, 6, "구분", "일반교과(디자인융합학부",
                 U, f"{LBL} 6쪽", "1단계 11/20(금) 16시 예정 · 면접 11/28(토) · 의예 12/5(토)",
                 start_pad=10, end_pad=5, lr=30)
    make_capture(HERE / "ulsan-2027-jamjae-date.png", US, 42, "학생부종합형 면접고사", ("after", "수험표 출력 시 안내"),
                 U, f"{LBL} 42쪽", "수험표 출력 11/25(수) 17시 · 의예 12/2(수) 17시 · 오전·오후반",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "ulsan-2027-jamjae-interview.png", US, 42, "2. 평가영역 및 배점", ("after", "입실하지 않은 경우"),
                 U, f"{LBL} 42쪽", "다대일 개인별 종합면접 10분 이내 · 500점 · 지각 0점",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "ulsan-2027-multi.png", US, 3, "복수지원 안내", ("after", "특성화고교졸업자 ②지역교과 전형 간 중복지원 불가"),
                 U, f"{LBL} 3쪽", "전형별 1회씩 6회 안 · 의예과는 지역교과·지역인재·지역의사제 중복 불가",
                 start_pad=10, end_pad=3, lr=45)
    make_capture(HERE / "ulsan-2027-med-local.png", US, 41, "지역교과(의예과) 면접고사", ("after", "15분 내외"),
                 U, f"{LBL} 41쪽", "지역교과 의예과 11/21(토) · 다대일 다면평가 · 15분 내외 · 200점",
                 start_pad=14, end_pad=20, lr=45)
    make_structure(HERE / "structure-ulsan.png", [
        "간호학과에 지원한 이유는 건강 정보를 상대가 실제로 따라 할 수 있게 전하는 일이 간호의 중요한 부분이라는 것을 학교에서 확인했기 때문입니다.",
        "2학년 보건 동아리에서 손 씻기 캠페인을 했는데, 글자로만 된 안내문을 붙였을 때는 30초 넘게 손을 씻는 친구가 열 명 중 두 명뿐이었습니다.",
        "손 씻기 여섯 단계를 그림으로 바꾸고 30초 노래에 맞추자 열 명 중 여섯 명으로 늘었고, 전하는 방식에 따라 행동이 달라진다는 것을 배웠습니다.",
        "간호학과에서 환자 교육을 제대로 배워, 퇴원한 뒤에도 환자가 스스로 건강을 관리하도록 돕는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_ulsan()
