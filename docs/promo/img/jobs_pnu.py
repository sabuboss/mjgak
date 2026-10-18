# 부산대 학생부종합(학생부종합전형·지역인재전형) 블로그 글 이미지. python jobs_pnu.py
# PDF 쪽수와 인쇄 쪽수: PDF 3~51쪽은 인쇄 = PDF - 2, PDF 52쪽부터는 인쇄 = PDF - 3 (PDF 51·52쪽이 둘 다 '- 49 -').
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_부산대학교.pdf")
U, LBL = "부산대학교", "2027학년도 수시모집요강"


def jobs_pnu():
    make_thumb(HERE / "thumb-pnu.png", "부산대 면접", line2="학생부종합·지역인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "pnu-2027-units.png", P, 36, "가. 모집단위", ("after", "합계"),
                 U, f"{LBL} 34쪽(PDF 36쪽)", "학생부종합 778명 · 지역인재 178명 · 의예과·약학부·간호학과는 지역인재만",
                 start_pad=10, end_pad=8, lr=45)
    make_capture(HERE / "pnu-2027-summary.png", P, 8, "전형별 모집인원", "논술전형",
                 U, f"{LBL} 6쪽(PDF 8쪽)", "면접은 학생부종합·지역인재·지역의사선발 · 그 아래 5개 전형은 서류 100%",
                 start_pad=10, end_pad=4, lr=45)
    make_capture(HERE / "pnu-2027-method.png", P, 37, "다. 전형방법", ("after", "총점의 고득점자순으로 충원합니다"),
                 U, f"{LBL} 35쪽(PDF 37쪽)", "1단계 서류 100% 3배수(약·의·치 4배수) · 2단계 1단계 80% + 면접 20%",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "pnu-2027-schedule.png", P, 38, "전형일정", ("after", "등록 및 충원합격자 발표 일정"),
                 U, f"{LBL} 36쪽(PDF 38쪽)", "1단계 12/1(화) 16시 · 면접 12/5(토) · 최초 합격 12/18(금) 16시",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "pnu-2027-interview.png", P, 67, "안내 4. 면접고사 안내", "5. 유의사항",
                 U, f"{LBL} 64쪽(PDF 67쪽)", "학생부 기반 면접 10분 내외 · 의예과는 공통문제 준비 10분 + 면접 10분 추가",
                 start_pad=10, end_pad=8, lr=22)
    make_capture(HERE / "pnu-2027-rules.png", P, 67, "5. 유의사항", ("after", "참조"),
                 U, f"{LBL} 64쪽(PDF 67쪽)", "결시·중도 포기 불합격 · 교복 착용 불가 · 성명·출신고교·지역 등 발언 금지",
                 start_pad=10, end_pad=10, lr=22, end_idx=-1)
    make_capture(HERE / "pnu-2027-minimum.png", P, 38, "동점자 선발", "전형일정",
                 U, f"{LBL} 36쪽(PDF 38쪽)", "학종·지역인재 최저는 간호학과·약학부·치의예과·의예과만 · 동점자는 면접 점수 먼저",
                 start_pad=10, end_pad=10, lr=45)
    make_structure(HERE / "structure-pnu.png", [
        "기계공학부에 가려고 2학년 때 물리학과 함께 기하를 골라 들었습니다.",
        "물리 시간에 도르래를 배우고 도르래 수를 바꿔 가며 같은 상자를 들어 올리는 힘을 용수철저울로 쟀습니다.",
        "기하에서 배운 벡터로 힘을 나눠 그려 보니, 측정값이 왜 계산과 조금씩 다른지 설명할 수 있었습니다.",
        "기계공학부에서 역학을 제대로 배워 힘이 덜 드는 기계 장치를 설계해 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_pnu()
