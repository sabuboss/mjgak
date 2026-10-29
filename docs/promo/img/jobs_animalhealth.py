# 동물보건학과 학과 글(naver-98) 이미지. python jobs_animalhealth.py
# 쪽수: 호서대 인쇄 쪽 = PDF 쪽 (PDF 27·50쪽 하단 '27'·'50'), 남서울대 인쇄 쪽 = PDF 쪽 (PDF 38쪽 '- 38 -'),
#       청주대 인쇄 = PDF (캡처 없음, 본문 쪽수만).
# 새 다운로드 없음.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"
HS = pdf("호서대학교")
NSU = pdf("남서울대학교")


def jobs_animalhealth():
    make_thumb(HERE / "thumb-animalhealth.png", "동물보건학과")
    # 호서대 학생부교과(면접전형): 교과 60 + 면접 40 · 최저 미반영 · 면접 10/23~24(25) · 공지 10/14
    make_capture(HERE / "hoseo-2027-animalhealth-method.png", HS, 27, "2. 전형 방법", "4. 제출 서류",
                 "호서대학교", f"{LBL} 27쪽", "면접전형 · 교과 60 + 면접 40 · 면접 10월 23일~24일(종료)",
                 start_pad=10, end_pad=10)
    # 호서대 면접고사 진행(예상 문제 중심, 약 10분, 다대일) + 복장·블라인드 + 평가항목
    make_capture(HERE / "hoseo-2027-animalhealth-interview.png", HS, 50, "03_면접고사 진행", ("after", "대학 인재상(협업, 선도, 자원관리, 창의성)"),
                 "호서대학교", f"{LBL} 50쪽", "예상 문제 중심 · 약 10분 내외 · 다대일 · 블라인드",
                 start_pad=10, end_pad=10)
    # 남서울대 교과면접: 비대면 녹화영상 3분 이내 · 공동체 40%(공개 5문항 중 2) · 진로 60%(당일 공개) · 업로드 9/19
    make_capture(HERE / "namseoul-2027-animalhealth-video.png", NSU, 38, "면접평가", "비대면 녹화영상 면접 평가 가이드",
                 "남서울대학교", f"{LBL} 38쪽", "교과면접 · 녹화영상 3분 이내 · 공동체 40% + 진로 60% · 9월 19일",
                 start_pad=12, end_pad=8)
    make_structure(HERE / "structure-animalhealth.png", [
        "수의사의 지도 아래 동물을 꼼꼼히 관찰하고 돌보는 동물보건사가 되고 싶어 지원했습니다.",
        "키우던 강아지가 밥을 먹지 않아 간 동물병원에서, 수의사 옆에서 강아지를 안정시키고 체온을 재며 진료를 돕는 분을 봤습니다.",
        "찾아보니 동물보건사는 동물의 상태를 관찰하고 체온·심박수 같은 기초 자료를 모으는 일도 맡는다는 것을 알았습니다.",
        "입학하면 동물의 몸과 질병의 기초부터 정확하게 배워 작은 변화도 알아채는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_animalhealth()
