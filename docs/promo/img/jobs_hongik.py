# 홍익대 실기/실적 미술우수자전형(서울·세종) + 농어촌학생전형 미술계열 블로그 글 이미지. python jobs_hongik.py
# 서울·세종 PDF 는 같은 모집요강(본문 동일). 인쇄 쪽수 = PDF 쪽수 - 2.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

SE = str(SRC / "m_홍익대학교(서울).pdf")
SJ = str(SRC / "m_홍익대학교(세종).pdf")
U, LBL = "홍익대학교", "2027학년도 수시모집요강"


def jobs_hongik():
    make_thumb(HERE / "thumb-hongik.png", "홍익대 면접", line2="미술우수자전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "hongik-2027-seoul-method.png", SE, 61, "1. 모집인원", ("after", "1단계 서류 성적을 반영함"),
                 U, f"{LBL} 59쪽(PDF 61쪽)", "서울 289명 · 1단계 교과 20 + 서류 80, 3배수 · 2단계 서류 40 + 면접 60",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "hongik-2027-interview.png", SE, 62, "(3) 서류평가", ("after", "면접 기출문제 예시는"),
                 U, f"{LBL} 60쪽(PDF 62쪽)", "면접: 미술관련 소양 · 창의성 · 표현능력 · 제출서류의 진실성",
                 start_pad=3, end_pad=12, lr=45)
    make_capture(HERE / "hongik-2027-seoul-schedule.png", SE, 63, "4. 대학수학능력시험", ("after", "섬유미술·패션디자인과"),
                 U, f"{LBL} 61쪽(PDF 63쪽)", "최저 3개 합 9 + 한국사 4 · 11/7(토) 발표 · 면접 12/5(토)~6(일)",
                 start_pad=10, end_pad=12, lr=45, end_idx=-1)
    make_capture(HERE / "hongik-2027-report-check.png", SE, 13, "(3) 본교는 미술활동보고서", ("after", "지정된 고사일시는 변경할 수 없음"),
                 U, f"{LBL} 11쪽(PDF 13쪽)", "보고서 유사도 결과는 면접에서 확인할 수 있음 · 수험표·신분증 지참",
                 start_pad=2, end_pad=8, lr=45)
    make_capture(HERE / "hongik-2027-doc-eval.png", SE, 122, "2. 실기/실적위주 전형", ("after", "타인을 위해 양보할 줄"),
                 U, f"{LBL} 120쪽(PDF 122쪽)", "미술우수자 서류평가: 학업 20 · 전공 40 · 발전가능성 25 · 인성 15",
                 start_pad=2, end_pad=10, lr=45, end_idx=-1)
    make_capture(HERE / "hongik-2027-sejong-schedule.png", SJ, 78, "2. 미술계열", ("after", "지정된 고사 일시는 변경할 수 없음"),
                 U, f"{LBL} 76쪽(PDF 78쪽)", "세종 미술계열 · 11/7(토) 발표 · 면접 11/28(토)~29(일)",
                 start_pad=10, end_pad=8, lr=45)
    make_capture(HERE / "hongik-2027-farm-method.png", SE, 33, "3. 전형방법", ("after", "1단계 서류 성적을 반영함"),
                 U, f"{LBL} 31쪽(PDF 33쪽)", "농어촌학생 미술계열: 1단계 2배수 · 2단계 서류 40 + 면접 60",
                 start_pad=10, end_pad=10, lr=45)
    make_structure(HERE / "structure-hongik.png", [
        "제가 고른 활동은 2학년 미술 시간에 만든 횡단보도 안전 안내 포스터입니다.",
        "등굣길 사진으로 위험한 곳을 표시해 초안을 그렸는데, 글자가 많아 멀리서 알아보기 어렵다는 친구들 말을 듣고 신호를 기다리는 발 그림 하나로 줄여 다시 그렸습니다.",
        "보는 사람의 눈높이에서 다시 확인해야 표현이 전달된다는 것을 배웠습니다.",
        "디자인학부에서 정보를 한눈에 전하는 디자인을 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_hongik()
