# 서울여대 학생부종합 바롬인재면접전형 블로그 글 이미지. python jobs_swu.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SWU = pdf("서울여자대학교")
U, LBL = "서울여자대학교", "2027학년도 수시모집요강"


def jobs_swu():
    make_thumb(HERE / "thumb-swu.png", "서울여대 면접", line2="바롬인재면접", line3="예상 질문 7개 총정리")
    make_capture(HERE / "swu-2027-barom-units.png", SWU, 16, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 14쪽(PDF 16쪽)", "바롬인재면접전형 202명 · 경영학과·언론영상학부 각 14명", start_pad=10, end_pad=8)
    make_capture(HERE / "swu-2027-barom-method.png", SWU, 16, "3. 전형방법", ("after", "동점자 처리기준 p.50 참고"),
                 U, f"{LBL} 14쪽(PDF 16쪽)", "1단계 서류 100% 5배수 · 2단계 서류 50% + 면접 50% · 최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "swu-2027-barom-tie.png", SWU, 52, "4. 동점자 처리기준 안내", ("after", "7순위 (서류평가 요소)"),
                 U, f"{LBL} 50쪽(PDF 52쪽)", "2단계 동점자: 면접평가 점수 → 서류 진로역량 → 서류 학업역량 순", start_pad=10, end_pad=10)
    make_capture(HERE / "swu-2027-barom-schedule.png", SWU, 17, "5. 전형일정", "6. 제출서류",
                 U, f"{LBL} 15쪽(PDF 17쪽)", "1단계 11/25(수) 18:00 예정 · 면접 11/28(토) · 최초합격 12/18(금)", start_pad=10, end_pad=8)
    make_capture(HERE / "swu-2027-barom-interview.png", SWU, 51, "면접평가", "6) 면접 내용 및 유의사항",
                 U, f"{LBL} 49쪽(PDF 51쪽)", "면접관 2인 개별 블라인드 10분 내외 · 진로 40 · 발전 35 · 인성 25", start_pad=10, end_pad=8)
    make_capture(HERE / "swu-2027-barom-blind.png", SWU, 51, "6) 면접 내용 및 유의사항", ("after", "면접고사 장소와 시간 등은"),
                 U, f"{LBL} 49쪽(PDF 51쪽)", "학생부 기반 지원동기·교과 이수 노력·관련 경험 확인 · 교복 착용 금지", start_pad=10, end_pad=10)
    make_capture(HERE / "swu-2027-barom-rule.png", SWU, 12, "학생부종합전형은 지원자 성명", ("after", "면접, 논술, 실기고사에 결시한 자"),
                 U, f"{LBL} 10쪽(PDF 12쪽)", "면접에서 성명·출신고교 등 언급 시 불이익 · 결시·중도포기는 불합격", start_pad=3, end_pad=3)
    make_structure(HERE / "structure-swu.png", [
        "언론영상학부에 지원한 이유는 같은 사건도 어떻게 전하느냐에 따라 사람들의 이해가 달라진다는 것을 직접 확인했기 때문입니다.",
        "2학년 방송부에서 학교 급식 설문 결과를 영상으로 전할 때, 처음 만든 영상은 숫자만 보여 줘서 친구들이 내용을 기억하지 못했습니다.",
        "학생 인터뷰 두 개를 넣고 결과를 그래프 한 장으로 줄여 다시 만들었더니, 영상을 본 친구들이 결과를 먼저 이야기하기 시작했습니다.",
        "언론영상학부에서 취재와 영상 제작을 함께 배워, 정확한 내용을 이해하기 쉽게 전하는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_swu()
