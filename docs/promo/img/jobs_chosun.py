# 조선대 학생부종합 면접전형 블로그 글(naver-115) 이미지. python jobs_chosun.py
# src/m_조선대학교.pdf = 조선대 입학처(i.chosun.ac.kr) 수시 모집요강 페이지의 "PDF 다운로드"
#   (2027학년도 조선대학교 수시모집요강, 116쪽, PDF 정보상 2026-09-03 작성, 2026-10-31 받음).
# 인쇄 쪽수 = PDF 쪽수 - 6 (인쇄 48쪽 = PDF 54쪽). 글자가 윤곽선이라 텍스트 검색이 안 된다.
# 그래서 jobs_dau.py 와 같은 cap()(좌표 자르기)을 쓴다. 좌표는 100dpi 로 렌더한 쪽 이미지의 픽셀 값.
# 인쇄 88~90쪽(면접평가 문제)은 캡처하지 않는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_조선대학교.pdf")
U, LBL = "조선대학교", "2027학년도 수시모집요강"
PX = 72 / 100  # 100dpi 픽셀 -> PDF 포인트
OFF = 6        # PDF 쪽 = 인쇄 쪽 + 6


def cap(out, printed, box, note, dpi=200):
    """jobs_dau.cap 과 같은 틀. printed=인쇄 쪽수, box=(x0, y0, x1, y1) 100dpi 픽셀."""
    page = printed + OFF
    pg = pymupdf.open(PDF)[page - 1]
    x0, y0, x1, y1 = (v * PX for v in box)
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    W = shot.width + 80
    HEAD, FOOT = 104, 92
    img = Image.new("RGB", (W, HEAD + shot.height + 40 + FOOT), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD], fill=NAVY)
    fc = font(30, True)
    chip = "2027학년도 모집요강"
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 44, 26 + 52], radius=26, fill=ACCENT)
    d.text((40 + 22, 31), chip, font=fc, fill=NAVY_D)
    d.text((40 + cw + 70, 30), U, font=font(38, True), fill="white")
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    fy = HEAD + shot.height + 40
    text_fixed(d, (40, fy + 10), f"출처: {U} {LBL} {printed}쪽(PDF {page}쪽)", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_chosun():
    make_thumb(HERE / "thumb-chosun.png", "조선대 면접", line2="학생부종합 면접전형", line3="예상 질문 7개 총정리")
    cap(HERE / "chosun-2027-units.png", 5, (95, 205, 735, 342),
        "학생부종합 면접전형 252명 → 255명")
    cap(HERE / "chosun-2027-method.png", 48, (95, 295, 735, 492),
        "1단계 서류 100% 5배수 · 2단계 서류 70% + 면접 30%")
    cap(HERE / "chosun-2027-schedule.png", 2, (95, 212, 735, 485),
        "1단계 발표 11/17(화) · 면접 11/28(토)·29(일)")
    cap(HERE / "chosun-2027-date.png", 49, (95, 205, 735, 760),
        "모집단위별 면접일 · 일부 단위는 이틀 중 랜덤 배정")
    cap(HERE / "chosun-2027-interview.png", 75, (95, 335, 735, 512),
        "입학사정관 2인 1조 · 학생부 기반 블라인드 · 10분 내외")
    cap(HERE / "chosun-2027-criteria.png", 75, (95, 580, 735, 835),
        "평가 영역 인성·적성 · 당해 연도 문제는 사전 비공개")
    cap(HERE / "chosun-2027-blind.png", 75, (190, 865, 735, 980),
        "교복·개인정보 확인 가능한 복장 금지 · 개인정보 언급 금지")
    make_structure(HERE / "structure-chosun.png", [
        "토목공학과에 지원한 이유는 비가 많이 온 날 학교 앞 도로가 잠기는 것을 보고, 물이 빠지는 길을 설계하는 일에 관심이 생겼기 때문입니다.",
        "1학년 통합사회 '자연환경과 인간' 단원 모둠 탐구에서 저는 학교 주변 빗물받이 위치를 지도에 표시하는 일을 맡았고, 물이 고이는 곳 근처의 빗물받이가 낙엽으로 막혀 있다는 것을 찾았습니다.",
        "구조물을 새로 만드는 것만큼 이미 있는 시설을 관리하는 일이 중요하다는 것을 배웠습니다.",
        "토목공학과에서 수리학과 도시 배수 설계를 배워, 비가 많이 와도 안전한 길을 만드는 기술자가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_chosun()
