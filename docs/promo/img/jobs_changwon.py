# 국립창원대 학생부종합 계열적합인재전형 블로그 글(naver-111) 이미지. python jobs_changwon.py
# src/m_국립창원대학교.pdf = 국립창원대 입학 홈페이지(ipsi.changwon.ac.kr) 입학안내 > 수시모집
#   「2027학년도 국립창원대학교 창원캠퍼스 수시모집요강」 PDF(56쪽, 2026-07-06 작성, 2026-10-31 받음).
# 이 PDF 는 글자 층이 없고(텍스트 검색 불가), 한 PDF 쪽에 인쇄 쪽 두 개가 좌우로 들어 있다.
#   인쇄 쪽 p 는 PDF (p // 2) + 1 쪽에 있다. 짝수 쪽 = 왼쪽 절반, 홀수 쪽 = 오른쪽 절반(x 595pt 부터).
# 그래서 promo_style.make_capture(문구 검색) 대신, 같은 틀의 cap() 을 여기에 복사해 좌표(PDF 포인트)로 자른다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_국립창원대학교.pdf")
U, LBL = "국립창원대학교", "2027학년도 창원캠퍼스 수시모집요강"


def cap(out, printed, box, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. printed=인쇄 쪽수, box=(x0, y0, x1, y1) PDF 포인트(펼침면 기준)."""
    page = printed // 2 + 1
    pg = pymupdf.open(PDF)[page - 1]
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(*box))
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


def jobs_changwon():
    make_thumb(HERE / "thumb-changwon.png", "창원대 면접", line2="계열적합인재전형", line3="예상 질문 7개 총정리")
    cap(HERE / "changwon-2027-method.png", 45, (672, 60, 1155, 405),
        "191명 · 1단계 서류 4배수 · 2단계 1단계 600 + 면접 400 · 최저 없음")
    cap(HERE / "changwon-2027-changes.png", 34, (36, 375, 515, 618),
        "간호학과 계열적합인재 15명(8명 증) · 1단계 3배수")
    cap(HERE / "changwon-2027-docs.png", 45, (672, 418, 1155, 725),
        "1단계 서류평가: 학업 30% · 진로 50% · 공동체 20%")
    cap(HERE / "changwon-2027-schedule.png", 35, (676, 304.5, 1152, 466.5),
        "1단계 11/13(금) 10시 예정 · 면접 11/24(화) 10시 · 발표 12/18")
    cap(HERE / "changwon-2027-interview.png", 84, (36, 320, 515, 535),
        "1인당 10분 내외 · 학생부 중심 · 의사소통능력 30%")
    cap(HERE / "changwon-2027-rules.png", 29, (676, 70, 1155, 212),
        "수험표·공적신분증 지참 · 휴대폰 등 전자기기 소지 불가")
    cap(HERE / "changwon-2027-special.png", 84, (36, 128, 515, 318),
        "특수교육대상자: 5~10분 내외 · 학과별 전공부분 문제 구술")
    make_structure(HERE / "structure-changwon.png", [
        "간호학과에 지원한 이유는 아픈 사람의 상태를 정확히 기록해 전하는 일이 간호의 중요한 부분이라는 것을 학교에서 직접 봤기 때문입니다.",
        "2학년 체육대회 날 보건 부스에서 보건 선생님을 도우며, 찾아온 학생의 이름과 시간, 불편한 곳을 기록하는 일을 맡았습니다.",
        "처음에는 '배가 아픔'처럼만 적었는데, 언제부터 어디가 아픈지까지 적어야 선생님이 판단하기 쉽다는 말씀을 듣고 기록 칸을 나눠 다시 만들며 정확한 기록이 다음 사람의 판단을 돕는다는 것을 배웠습니다.",
        "간호학과에서 환자를 관찰하고 기록하는 법을 제대로 배워, 의료진이 믿고 쓸 수 있는 정보를 전하는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_changwon()
