# 언어치료학과 학과 글(naver-93) 이미지. python jobs_speech.py
# 쪽수: 한림대 디자인본 PDF 는 12쪽부터 인쇄 쪽수 = PDF 쪽수(24·88쪽 확인).
#       부산가톨릭대 PDF 는 인쇄 쪽수 = PDF 쪽수(5·20·21쪽 확인).
# 부산가톨릭대 요강은 src/m_부산가톨릭대학교.pdf 를 읽는다(새 다운로드 없음).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"
HL = str(SRC / "m_한림대학교.pdf")
CUP = str(Path(__file__).parent / "src" / "m_부산가톨릭대학교.pdf")  # 공식 입학처 2027 수시모집요강


def jobs_speech():
    make_thumb(HERE / "thumb-speech.png", "언어치료학과")
    # 한림대 학생부종합 공통: 전형일정(1단계 12/3, 학교생활우수자 면접 12/9) + 전형방법(4배수, 70+30)
    make_capture(HERE / "hallym-2027-speech-method.png", HL, 24, "1. 전형일정", "※ 계산과정에서",
                 "한림대학교", f"{LBL} 24쪽", "1단계 서류 100% 4배수 · 2단계 70 + 면접 30 · 면접 12/9(수)",
                 start_pad=8, end_pad=1, lr=40)
    # 한림대 면접(의학과 제외): 서류검증 50% 개별문항 · 인성 50% 공통문항 · 평가기준
    make_capture(HERE / "hallym-2027-speech-interview.png", HL, 88, "나) 평가영역 및 주요내용", "[면접평가 점수산출 예시]",
                 "한림대학교", f"{LBL} 88쪽", "서류검증 50%(제출서류 기반 개별문항) · 인성 50%(공통문항)",
                 start_pad=8, end_pad=8, lr=40)
    # 부산가톨릭대 자기추천전형: 지원자격 · 수능최저 없음 · 1단계 5배수 · 70 + 30
    make_capture(HERE / "cup-2027-speech-method.png", CUP, 20, "1. 지원자격", ("after", "1단계 평가서류"),
                 "부산가톨릭대학교", f"{LBL} 20쪽", "자기추천전형 · 1단계 서류 5배수 · 70% + 면접 30% · 최저 없음",
                 start_pad=10, end_pad=8, lr=40)
    # 부산가톨릭대 비대면(영상 업로드) 면접 안내 + 평가영역
    make_capture(HERE / "cup-2027-speech-interview.png", CUP, 21, "나. 면접평가", ("after", "배려심 및 공동체 의식"),
                 "부산가톨릭대학교", f"{LBL} 21쪽", "비대면 영상 면접 · 학생부 기반 문항 · 진로역량 10 · 공동체역량 20",
                 start_pad=10, end_pad=10, lr=40)
    make_structure(HERE / "structure-speech.png", [
        "언어재활사는 의사소통이 어려운 사람에게 진단과 훈련을 함께 하는 전문가라고 알게 돼 지원했습니다.",
        "말이 늦던 사촌 동생이 1년 동안 언어치료실에 다닌 뒤 처음으로 자기 이름을 또박또박 말해서 온 가족이 기뻐했습니다.",
        "찾아보니 언어재활사는 영유아부터 노년기까지 만나고, 말을 고쳐 주는 것보다 진단에서 출발한다는 것을 배웠습니다.",
        "입학하면 아동의 언어발달과 진단 방법부터 제대로 배워 보호자와 함께 가는 언어재활사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_speech()
