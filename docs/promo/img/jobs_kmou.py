# 국립한국해양대 학생부교과 지역인재전형 면접 블로그 글(naver-112) 이미지. python jobs_kmou.py
# src/m_국립한국해양대학교.pdf = 국립한국해양대 입학정보 홈페이지 모집요강 페이지의 "PDF 다운로드"
#   (/common/nttFileDownload.do?fileKey=5800d328..., 64쪽, 300dpi 이미지, PDF 정보상 2026-06-12 작성).
# 인쇄 쪽수 = PDF 쪽수. 이 PDF 는 쪽 전체가 이미지라 글자 층이 없다(텍스트 검색 불가).
# 그래서 promo_style.make_capture(문구 검색) 대신 jobs_dau.py 의 cap()(좌표로 자르기)을 복사해 쓴다.
# 좌표는 110dpi 로 렌더한 쪽 이미지의 픽셀 값(x0, y0, x1, y1)이다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_국립한국해양대학교.pdf")
U, LBL = "국립한국해양대학교", "2027 신입생 수시 모집요강"
PX = 72 / 110  # 110dpi 픽셀 -> PDF 포인트


def cap(out, page, box, doc_label, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. box=(x0, y0, x1, y1) 110dpi 픽셀."""
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
    text_fixed(d, (40, fy + 10), f"출처: {U} {doc_label}", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_kmou():
    make_thumb(HERE / "thumb-kmou.png", "한국해양대", line2="지역인재전형 면접", line3="예상 질문 6개 총정리")
    cap(HERE / "kmou-2027-jiyeok-method.png", 16, (60, 105, 808, 672),
        f"{LBL} 16쪽", "지역인재 117명 · 1단계 교과 100% 5배수 · 2단계 80 + 면접 20")
    cap(HERE / "kmou-2027-jiyeok-interview.png", 16, (60, 678, 808, 1168),
        f"{LBL} 16쪽", "면접: 기본소양(지원동기, 고교생활, 학업계획) · 결시자 불합격")
    cap(HERE / "kmou-2027-units.png", 11, (62, 165, 906, 1048),
        f"{LBL} 11쪽", "지역인재: 해사 43 · 해양과학기술 19 · 해양공과 35 · 인문사회 20")
    cap(HERE / "kmou-2027-schedule.png", 12, (60, 162, 808, 706),
        f"{LBL} 12쪽", "1단계 10/28 · 지역인재 면접 11/26(목) · 합격자 발표 12/18")
    cap(HERE / "kmou-2027-tie.png", 30, (60, 662, 808, 826),
        f"{LBL} 30쪽", "지역인재 동점자: 면접점수 → 교과 계열별 순위")
    cap(HERE / "kmou-2027-health.png", 14, (60, 55, 808, 462),
        f"{LBL} 14쪽", "해사대학: 건강진단서 원본, 한 항목이라도 부적합이면 불합격")
    make_structure(HERE / "structure-kmou.png", [
        "기관시스템공학부에 지원한 동기는 배를 움직이는 기관이 연료의 에너지를 얼마나 일로 바꾸는지 직접 따져 본 경험 때문입니다.",
        "2학년 물리학Ⅰ에서 열기관은 흡수한 열의 일부만 일로 바꾸고 나머지는 내보낸다는 것과 열효율을 배운 뒤, 과학 동아리에서 큰 선박 엔진 자료를 찾아봤습니다.",
        "버려지는 배기가스의 열을 다시 써서 효율을 높이는 장치가 있다는 것을 알았고, 기관은 만드는 것만큼 잘 관리하는 일이 중요하다는 것을 배웠습니다.",
        "기관시스템공학부에서 선박 기관의 원리와 운전을 배워, 배가 연료를 덜 쓰고 안전하게 움직이도록 관리하는 기관사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_kmou()
