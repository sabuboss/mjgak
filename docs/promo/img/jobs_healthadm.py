# 보건행정학과 학과 글(naver-94) 이미지. python -I jobs_healthadm.py
# 쪽수: 남서울대('- 38 -')·을지대('17','18')·부산가톨릭대('21') 모두 인쇄 쪽수 = PDF 쪽수.
# 부산가톨릭대 요강은 src 에 없어 기존 다운로드본(dl_dept/speech-therapy/cup_2027_susi.pdf)을 읽기만 한다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"
CUP = str(Path(__file__).parent / "src" / "m_부산가톨릭대학교.pdf")  # 공식 입학처 2027 수시모집요강


def jobs_healthadm():
    make_thumb(HERE / "thumb-healthadm.png", "보건행정학과")
    # 남서울대 교과+면접: 면접평가 개요(공동체 40 · 진로 60 · 비대면 녹화영상 3분 이내 · 업로드 일시)
    make_capture(HERE / "namseoul-2027-healthadm-video.png", pdf("남서울대학교"), 38, "면접평가 개요", 252,
                 "남서울대학교", f"{LBL} 38쪽", "교과+면접 · 비대면 녹화영상 3분 이내 · 공동체 40% + 진로 60%",
                 start_pad=34, lr=30)
    # 을지대 EU면접형: 전형방법 · 면접일 · 평가항목
    make_capture(HERE / "eulji-2027-healthadm-interview.png", pdf("을지대학교"), 17, "1. EU면접형", ("after", "제출서류 진위여부"),
                 "을지대학교", f"{LBL} 17쪽", "EU면접형 · 1단계 4배수 · 70% + 면접 30% · 11월 21일(토)",
                 start_pad=12, end_pad=8)
    # 을지대 전년도 면접 문항: 첫 문항부터 '보건 통계 분석' 문항까지
    make_capture(HERE / "eulji-2027-healthadm-questions.png", pdf("을지대학교"), 18, "라. 전년도(2026학년도) 면접문항 예시", ("after", "보건 통계 분석"),
                 "을지대학교", f"{LBL} 18쪽", "전년도(2026학년도) 실제 면접 문항 공개(일부)",
                 start_pad=10, end_pad=4)
    # 부산가톨릭대 자기추천전형: 비대면 면접 운영 · 블라인드 · 평가영역
    make_capture(HERE / "cup-2027-healthadm-interview.png", CUP, 21, "나. 면접평가", ("after", "배려심 및 공동체 의식"),
                 "부산가톨릭대학교", f"{LBL} 21쪽", "자기추천전형 · 면접영상 업로드 · 입학사정관 2명 평가",
                 start_pad=10, end_pad=12, lr=46)
    make_structure(HERE / "structure-healthadm.png", [
        "병원이 돌아가려면 진료 말고도 기록과 정보를 정확하게 관리하는 사람이 필요하다고 생각해 지원했습니다.",
        "할아버지가 입원하셨을 때 접수, 보험 청구, 의무기록을 맡는 분들이 따로 있다는 것을 처음 알았습니다.",
        "지원 학과 교육과정표를 찾아보니 보건의료 제도와 병원 경영, 보건의료정보를 다루는 과목이 함께 있었습니다.",
        "입학하면 의료 기록과 정보를 다루는 과목부터 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_healthadm()
