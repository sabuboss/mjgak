# 동아대 학생부종합 잠재능력우수자전형 블로그 글(naver-102) 이미지. python jobs_dau.py
# src/m_동아대학교.pdf = 동아대 입학안내 홈페이지(ent.donga.ac.kr) 2027학년도 수시모집 신입생 모집요강(2026-08-27 게시).
# 인쇄 쪽수 = PDF 쪽수. 이 PDF 는 글자가 윤곽선(벡터)으로 되어 있어 텍스트 검색이 안 된다.
# 그래서 promo_style.make_capture(문구 검색) 대신, 같은 틀을 쓰되 좌표로 자르는 cap() 을 여기에 복사해 쓴다.
# 좌표는 110dpi 로 렌더한 쪽 이미지의 픽셀 값(x0, y0, x1, y1)이다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_동아대학교.pdf")
U, LBL = "동아대학교", "2027학년도 수시모집요강"
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


def jobs_dau():
    make_thumb(HERE / "thumb-dau.png", "동아대 면접", line2="잠재능력우수자", line3="예상 질문 7개 총정리")
    cap(HERE / "dau-2027-units.png", 30, (75, 160, 880, 352),
        f"{LBL} 30쪽", "잠재능력우수자전형 512명(정원 내)")
    cap(HERE / "dau-2027-method.png", 40, (75, 248, 880, 612),
        f"{LBL} 40쪽", "1단계 서류 100% 5배수 · 2단계 1단계 60% + 면접 40% · 수능 면제")
    cap(HERE / "dau-2027-interview.png", 40, (280, 622, 880, 1140),
        f"{LBL} 40쪽", "면접 400점: 학업 100 · 진로 200 · 공동체 100 · 2인 1조 10분 내외")
    cap(HERE / "dau-2027-tie.png", 41, (75, 338, 880, 660),
        f"{LBL} 41쪽", "1단계 동점자 모두 선발 · 면접 결시자는 불합격")
    cap(HERE / "dau-2027-schedule.png", 29, (78, 612, 470, 882),
        f"{LBL} 29쪽", "1단계 11/20 14시 · 면접 11/27·28")
    cap(HERE / "dau-2027-rules.png", 35, (75, 700, 880, 905),
        f"{LBL} 35쪽", "수험표·신분증·필기도구 지참 · 지각 입실 불가 · 전자기기 소지 불가")
    cap(HERE / "dau-2027-medical.png", 48, (280, 1010, 880, 1140),
        f"{LBL} 48쪽", "의예과 지역인재종합: 1차·2차 면접 각 2인 1조 7분 내외")
    make_structure(HERE / "structure-dau.png", [
        "기계공학과에 지원한 이유는 기계가 힘을 바꿔 전달하는 원리를 제 손으로 확인해 본 경험 때문입니다.",
        "2학년 물리 시간에 일과 에너지를 배운 뒤, 동아리에서 자전거 기어를 바꿔 가며 같은 거리를 가는 데 필요한 페달 회전 수를 세어 표로 정리했습니다.",
        "가벼운 기어일수록 페달은 쉬웠지만 더 많이 돌려야 해서, 힘을 줄이면 그만큼 움직이는 거리가 늘어난다는 것을 숫자로 확인했습니다.",
        "기계공학과에서 동력 전달과 기계 설계를 배워, 적은 힘으로 효율 좋게 움직이는 장치를 만들고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dau()
