# 영남대 학생부교과 창의인재전형 면접 블로그 글(naver-109) 이미지. python jobs_yeungnam.py
# src/m_영남대학교.pdf = 영남대 입학안내 홈페이지(enter.yu.ac.kr) 수시 모집요강 메뉴의 PDF
#   (2027학년도 수시 신입생 모집요강, 80쪽, InDesign 2026-08-04 작성, 서버 Last-Modified 2026-08-18).
# 인쇄 쪽수 = PDF 쪽수. 이 PDF 는 8쪽 말고는 글자 층이 없어 텍스트 검색이 안 된다.
# 그래서 promo_style.make_capture(문구 검색) 대신, 같은 틀을 쓰되 좌표로 자르는 cap() 을 여기에 복사해 쓴다(견본 jobs_dau.py).
# 좌표는 110dpi 로 렌더한 쪽 이미지(910x1287)의 픽셀 값(x0, y0, x1, y1)이다.
# 쪽 오른쪽 위 캐릭터 그림과 쪽 아래 캠퍼스 사진은 잘라 넣지 않는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_영남대학교.pdf")
U, LBL = "영남대학교", "2027학년도 수시 신입생 모집요강"
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


def jobs_yeungnam():
    make_thumb(HERE / "thumb-yeungnam.png", "영남대 면접", line2="창의인재전형", line3="예상 질문 7개 총정리")
    cap(HERE / "yeungnam-2027-change.png", 11, (80, 685, 828, 848),
        f"{LBL} 11쪽", "창의인재전형에 전공자유선택학부 인문 15 · 자연 18 신설")
    cap(HERE / "yeungnam-2027-units.png", 27, (80, 148, 828, 652),
        f"{LBL} 27쪽", "의예 8 · 전공자유 인문 15 · 자연 18 · 최저 2개 합 8")
    cap(HERE / "yeungnam-2027-method.png", 27, (80, 652, 828, 1105),
        f"{LBL} 27쪽", "1단계 학생부 100% 5배수 · 2단계 1단계 70% + 면접 30%")
    cap(HERE / "yeungnam-2027-schedule.png", 15, (85, 150, 825, 777),
        f"{LBL} 15쪽", "전공자유선택학부 면접 11/21(토) · 합격자 발표 12/18(금)")
    cap(HERE / "yeungnam-2027-interview.png", 28, (80, 115, 828, 838),
        f"{LBL} 28쪽", "11/21(토) 09:00 경산캠퍼스 · 인성·창의성·전공적합성 종합")
    cap(HERE / "yeungnam-2027-major.png", 8, (80, 290, 402, 568),
        f"{LBL} 8쪽", "평점 3.0 이상 원하는 전공")
    cap(HERE / "yeungnam-2027-med-local.png", 32, (80, 572, 828, 704),
        f"{LBL} 32쪽", "지역인재 의예과 11/28(토) 09:00 · 학생부·제시문 바탕")
    cap(HERE / "yeungnam-2027-med-doctor.png", 34, (80, 512, 828, 672),
        f"{LBL} 34쪽", "지역의사선발 11/28(토) 15:00 · 제시문 바탕 공동체역량")
    make_structure(HERE / "structure-yeungnam.png", [
        "전공자유선택학부에 지원한 이유는 관심 있는 두 분야를 직접 배워 본 뒤 전공을 고르고 싶기 때문입니다.",
        "2학년 때 지역 전통시장 방문객이 줄어든 이유를 조사하면서, 상인 인터뷰는 사회문화 시간에, 방문객 통계는 확률과 통계 시간에 배운 방법으로 정리했습니다.",
        "같은 문제도 사람의 이야기와 숫자를 함께 봐야 원인이 보인다는 것을 배웠고, 경영과 사회학 중 어느 쪽이 제게 맞는지 아직 확인하고 싶습니다.",
        "1년 동안 두 분야의 기초 과목을 듣고 학사지도교수님과 상담해, 근거를 갖고 전공을 정하겠습니다.",
    ])


if __name__ == "__main__":
    jobs_yeungnam()
