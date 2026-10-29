# 치기공학과 학과 글(naver-96) 이미지. python jobs_dentaltech.py
# 쪽수: 신한대 인쇄 쪽 = PDF 쪽 - 2 (PDF 26쪽 '- 24 -'), 부산가톨릭대 인쇄 쪽 = PDF 쪽 (PDF 6·21쪽 하단 '6'·'21').
# 새 다운로드 없음. src/m_신한대학교.pdf, src/m_부산가톨릭대학교.pdf 를 읽는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"
CUP = pdf("부산가톨릭대학교")


def jobs_dentaltech():
    make_thumb(HERE / "thumb-dentaltech.png", "치기공학과")
    # 신한대 일반전형(학생부교과): 면접 평가항목(지원동기 / 논리적 사고력 및 인성) · 개별 구술 3분 내외 · 2인:1인
    make_capture(HERE / "shinhan-2027-dentaltech-interview.png", pdf("신한대학교"), 26, "면접고사 평가항목 및 방법", "학교폭력조치사항 반영 방법",
                 "신한대학교", f"{LBL} 24쪽(PDF 26쪽)", "일반전형 면접 · 개별 구술 3분 내외 · 두 문제 출제 · 2인이 1인 평가",
                 start_pad=14, end_pad=14)
    # 부산가톨릭대 전형일정: 1단계 10/14 · 영상 업로드 10/14~10/21 · 영상 평가 10/25 · 가톨릭지도자추천 대면 10/24
    make_capture(HERE / "cup-2027-dentaltech-schedule.png", CUP, 6, "안내사항", "학생부교과(교과우수전형Ⅰ)",
                 "부산가톨릭대학교", f"{LBL} 6쪽", "자기추천 1단계 10/14 · 영상 업로드 ~10/21 · 영상 평가 10/25(종료)",
                 start_pad=12, end_pad=11, lr=40)
    # 부산가톨릭대 자기추천전형 비대면(영상 업로드) 면접 + 평가영역
    make_capture(HERE / "cup-2027-dentaltech-interview.png", CUP, 21, "나. 면접평가", ("after", "배려심 및 공동체 의식"),
                 "부산가톨릭대학교", f"{LBL} 21쪽", "자기추천 비대면 영상 면접 · 학생부 기반 문항 · 입학사정관 2명",
                 start_pad=10, end_pad=10, lr=40)
    make_structure(HERE / "structure-dentaltech.png", [
        "치과의사의 의뢰대로 기공물을 정확하게 만들어 내는 치과기공사가 되고 싶어 지원했습니다.",
        "교정 치료 때 입안 본을 뜨고 며칠 뒤 장치가 제 이에 딱 맞게 나온 것을 보고, 누가 만드는지 궁금해졌습니다.",
        "찾아보니 치과기공사는 보철물·교정장치·충전물 같은 치과기공물을 디자인하고 제작·수리·가공하는 사람이었습니다.",
        "입학하면 치아 형태를 이해하는 기초부터 정확하게 배우고, 전산설계 작업까지 익히고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dentaltech()
