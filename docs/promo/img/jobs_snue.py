# 서울교대 학생부종합 교직인성우수자전형 블로그 글 이미지. python jobs_snue.py
# 인쇄 쪽수 = PDF 쪽수 - 2. PDF 4쪽(인쇄 2쪽)은 90도 돌아간 가로 쪽이라 capture_rotated 로 자른다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pymupdf
from PIL import Image, ImageDraw
from promo_style import (HERE, SRC, make_thumb, make_capture, make_structure,
                         font, text_fixed, NAVY, NAVY_D, BG, LINE, GRAY, ACCENT)

P = str(SRC / "m_서울교육대학교.pdf")
U, LBL = "서울교육대학교", "2027학년도 수시모집요강"


def capture_rotated(out, pdf, page, box, univ, doc_label, note, dpi=200):
    """돌아간 쪽을 화면에 보이는 방향으로 렌더링한 뒤 box(보이는 방향 기준 pt 좌표 x0,y0,x1,y1)로 자른다.
    틀은 promo_style.make_capture 와 같다."""
    pg = pymupdf.open(pdf)[page - 1]
    pix = pg.get_pixmap(dpi=dpi)
    full = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    s = dpi / 72
    shot = full.crop(tuple(int(v * s) for v in box))
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
    d.text((40 + cw + 70, 30), univ, font=font(38, True), fill="white")
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    fy = HEAD + shot.height + 40
    text_fixed(d, (40, fy + 10), f"출처: {univ} {doc_label}", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_snue():
    make_thumb(HERE / "thumb-snue.png", "서울교대 면접", line2="교직인성우수자", line3="예상 질문 7개 총정리")
    capture_rotated(HERE / "snue-2027-tc-change.png", P, 4, (66, 108, 776, 518),
                    U, f"{LBL} 2쪽(PDF 4쪽)", "교직인성우수자 100명→150명 · 최저 4개 합 10 → 2개 합 6")
    make_capture(HERE / "snue-2027-tc-method.png", P, 13, "학생부종합", ("after", "동점자가 발생할 경우 모두 선발"),
                 U, f"{LBL} 11쪽(PDF 13쪽)", "150명 · 1단계 서류 100% 2배수 · 2단계 1단계 500 + 면접 500",
                 start_pad=14, end_pad=8, lr=40)
    make_capture(HERE / "snue-2027-tc-document.png", P, 13, "서류평가 방법", ("after", "교직 진로를 위한"),
                 U, f"{LBL} 11쪽(PDF 13쪽)", "서류평가: 학업 역량 40 · 인성 역량 20 · 교직 역량 40",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "snue-2027-tc-schedule.png", P, 7, "구분", 555,
                 U, f"{LBL} 5쪽(PDF 7쪽)", "1단계 11/13(금) 10시 · 면접 11/21(토) · 최초 합격 12/18(금)",
                 start_pad=8, end_pad=0, lr=40)
    make_capture(HERE / "snue-2027-tc-interview.png", P, 14, "면접 평가", "사정 원칙",
                 U, f"{LBL} 12쪽(PDF 14쪽)", "학생부 기반 60 · 교직 적·인성 40 · 최저 2개 합 6 + 한국사 4",
                 start_pad=10, end_pad=14, lr=40)
    make_capture(HERE / "snue-2027-tc-rules.png", P, 9, "면접평가 시 유의", "기타 사항",
                 U, f"{LBL} 7쪽(PDF 9쪽)", "일시 변경 불가 · 신분증 · 신상 언급 불이익 · 자기소개 없음",
                 start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "snue-2027-tc-principal.png", P, 12, "복수의 면접위원", "사정원칙",
                 U, f"{LBL} 10쪽(PDF 12쪽)", "학교장추천 면접: 교직 적·인성 · 최저 2개 합 6 + 한국사 4",
                 start_pad=32, end_pad=14, lr=40)
    make_structure(HERE / "structure-snue.png", [
        "교사라는 진로를 확인한 활동은 2학년 때 초등학생 독서 멘토링입니다.",
        "처음에는 책을 읽어 주기만 했는데, 아이들이 내용을 거의 기억하지 못했습니다.",
        "한 장마다 다음 장면을 맞혀 보게 했더니, 아이들이 먼저 책장을 넘기자고 했습니다.",
        "교대에서 아이가 스스로 읽게 만드는 수업 방법을 제대로 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_snue()
