# 한양대 학생부종합(면접형) 블로그 글 이미지. python jobs_hyu.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pymupdf
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

HYU = pdf("한양대학교")
U, LBL = "한양대학교", "2027학년도 수시모집요강"


def y_of(page, text, idx=0, edge="y0"):
    """PDF 쪽(1부터)에서 문구의 y 좌표."""
    r = pymupdf.open(HYU)[page - 1].search_for(text)[idx]
    return getattr(r, edge)


def jobs_hyu():
    make_thumb(HERE / "thumb-hyu.png", "한양대 면접", line2="학생부종합(면접형)", line3="기출 3개·예상 질문 3개")
    # 8쪽(PDF 15): 면접형 확대, 의예과 신설
    make_capture(HERE / "hyu-2027-change.png", HYU, 15, "의예과 선발 및 학생부 기반 면접 실시", "지원자격 ‘자립지원대상자’",
                 U, f"{LBL} 8쪽(PDF 15쪽)", "면접형 120명 → 138명 · 의예과 16명 면접형으로 신설", start_pad=12, end_pad=16)
    # 26쪽(PDF 33): 모집인원·지원자격·전형방법
    make_capture(HERE / "hyu-2027-method.png", HYU, 33, "의과대학 의예과 : 학생부 기반 면접 신설", ("after", "52 page 참조"),
                 U, f"{LBL} 26쪽(PDF 33쪽)", "138명 · 1단계 학생부종합평가 100(7배수 내외) · 2단계 70+30", start_pad=12, end_pad=10)
    # 1쪽(PDF 8): 면접형 전형일정
    make_capture(HERE / "hyu-2027-schedule.png", HYU, 8, "1단계 합격자 발표",
                 y_of(8, "최종합격자 발표", 1, "y1") + 9,
                 U, f"{LBL} 1쪽(PDF 8쪽)", "1단계 11/13(금) 예정 · 면접 11/22(일) · 12/5(토) · 12/6(일)", start_pad=10)
    # 27쪽(PDF 34): 모집단위별 면접 방식 + 제시문 기반 면접
    make_capture(HERE / "hyu-2027-eng.png", HYU, 34, "5. 면접고사", ("after", "55 page 참조"),
                 U, f"{LBL} 27쪽(PDF 34쪽)", "공대·인터칼리지 제시문 기반 · 현장 녹화(비대면) · 20분 내외", start_pad=12, end_pad=10)
    # 27쪽(PDF 34): 학생부 기반 면접(의예과·사범대학)
    make_capture(HERE / "hyu-2027-medu.png", HYU, 34, "2) 의과대학 및 사범대학", ("after", "논리적인 전개력"),
                 U, f"{LBL} 27쪽(PDF 34쪽)", "의예 12/5 · 사범 12/6 · 2인 내외 대면 · 10분 내외", start_pad=12, end_pad=14, end_idx=-1)
    # 55쪽(PDF 62): 면접고사 유의사항
    make_capture(HERE / "hyu-2027-rule.png", HYU, 62, "Ⅱ. 면접고사 유의사항", ("after", "반드시 확인해야 합니다"),
                 U, f"{LBL} 55쪽(PDF 62쪽)", "블라인드 · 교복 착용 금지 · 모바일 신분증 불인정 · 미응시 불합격", start_pad=12, end_pad=10)
    # 28쪽(PDF 35): 동점자·수능최저
    make_capture(HERE / "hyu-2027-tie.png", HYU, 35, "6. 동점자 처리기준", ("after", "60 page 참조"),
                 U, f"{LBL} 28쪽(PDF 35쪽)", "동점자 1순위 면접 성적 · 수능최저학력기준 미적용", start_pad=12, end_pad=10)
    make_structure(HERE / "structure-hyu.png", [
        "의료인에게 가장 필요한 태도는 환자가 이해할 때까지 설명하는 것이라고 생각합니다.",
        "보건 동아리에서 어르신 복약 안내문을 만들었는데, 처음 만든 표는 글씨가 작고 용어가 어려워 읽기 힘들다는 말을 들었습니다.",
        "글자를 키우고 '식후 30분'처럼 시간을 그림으로 바꿔 다시 여쭤보니 그제야 고개를 끄덕이셨고, 설명은 듣는 사람 기준으로 해야 한다는 것을 배웠습니다.",
        "의예과에서 의학 지식만큼 환자와 소통하는 법도 배워, 설명을 끝까지 책임지는 의사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_hyu()
