# 한국외대 학생부종합전형(면접형) 블로그 글 이미지. python jobs_hufs_int.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

HUFS = pdf("한국외국어대학교")
U, LBL = "한국외국어대학교", "2027학년도 수시모집요강"


def jobs_hufs_int():
    make_thumb(HERE / "thumb-hufs.png", "한국외대 면접", line2="학생부종합 면접형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "hufs-2027-int-summary.png", HUFS, 16, "1. 2027학년도 수시모집 전형 요약", "2. 수시모집 지원 횟수 6회 제한",
                 U, f"{LBL} 14쪽(PDF 16쪽)", "학생부종합전형(면접형) 478명 · 1단계 3배수 · 2단계 서류 50% + 면접 50%", start_pad=10, end_pad=8)
    make_capture(HERE / "hufs-2027-int-method.png", HUFS, 25, "2. 대학수학능력시험 최저학력기준", ("after", "단계별 선발인원 이내의 순위에 포함되더라도"),
                 U, f"{LBL} 23쪽(PDF 25쪽)", "수능최저 없음 · 1단계 500점 3배수 · 2단계 1,000점 · 점수 일정 수준 이하는 불합격", start_pad=10, end_pad=2)
    make_capture(HERE / "hufs-2027-int-tie.png", HUFS, 27, "7. 동점자 처리 기준", ("after", "1단계 불합격자에 한하여"),
                 U, f"{LBL} 25쪽(PDF 27쪽)", "2단계 동점자는 면접 총점 → 진로개발역량 → 협력적소통역량 순", start_pad=10, end_pad=10)
    make_capture(HERE / "hufs-2027-int-schedule.png", HUFS, 21, "1단계", 325.5,
                 U, f"{LBL} 19쪽(PDF 21쪽)", "1단계 11/16(월) · 면접 11/21(토) 서울캠·11/22(일) 글로벌캠, 모두 서울캠퍼스", start_pad=1)
    make_capture(HERE / "hufs-2027-int-change.png", HUFS, 16, "다. 학생부종합전형(면접형) 면접고사 평가요소 변경", "라. 학교생활기록부에",
                 U, f"{LBL} 14쪽(PDF 16쪽)", "면접 평가요소 변경: 학업·진로·공동체역량 → 진로개발·협력적소통역량", start_pad=2, end_pad=8)
    make_capture(HERE / "hufs-2027-int-eval.png", HUFS, 25, "다. 면접평가", ("after", "- 면접태도"),
                 U, f"{LBL} 23쪽(PDF 25쪽)", "인·적성면접 · 2인 면접관 · 진로개발역량 60 + 협력적소통역량 40", start_pad=3, end_pad=10)
    make_capture(HERE / "hufs-2027-int-blind.png", HUFS, 26, "4) 블라인드 면접 유의사항", ("after", "(면접대기실에서는 소지 허용)"),
                 U, f"{LBL} 24쪽(PDF 26쪽)", "성명·수험번호·출신고교 블라인드 · 가번호 순서 · 교복 금지 · 면접고사실 수험표 소지 금지", start_pad=10, end_pad=2)
    make_structure(HERE / "structure-hufs.png", [
        "스페인어과에 지원한 이유는 언어를 통해 중남미 사회를 직접 이해하고 싶어서입니다.",
        "1학년 세계지리 시간에 중남미의 커피 수출 구조를 조사하다가, 현지 기사 원문을 읽지 못해 번역 요약에만 기대야 하는 것이 답답했습니다.",
        "그래서 방과후 스페인어 강좌를 신청하고 짧은 현지 기사를 사전을 찾아 가며 직접 요약해 보면서, 원문을 읽어야 보이는 것이 있다는 것을 알았습니다.",
        "한국외대 스페인어과에서 언어와 함께 그 지역의 사회와 경제를 배워, 원문으로 지역을 읽는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_hufs_int()
