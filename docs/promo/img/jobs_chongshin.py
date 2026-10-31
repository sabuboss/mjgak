# 총신대 학생부종합 코람데오인재 면접 블로그 글(naver-103) 이미지. python jobs_chongshin.py
# src/m_총신대학교.pdf = 총신대학교 2027학년도 수시모집요강(최종), 45쪽, 2026-05-29 작성.
# 인쇄 쪽수 = PDF 쪽수 - 1 (PDF 1쪽 표지, PDF 2쪽 목차).
# 이 PDF 는 글자 층이 없어(쪽 번호만 추출됨) 텍스트 검색이 안 된다.
# 그래서 promo_style.make_capture(문구 검색) 대신, 같은 틀을 쓰되 좌표로 자르는 cap() 을 여기에 둔다(jobs_dau.py 와 같은 방식).
# 좌표는 110dpi 로 렌더한 쪽 이미지의 픽셀 값(x0, y0, x1, y1)이다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

PDF = str(SRC / "m_총신대학교.pdf")
U, LBL = "총신대학교", "2027학년도 수시모집요강"
PX = 72 / 110  # 110dpi 픽셀 -> PDF 포인트


def cap(out, printed, box, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. printed=인쇄 쪽수, box=(x0, y0, x1, y1) 110dpi 픽셀."""
    pg = pymupdf.open(PDF)[printed]  # 인쇄 n쪽 = PDF n+1쪽 = 인덱스 n
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
    text_fixed(d, (40, fy + 10), f"출처: {U} {LBL} {printed}쪽(PDF {printed + 1}쪽)", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_chongshin():
    make_thumb(HERE / "thumb-chongshin.png", "총신대 면접", line2="코람데오인재", line3="예상 질문 7개 총정리")
    cap(HERE / "chongshin-2027-coramdeo-units.png", 12, (62, 84, 850, 512),
        "코람데오인재 121명 · 신학과 37 · 유아교육과 20 · 수능최저 없음")
    cap(HERE / "chongshin-2027-coramdeo-method.png", 12, (62, 528, 850, 1072),
        "1단계 서류 100% 3배수 · 2단계 1단계 70 + 구술면접 30")
    cap(HERE / "chongshin-2027-docs-eval.png", 25, (62, 92, 850, 516),
        "서류평가 학업역량 30 · 진로역량 30 · 공동체역량 40")
    cap(HERE / "chongshin-2027-schedule.png", 7, (62, 560, 834, 1124),
        "코람데오인재 1단계 11/4(수) · 면접 11/14(토) · 발표 12/18(금)")
    cap(HERE / "chongshin-2027-first.png", 8, (62, 82, 850, 400),
        "1단계 합격자 발표 11/4(수) 15:00 · 입학 홈페이지 공고")
    cap(HERE / "chongshin-2027-interview.png", 26, (62, 380, 850, 784),
        "출제지문 답변 + 제출서류 진위 확인 · 2:1 · 10분 내외")
    cap(HERE / "chongshin-2027-rules.png", 28, (62, 594, 850, 872),
        "결시·F 불합격 · 수험표 가슴 부착 · 모바일 기기 금지")
    cap(HERE / "chongshin-2027-multi.png", 2, (62, 236, 850, 626),
        "전형일이 다른 전형 간 복수지원 가능 · 같은 날 전형은 불가")
    make_structure(HERE / "structure-chongshin.png", [
        "이 글이 말하는 섬김은 큰일보다 상대에게 지금 필요한 작은 일을 먼저 찾는 것이라고 생각합니다.",
        "중등부 교사 보조로 섬길 때, 예배에 자주 늦던 후배가 아침을 거르고 온다는 것을 알고 예배 전에 간단한 간식을 함께 준비하자고 교사회에 제안했습니다.",
        "그 뒤 후배가 제시간에 오는 날이 늘었고, 말씀을 전하기 전에 그 사람의 형편을 먼저 살피는 것이 섬김의 시작이라는 것을 배웠습니다.",
        "신학과에서 말씀을 깊이 배워, 말씀과 삶이 함께 가는 사역자가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_chongshin()
