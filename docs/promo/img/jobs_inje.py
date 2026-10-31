# 인제대 학생부교과 지역인재Ⅰ전형(간호학과·약학과) 면접 블로그 글(naver-110) 이미지. python jobs_inje.py
# src/m_인제대학교.pdf = 인제대 입학홈페이지(iphak.inje.ac.kr) 수시 모집요강 PDF
#   (pds/mojib/1283_2027 인제대 수시요강-웹 업로드용, 80쪽, PDF 수정일 2026-08-14). 2026-10-31 받음.
# 인쇄 쪽수 = PDF 쪽수. 이 PDF 는 글자가 윤곽선이라 텍스트 검색이 안 된다.
# 그래서 promo_style.make_capture(문구 검색) 대신, jobs_dau.py 의 cap() 과 같은 틀로 좌표를 잘라 쓴다.
# 좌표는 120dpi 로 렌더한 쪽 전체 이미지의 픽셀 값(x0, y0, x1, y1)이다(쪽 크기 992 x 1403).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_인제대학교.pdf")
U, LBL = "인제대학교", "2027학년도 수시 모집요강"
PX = 72 / 120  # 120dpi 픽셀 -> PDF 포인트


def cap(out, page, box, doc_label, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. box=(x0, y0, x1, y1) 120dpi 픽셀."""
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


def jobs_inje():
    make_thumb(HERE / "thumb-inje.png", "인제대 면접", line2="지역인재Ⅰ간호·약학", line3="공개 질문 7개 총정리")
    cap(HERE / "inje-2027-units.png", 12, (72, 255, 872, 612),
        f"{LBL} 12쪽", "지역인재Ⅰ 의예 31 · 약학 6 · 간호 25 · 의예·약학 약학 8")
    cap(HERE / "inje-2027-local1-method.png", 21, (112, 818, 922, 1178),
        f"{LBL} 21쪽", "1단계 교과 100% 5배수 · 2단계 1단계 80 + 면접 20")
    cap(HERE / "inje-2027-schedule.png", 11, (120, 517, 918, 810),
        f"{LBL} 11쪽", "1단계 11/4(수) 14시 · 간호·약학 11/21(토) · 의예 11/28")
    cap(HERE / "inje-2027-nursing-interview.png", 44, (72, 130, 872, 585),
        f"{LBL} 44쪽", "간호학과 심층면접 · 2명당 10분 · 1분 준비 후 9분")
    cap(HERE / "inje-2027-pharm-interview.png", 43, (120, 802, 918, 1330),
        f"{LBL} 43쪽", "약학과 심층면접 · 1명당 10분 · 1분 준비 후 9분")
    cap(HERE / "inje-2027-rules.png", 45, (120, 258, 918, 682),
        f"{LBL} 45쪽", "면접 결시 불합격 · 면접위원 2인 이상 0점이면 불합격")
    cap(HERE / "inje-2027-med-mmi.png", 43, (120, 130, 918, 778),
        f"{LBL} 43쪽", "의예과 MMI 질문 예시 · 면접실 밖 2분 준비 후 8분 면접")
    make_structure(HERE / "structure-inje.png", [
        "인제대 간호학과에 지원한 이유는 제가 사는 지역에서 사람을 곁에서 돌보는 간호사가 되고 싶기 때문입니다.",
        "2학년 때 할머니가 무릎 수술 뒤 퇴원하셨을 때, 약 먹는 시간을 자꾸 잊으셔서 요일별 약통에 색 스티커를 붙여 드렸습니다.",
        "그 뒤로 거르는 날이 줄었고, 돌봄은 크게 돕는 일보다 상대가 혼자서도 할 수 있게 만드는 일이라는 것을 배웠습니다.",
        "인제대 간호학과에서 환자 교육을 제대로 배워 부산·울산·경남 지역 환자 곁을 지키는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_inje()
