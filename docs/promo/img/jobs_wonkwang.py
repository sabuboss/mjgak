# 원광대 학생부종합전형(면접 실시 모집단위) 블로그 글(naver-116) 이미지. python jobs_wonkwang.py
# src/m_원광대학교.pdf = 원광대 입학처(ipsi.wku.ac.kr) 수시 모집요강 게시물의
#   "2027학년도 원광대학교 수시모집요강_low_V10.pdf"(서버 파일명 20260908040506009_..., 92쪽, PDF 수정일 2026-09-08).
# 인쇄 쪽수 = PDF 쪽수 (본문 안 "21페이지", "33페이지", "51페이지" 참조가 PDF 쪽과 맞고, 머리말의 "32 33" 표기도 같다).
# 이 PDF 는 글자 층이 있지만 표 글자 순서가 뒤섞여 문구 검색 자르기가 불안정하다.
# 그래서 jobs_dau.py 의 cap() 을 복사해, 좌표(110dpi 픽셀)로 자른다. 여러 상자를 위아래로 붙일 수 있게 boxes 를 받는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_원광대학교.pdf")
U, LBL = "원광대학교", "2027학년도 수시모집요강"
PX = 72 / 110  # 110dpi 픽셀 -> PDF 포인트


def _shot(page, box, dpi):
    pg = pymupdf.open(PDF)[page - 1]
    x0, y0, x1, y1 = (v * PX for v in box)
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def cap(out, page, boxes, doc_label, note, dpi=200, gap=18):
    """promo_style.make_capture 와 같은 틀. boxes=[(x0, y0, x1, y1), ...] 110dpi 픽셀, 같은 쪽에서 위아래로 붙인다."""
    if isinstance(boxes[0], (int, float)):
        boxes = [boxes]
    shots = [_shot(page, b, dpi) for b in boxes]
    sw = max(s.width for s in shots)
    sh = sum(s.height for s in shots) + gap * (len(shots) - 1)
    shot = Image.new("RGB", (sw, sh), "white")
    y = 0
    for i, s in enumerate(shots):
        shot.paste(s, (0, y))
        y += s.height
        if i < len(shots) - 1:
            ImageDraw.Draw(shot).line([(20, y + gap // 2), (sw - 20, y + gap // 2)], fill=LINE, width=2)
            y += gap
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


def jobs_wonkwang():
    make_thumb(HERE / "thumb-wonkwang.png", "원광대 면접", line2="학생부종합전형", line3="예상 질문 7개 총정리")
    cap(HERE / "wonkwang-2027-units.png", 24, (85, 300, 822, 712),
        f"{LBL} 24쪽", "학생부종합 58명 · 지역인재종합 178명(면접 학과) · 응급구조학과는 면접 없음")
    cap(HERE / "wonkwang-2027-target.png", 33, (100, 112, 850, 602),
        f"{LBL} 33쪽", "면접은 원불교·의예·치의예·한의예·약학·한약학만 · 5배수")
    cap(HERE / "wonkwang-2027-method.png", 35, (100, 382, 850, 748),
        f"{LBL} 35쪽", "1단계 서류 100% 5배수 · 2단계 1단계 700 + 면접 300")
    cap(HERE / "wonkwang-2027-schedule.png", 30, [(85, 500, 825, 864), (85, 1100, 825, 1218)],
        f"{LBL} 30쪽", "1단계 11/20(금) · 면접 12/1(화)·12/2(수) · 최종 12/18(금)")
    cap(HERE / "wonkwang-2027-interview.png", 33, (100, 622, 850, 1212),
        f"{LBL} 33쪽", "발전가능성 40 · 인성 및 가치관 33.3 · 의사소통능력 26.7")
    cap(HERE / "wonkwang-2027-rules.png", 18, (85, 486, 830, 692),
        f"{LBL} 18쪽", "실물 신분증 지참(모바일 불인정) · 전자기기 사용 불가 · 일정 변경 불가")
    cap(HERE / "wonkwang-2027-minimum.png", 35, (100, 758, 850, 1210),
        f"{LBL} 35쪽", "학생부종합 수능 최저 · 원불교학과는 최저 없음")
    cap(HERE / "wonkwang-2027-local.png", 37, (100, 282, 850, 616),
        f"{LBL} 37쪽", "지역인재종합 지원자격 · 전북권·호남권 · 한약학과는 비수도권")
    make_structure(HERE / "structure-wonkwang.png", [
        "한약학과에 지원한 이유는 식물에서 얻은 재료가 약이 되려면 성분과 품질을 과학적으로 다뤄야 한다는 것을 탐구 활동에서 느꼈기 때문입니다.",
        "2학년 생명과학 동아리에서 같은 녹차 잎을 물 온도만 바꿔 우려 보았는데, 뜨거운 물일수록 색이 진하고 맛이 썼습니다.",
        "같은 재료라도 다루는 조건에 따라 우러나는 성분이 달라진다는 것을 알았고, 그 뒤로 실험마다 조건을 빠짐없이 기록하는 습관이 생겼습니다.",
        "한약학과에서 한약재의 성분과 품질 관리를 제대로 배워, 믿고 쓸 수 있는 한약을 만드는 한약사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_wonkwang()
