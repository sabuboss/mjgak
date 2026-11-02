# 대입 면접 1분 자기소개 예시와 만드는 법 블로그 글(naver-121) 이미지. python jobs_intro.py
# 캡처: src/m_수원대학교.pdf (2027 수원대학교 신입생 모집요강_수시모집, 인쇄 쪽수 = PDF 쪽수) 34쪽 고교추천전형 면접고사 방법 표.
# 도식: 본문 '학과별 예시 2(자연계열, 화학과)'를 4문장(지원 동기 한 문장 → 대표 경험 → 배운 점 → 입학 후 계획)으로 나눈 것.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

SW = pdf("수원대학교")


def jobs_intro():
    make_thumb(HERE / "thumb-intro.png", "1분 자기소개", line2="학과별 예시 4개", line3="만드는 법 4단계", chip="2027 수시 면접")
    make_capture(HERE / "suwon-2027-intro-1min.png", SW, 34, "면접고사 방법", "유의사항",
                 "수원대학교", "2027학년도 수시모집요강 34쪽", "고교추천전형 · 평가항목 인성(1분 이내 자기소개) · 그룹면접",
                 start_pad=10, end_pad=14, lr=32)
    make_structure(HERE / "structure-intro.png", [
        "안녕하세요, 같은 실험이 왜 다른 값을 내는지 끝까지 확인하고 싶어서 화학과에 지원한 지원자입니다.",
        "2학년 화학 실험에서 비타민C 적정을 했는데 우리 모둠 값만 크게 달라서, 점심시간에 세 번 더 실험해 보니 용액을 만든 뒤 오래 둔 것이 원인이었습니다.",
        "한 번의 결과보다 조건을 바꿔 가며 반복한 기록을 믿어야 한다는 것을 배웠습니다.",
        "입학하면 분석화학을 깊이 공부해 식품 속 성분을 정확히 재는 방법을 연구하고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_intro()
