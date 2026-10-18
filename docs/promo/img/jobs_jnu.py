# 전남대 학생부종합 고교생활우수자Ⅰ 블로그 글 이미지. python jobs_jnu.py
# 전남대 PDF: 인쇄 쪽수 = PDF 쪽수 (같음).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

JNU = pdf("전남대학교")
U, LBL = "전남대학교", "2027학년도 수시모집요강"


def jobs_jnu():
    make_thumb(HERE / "thumb-jnu.png", "전남대 면접", line2="고교생활우수자Ⅰ", line3="예상 질문 7개 총정리")
    make_capture(HERE / "jnu-2027-gs-method.png", JNU, 40, "1. 학생부종합(고교생활우수자", "2) 평가 방법",
                 U, f"{LBL} 40쪽", "899명 · 1단계 서류 100% 3배수(수의·약·의·치전원 6배수) · 2단계 1단계 70% + 면접 30%",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "jnu-2027-gs-minimum.png", JNU, 40, "2) 평가 방법", "라. 제출 서류",
                 U, f"{LBL} 40쪽", "수능 최저는 의학과·치의학전문대학원·수의예과·약학부만",
                 start_pad=4, end_pad=8)
    make_capture(HERE / "jnu-2027-gs-schedule.png", JNU, 16, "2026. 11. 13.(금) 15:00 예정", 527,
                 U, f"{LBL} 16쪽", "1단계 11/13(금) 15:00 · 면접 안내 11/25(수) 15:00 · 면접 12/2(수)",
                 start_pad=5)
    make_capture(HERE / "jnu-2027-gs-result.png", JNU, 16, "2026. 12. 18.(금) 15:00 예정", 712,
                 U, f"{LBL} 16쪽", "최초 합격자 발표 12/18(금) 15:00 예정 · 등록 12/21(월)~12/23(수)",
                 start_pad=3.5)
    make_capture(HERE / "jnu-2027-gs-interview.png", JNU, 53, "1. 평가 요소 및 반영 점수", "3. 면접 응시자 유의사항",
                 U, f"{LBL} 53쪽", "진로·학업역량 180 · 공동체역량 120 · 15분 이내 · 학생부 기반",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "jnu-2027-gs-rules.png", JNU, 53, "3. 면접 응시자 유의사항", ("after", "라. 교내·외 인증시험"),
                 U, f"{LBL} 53쪽", "교복·명찰 착용 금지 · 블라인드 면접 · 학생부 기재금지 항목 발언 금지",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "jnu-2027-gs-tie.png", JNU, 61, "면접 점수가 높은 자", 697,
                 U, f"{LBL} 61쪽", "2단계 동점자: 면접 점수 → 면접 진로·학업역량 → 면접 공동체역량 순",
                 start_pad=4, start_idx=1)
    make_structure(HERE / "structure-jnu.png", [
        "기계공학부에 지원한 이유는 움직이는 물건이 어떻게 힘을 전달하는지 직접 확인해 보면서 기계 설계에 관심이 생겼기 때문입니다.",
        "2학년 물리 시간에 지레와 도르래를 배운 뒤, 동아리에서 고무줄과 나무 막대로 물건을 들어 올리는 팔 모형을 만들었습니다.",
        "처음 만든 팔은 끝부분이 자꾸 휘었는데, 막대를 두 겹으로 붙이고 받침점을 옮기자 더 무거운 물건도 들었고, 모양을 조금만 바꿔도 힘이 전달되는 방식이 달라진다는 것을 알았습니다.",
        "기계공학부에서 재료역학과 기계 설계를 배워, 작은 힘으로도 무거운 짐을 옮기는 장치를 만들어 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_jnu()
