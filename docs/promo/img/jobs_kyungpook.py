# 경북대 학생부종합(지역인재전형 등 면접 실시 전형) 블로그 글 이미지. python jobs_kyungpook.py
# PDF 쪽수와 인쇄 쪽수: 인쇄 = PDF - 3 (PDF 4쪽 = '- 1 -', PDF 114쪽 = '- 111 -' 모두 확인).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_경북대학교.pdf")
U, LBL = "경북대학교", "2027학년도 수시모집요강"


def jobs_kyungpook():
    make_thumb(HERE / "thumb-kyungpook.png", "경북대 면접", line2="학생부종합 지역인재", line3="예상 질문 7개 총정리")
    make_capture(HERE / "kyungpook-2027-summary.png", P, 5, "일반학생전형", "논술(AAT)전형",
                 U, f"{LBL} 2쪽(PDF 5쪽)", "학생부종합 일반학생 883명은 서류 100% · 지역인재 366명 등은 면접 30%",
                 start_pad=10, end_pad=4, lr=45)
    make_capture(HERE / "kyungpook-2027-units.png", P, 11, "정 원 내", "아동학부",
                 U, f"{LBL} 8쪽(PDF 11쪽)", "지역인재(학생부종합) 의예과 34명 · 전자공학부 30명 · 치의예과 16명",
                 start_pad=8, end_pad=4, lr=30)
    make_capture(HERE / "kyungpook-2027-method.png", P, 40, "가. 모집인원", "라. 서류평가 및 면접",
                 U, f"{LBL} 37쪽(PDF 40쪽)", "1단계 서류 100% 4배수(의·치·약 5배수) · 2단계 서류 70% + 면접 30%",
                 start_pad=10, end_pad=6, lr=30)
    make_capture(HERE / "kyungpook-2027-schedule.png", P, 7, "실기전형(음악학과", ("after", "(88쪽 참조)"),
                 U, f"{LBL} 4쪽(PDF 7쪽)", "1단계 11/6(금) 16시 · 고사장 안내 11/17(화) 10시 · 면접 11/21(토)",
                 start_pad=9, end_pad=10, lr=30, end_idx=-1)
    make_capture(HERE / "kyungpook-2027-interview.png", P, 83, "3. 학생부종합전형 면접", ("after", "모집인원에 관계없이 불합격 처리함"),
                 U, f"{LBL} 80쪽(PDF 83쪽)", "면접위원 2인 · 10분 내외 · 학생부 기반 · 60% 미만 불합격 · 자유복",
                 start_pad=10, end_pad=8, lr=30, end_idx=-1)
    make_capture(HERE / "kyungpook-2027-criteria.png", P, 84, "마. 학생부종합전형", "4. 특기자",
                 U, f"{LBL} 81쪽(PDF 84쪽)", "면접 평가 학업역량 35% · 진로역량 45% · 공동체역량 20%",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "kyungpook-2027-minimum.png", P, 80, "나. 의예과", "다. 전자공학부",
                 U, f"{LBL} 77쪽(PDF 80쪽)", "의·치 수학 포함 3개 영역 합 4 · 약 합 5 · 지역의사는 1등급 하향",
                 start_pad=10, end_pad=8, lr=30)
    make_structure(HERE / "structure-kyungpook.png", [
        "생명과학Ⅰ 시간에 효소의 활성이 온도에 따라 달라진다는 것을 배우고, 감자즙과 과산화수소로 직접 확인해 봤습니다.",
        "10도, 25도, 40도, 60도 물에 감자즙을 담갔다가 과산화수소를 넣고 거품 높이를 쟀더니 40도에서 가장 높았고 60도에서는 거의 생기지 않았습니다.",
        "온도가 너무 높으면 효소 단백질의 구조가 바뀌어 다시 작동하지 않는다는 것을 실험으로 이해했습니다.",
        "생명공학부에서 효소를 산업에 쓰는 방법을 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kyungpook()
