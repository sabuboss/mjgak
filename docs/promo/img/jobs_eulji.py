# 을지대 학생부종합 EU면접형 블로그 글(naver-122) 이미지. python jobs_eulji.py
# m_을지대학교.pdf: 인쇄 쪽수 = PDF 쪽수 (쪽마다 인쇄된 번호와 PDF 쪽이 같음).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

EU = str(SRC / "m_을지대학교.pdf")
U, LBL = "을지대학교", "2027학년도 수시모집요강"


def jobs_eulji():
    make_thumb(HERE / "thumb-eulji.png", "을지대 면접", line2="EU면접형", line3="실제 문항 29개 총정리")
    make_capture(HERE / "eulji-2027-eu-units.png", EU, 7, "Ⅱ. 전형별 모집단위", ("after", "미표기는 성남캠퍼스"),
                 U, f"{LBL} 7쪽", "EU면접형(첫째 칸) 123명 · 자연계열학부 26 · 인문사회계열학부 25",
                 start_pad=10, end_pad=3, lr=12)
    make_capture(HERE / "eulji-2027-eu-method.png", EU, 17, "1. EU면접형", "다. 면접고사",
                 U, f"{LBL} 17쪽", "1단계 서류 100% 4배수 · 2단계 1단계 70% + 면접 30% · 최저 없음",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "eulji-2027-eu-docs.png", EU, 41, "다. 평가항목 반영비율", "라. 평가항목별",
                 U, f"{LBL} 41쪽", "EU면접형 서류평가 학업 35 · 진로 35 · 공동체 30",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "eulji-2027-eu-schedule.png", EU, 11, "6. 고사일정", ("after", "공지사항을 필히 확인"),
                 U, f"{LBL} 11쪽", "11/18(수) 대상자·고사장 발표 · 11/21(토) 면접 · 성남캠퍼스",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "eulji-2027-eu-interview.png", EU, 17, "다. 면접고사", ("after", "면접태도 및 자세, 제출서류 진위여부"),
                 U, f"{LBL} 17쪽", "서류기반 블라인드 면접 · 단정한 사복 · 평가 30·30·20·20",
                 start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "eulji-2027-eu-questions.png", EU, 18, "라. 전년도", "마. 제출서류",
                 U, f"{LBL} 18쪽", "대학이 공개한 2026학년도 실제 면접 문항 29개",
                 start_pad=10, end_pad=12, lr=40)
    make_structure(HERE / "structure-eulji.png", [
        "1학년 때는 기계공학에 관심이 있었는데, 2학년 물리학Ⅰ에서 전자기파를 배우며 관심이 의료 영상으로 옮겨 갔습니다.",
        "X선이 몸을 통과하는 정도가 조직마다 다르다는 것을 배우고, 뼈는 하얗게, 폐는 검게 보이는 이유를 조사해 발표했습니다.",
        "기계를 좋아하는 마음은 그대로이고, 그 기계가 사람을 진단하는 데 쓰인다는 점에서 진로가 더 분명해졌습니다.",
        "방사선학과에서 영상 장비의 원리와 방사선 안전을 함께 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_eulji()
