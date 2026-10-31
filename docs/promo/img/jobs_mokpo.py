# 국립목포대 학생부종합 지역인재(종합)·미래인재전형 면접 블로그 글(naver-105) 이미지. python jobs_mokpo.py
# src/m_국립목포대학교.pdf = 국립목포대 입학처(ipsi.mokpo.ac.kr) 수시 모집요강 페이지의 PDF
#   (2027학년도 국립목포대학교 신입생 수시모집요강, 86쪽, PDF 작성 2026-09-02, sha1 77f91556…).
# 인쇄 쪽수 = PDF 쪽수 - 2 (예: PDF 45쪽 = 인쇄 43쪽).
# 이 PDF 는 1·28쪽 말고는 글자 층이 없는 이미지라 텍스트 검색이 안 된다.
# 그래서 promo_style.make_capture(문구 검색) 대신, 같은 틀을 쓰되 좌표로 자르는 cap() 을 여기에 둔다(견본 jobs_dau.py).
# 좌표는 150dpi 로 렌더한 쪽 이미지의 픽셀 값(x0, y0, x1, y1)이다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_국립목포대학교.pdf")
U, LBL = "국립목포대학교", "2027학년도 신입생 수시모집요강"
PX = 72 / 150  # 150dpi 픽셀 -> PDF 포인트


def lbl(printed):
    return f"{LBL} {printed}쪽(PDF {printed + 2}쪽)"


def cap(out, page, box, doc_label, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. page=PDF 쪽(1부터), box=(x0, y0, x1, y1) 150dpi 픽셀."""
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


def jobs_mokpo():
    make_thumb(HERE / "thumb-mokpo.png", "목포대 면접", line2="지역인재·미래인재전형", line3="공개 질문 10개 총정리")
    cap(HERE / "mokpo-2027-units.png", 42, (105, 245, 1185, 893),
        lbl(40), "지역인재(종합) 38명 · 미래인재(전문학사) 79명 · 장애인 6명")
    cap(HERE / "mokpo-2027-method.png", 43, (105, 462, 1185, 772),
        lbl(41), "1단계 서류 100% 6배수 · 2단계 1단계 80% + 면접 20%")
    cap(HERE / "mokpo-2027-schedule.png", 28, (105, 256, 1180, 1172),
        lbl(26), "1단계 11/13(금) · 면접 11/27(금) · 장애인 11/28(토)")
    cap(HERE / "mokpo-2027-interview.png", 44, (105, 432, 1185, 1000),
        lbl(42), "발전가능성 40 · 학교생활(태도) 30 · 학업외소양 30 · 10분 이내")
    cap(HERE / "mokpo-2027-questions.png", 45, (105, 112, 1185, 870),
        lbl(43), "대학이 공개한 면접평가 공통(예시) 문항 10개")
    cap(HERE / "mokpo-2027-notice.png", 45, (105, 878, 1185, 1600),
        lbl(43), "결시자 불합격 · 수험표·신분증 · 약학과만 수능 최저")
    cap(HERE / "mokpo-2027-multi.png", 32, (105, 160, 1180, 685),
        lbl(30), "최대 6개 전형 · 지역인재(종합)과 미래인재는 중복 지원 불가")
    make_structure(HERE / "structure-mokpo.png", [
        "간호학과에 지원한 계기는 보건 동아리의 경로당 건강 체조 봉사에서, 설명 한마디가 어르신의 생활을 바꾸는 것을 본 일입니다.",
        "처음에는 동작만 보여 드렸는데 따라 하기 힘들어하셔서, 의자에 앉아 하는 동작으로 바꾸고 동작마다 어디에 좋은지 한 줄씩 설명했습니다.",
        "다음 방문 때 집에서도 해 봤다고 먼저 말씀하시는 분이 생겼고, 돌봄은 상대가 혼자서도 할 수 있게 돕는 일이라는 것을 배웠습니다.",
        "간호학과에서 전문 지식을 제대로 배워, 지역 어르신이 스스로 건강을 관리하도록 돕는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_mokpo()
