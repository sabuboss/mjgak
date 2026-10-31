# 연세대 미래캠퍼스 의예과 면접(학교생활우수자(면접형) 중심) 블로그 글(naver-114) 이미지. python jobs_ysmirae.py
# PDF: src/m_연세대학교미래.pdf = 연세대 미래입학처 수시 모집요강/서식 페이지(admission.yonsei.ac.kr/mirae/admission/html/rolling/guide.asp)의
#      "[배포용]2027학년도 연세대학교 미래캠퍼스 수시모집요강" PDF(2026-09-09 작성, 106쪽). 2026-10-31 받음.
# 인쇄 쪽수 = PDF 쪽수 - 5 (인쇄 33쪽 = PDF 38쪽).
# 기출 문항은 대학 이용 조건(인용 시 본교 허락) 때문에 캡처하지 않는다. 쪽 머리의 대학 교표가 들어가지 않게 자른다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

YS = pdf("연세대학교미래")
U, LBL = "연세대학교 미래캠퍼스", "2027학년도 수시모집요강"


def jobs_ysmirae():
    make_thumb(HERE / "thumb-ysmirae.png", "연세대 미래", line2="의예과 면접 11/28", line3="예상 질문 6개 총정리")
    make_capture(HERE / "ysmirae-2027-med-units.png", YS, 38, "1. 모집단위 및 모집인원", "2. 지원자격",
                 U, f"{LBL} 33쪽(PDF 38쪽)", "학교생활우수자(면접형) 369명 중 의예과 21명",
                 start_pad=4, end_pad=10, lr=30)
    make_capture(HERE / "ysmirae-2027-med-method.png", YS, 38, "3. 전형방법: 단계별", ("after", "최하등급(C) 부여"),
                 U, f"{LBL} 33쪽(PDF 38쪽)", "1단계 서류 100%(의예과 600%) · 2단계 1단계 70 + 면접 30",
                 start_pad=8, end_pad=8, lr=30)
    make_capture(HERE / "ysmirae-2027-med-schedule.png", YS, 19, "1. 전형일정 및 합격자 발표", ("after", "2026.12.18"),
                 U, f"{LBL} 14쪽(PDF 19쪽)", "의예과 면접대상자 발표 11/24(화) 17시 · 면접 11/28(토)",
                 start_pad=8, end_pad=2, lr=30)
    make_capture(HERE / "ysmirae-2027-med-interview.png", YS, 85, "면접방식", "3. 면접 관련 수험생 유의사항",
                 U, f"{LBL} 80쪽(PDF 85쪽)", "의예과 현장 대면 · 숙지 10분 · 면접 10분 · 제시문 질문 2 + 현장 질문 2",
                 start_pad=10, end_pad=8, lr=30)
    make_capture(HERE / "ysmirae-2027-med-rules.png", YS, 85, "3. 면접 관련 수험생 유의사항", ("after", "면접대상자 유의사항"),
                 U, f"{LBL} 80쪽(PDF 85쪽)", "응시표·신분증 모두 지참 · 교복·명찰 금지 · 입실 시각 엄수",
                 start_pad=8, end_pad=8, lr=30)
    make_capture(HERE / "ysmirae-2027-med-summary.png", YS, 7, "가. 전형요약표", ("after", "면접일정이 겹쳐"),
                 U, f"{LBL} 2쪽(PDF 7쪽)", "의예과 면접 전형 · 교과 81+9+10 · 종합 80+20 · 1개 전형만",
                 start_pad=3, end_pad=8, lr=30)
    make_capture(HERE / "ysmirae-2027-med-min.png", YS, 87, "전형명", 262,
                 U, f"{LBL} 82쪽(PDF 87쪽)", "의예과 수능 최저: 전형별로 4합 5·4합 6·3합 5",
                 start_pad=12, lr=30)
    make_structure(HERE / "structure-ysmirae.png", [
        "검사 결과는 먼저 환자 본인에게 알리고, 가족에게 알릴지는 환자가 스스로 정하도록 돕는 것이 맞다고 생각합니다.",
        "생활과 윤리 시간에 유전 정보 공개를 두고 토론했는데, 저는 처음에 가족의 건강을 위해 바로 알려야 한다는 쪽이었습니다.",
        "그런데 같은 정보라도 누가, 언제, 어떻게 전하느냐에 따라 환자가 받는 상처가 달라진다는 반론을 듣고, 비밀 유지와 가족의 이익을 함께 따져야 한다는 것을 배웠습니다.",
        "의사가 되면 환자의 결정을 존중하면서도 가족이 검사받을 기회를 놓치지 않도록, 환자와 충분히 대화하는 의사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_ysmirae()
