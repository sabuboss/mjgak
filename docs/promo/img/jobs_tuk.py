# 한국공학대 학생부종합 창의인재 블로그 글 이미지. python jobs_tuk.py
# 인쇄 쪽수 = PDF 쪽수 - 2 (PDF 3쪽 = 인쇄 1쪽, PDF 23쪽 = 인쇄 21쪽 확인).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

TU = str(SRC / "m_한국공학대학교.pdf")
U, LBL = "한국공학대학교", "2027학년도 수시모집요강"


def jobs_tuk():
    make_thumb(HERE / "thumb-tuk.png", "한국공학대 면접", line2="학생부종합 창의인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "tuk-2027-units.png", TU, 23, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 21쪽(PDF 23쪽)", "창의인재 256명 · 디자인공학부 22명 · 기계공학과 18명",
                 start_pad=12, end_pad=8, lr=45)
    make_capture(HERE / "tuk-2027-method.png", TU, 23, "2. 지원자격", ("after", "100%(500점)"),
                 U, f"{LBL} 21쪽(PDF 23쪽)", "1단계 서류 100% 4배수 · 2단계 1단계 60% + 면접 40% · 최저 없음",
                 start_pad=10, end_pad=10, lr=45, end_idx=-1)
    make_capture(HERE / "tuk-2027-schedule.png", TU, 7, "구분", "최초합격자",
                 U, f"{LBL} 5쪽(PDF 7쪽)", "1단계 11/6(금) 이전 · 창의인재 면접 11/28(토)",
                 start_pad=12, end_pad=35, lr=32)
    make_capture(HERE / "tuk-2027-criteria.png", TU, 24, "4. 선발원칙", "5. 전형일정",
                 U, f"{LBL} 22쪽(PDF 24쪽)", "입학사정관 2명 · 10분 이내 · 학업 30 · 진로 40 · 공동체 30",
                 start_pad=10, end_pad=10, lr=32)
    make_capture(HERE / "tuk-2027-times.png", TU, 24, "5. 전형일정", ("after", "변경할 수 없음"),
                 U, f"{LBL} 22쪽(PDF 24쪽)", "11/28(토) 09:00 · 13:00, AI로봇전공은 09:00만",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "tuk-2027-notice.png", TU, 25, "나. 장소", ("after", "면접에 결시한 자는 불합격 처리함"),
                 U, f"{LBL} 23쪽(PDF 25쪽)", "면접시간·장소 11/24(화) 공고 · 30분 전 입실 · 결시 불합격",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "tuk-2027-blind.png", TU, 25, "동점자 처리기준(2단계)", ("after", "경우 부정행위로 간주하여 처리"),
                 U, f"{LBL} 23쪽(PDF 25쪽)", "교복 등 출신고교 유추 의상 금지 · 이름·고교 언급 시 경고",
                 start_pad=14, end_pad=10, lr=45)
    make_structure(HERE / "structure-tuk.png", [
        "기계공학과를 고른 이유는 움직이는 장치가 왜 멈추는지 원인을 찾는 일이 가장 재미있었기 때문입니다.",
        "2학년 물리 수행평가에서 고무줄 동력 자동차를 만들었는데, 바퀴가 헛돌아 1미터도 못 가고 멈췄습니다.",
        "바퀴에 고무 밴드를 감아 마찰을 늘리자 4미터를 갔고, 원인을 하나씩 바꿔 확인하는 방법을 배웠습니다.",
        "기계공학과에서 동역학과 설계를 배워, 고장 원인을 숫자로 설명하는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_tuk()
