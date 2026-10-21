# 수능 끝나고 면접 보는 대학 총정리(2027 수시, 날짜별) 블로그 글 이미지. python jobs_after.py
# 날짜는 각 대학 2027학년도 수시모집요강 전형일정 표에서 직접 확인(쪽수는 ROWS 의 "pg" 칸, 인쇄 쪽수 기준).
# "수능 뒤 N일" = 면접일 - 수능일(2026-11-19), 이 글에서 계산한 값.
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200
CSAT = date(2026, 11, 19)
PRE, DAY, POST = "수능 전", "수능 당일", "수능 후"

# (면접일 줄들, 대학, 전형, 1단계 발표, 수능 전/후, 근거 쪽, 면접 첫날 (m,d), 면접 마지막날 (m,d))
ROWS1 = [
    (["11/21(토)"], "서울교대", "교직인성우수자·학교장추천 등", "11/13(금) 10:00", PRE, "5쪽", (11, 21), (11, 21)),
    (["11/21(토)"], "을지대", "EU면접형 · 성남캠퍼스", "11/18(수)", PRE, "11쪽", (11, 21), (11, 21)),
    (["11/21(토)"], "인천대", "자기추천", "11/6(금)", PRE, "7쪽", (11, 21), (11, 21)),
    (["11/21(토)"], "경북대", "학생부종합 단계별 전형", "11/6(금) 16:00", PRE, "4쪽", (11, 21), (11, 21)),
    (["11/21(토)·22(일)", "모집단위별"], "덕성여대", "덕성인재Ⅱ", "11/12(목)", PRE, "12쪽", (11, 21), (11, 22)),
    (["11/21(토)·22(일)", "모집단위별"], "이화여대", "미래인재(면접형)", "11/12(목)", PRE, "9쪽", (11, 21), (11, 22)),
    (["11/21(토)·22(일)", "단과대학별"], "인하대", "인하미래인재(면접형)", "11/17(화)", PRE, "8쪽", (11, 21), (11, 22)),
    (["11/21 자연계", "11/22 인문·예체능계"], "국민대", "국민프런티어", "11/17(화) 14:00 예정", PRE, "10쪽", (11, 21), (11, 22)),
    (["11/21 창의소프트학부", "11/22 인문·자연계열"], "세종대", "세종인재(면접형)", "11/13(금)", PRE, "8쪽", (11, 21), (11, 22)),
    (["11/21 서울캠퍼스", "11/22 글로벌캠퍼스"], "한국외대", "학생부종합(면접형)", "11/16(월)", PRE, "19쪽", (11, 21), (11, 22)),
    (["11/21·22·28·29", "모집단위별"], "성신여대", "자기주도인재", "11/13(금) 10:00 예정", PRE, "10쪽", (11, 21), (11, 29)),
    (["11/22 공과대학 등", "12/5 의대 · 12/6 사범대"], "한양대", "학생부종합(면접형)", "11/13(금) 예정", PRE, "PDF 8쪽", (11, 22), (12, 6)),
    (["11/22·28·29", "단과대학별"], "아주대", "ACE (의학과·약학과 제외)", "11/17(화)", PRE, "6쪽", (11, 22), (11, 29)),
    (["11/25(수)~26(목)"], "경상국립대", "학생부종합 일반전형(면접 모집단위)", "11/13(금) 16:00", PRE, "13쪽", (11, 25), (11, 26)),
    (["11/26(목)"], "전북대", "큰사람", "11/20(금) 14:00 예정", POST, "16쪽", (11, 26), (11, 26)),
    (["11/27(금)"], "숭실대", "SSU미래인재(면접형)", "11/23(월) 10:00", POST, "6·8쪽", (11, 27), (11, 27)),
    (["11/27(금)"], "강원대", "미래인재면접", "11/20(금) 15:00", POST, "3쪽", (11, 27), (11, 27)),
    (["11/27(금)", "의·치·수의 11/28(토)"], "서울대", "일반전형", "11/20(금) 18:00 이후", POST, "2쪽", (11, 27), (11, 28)),
]

ROWS2 = [
    (["11/28(토)"], "서울여대", "바롬인재면접", "11/25(수) 18:00 예정", POST, "5쪽", (11, 28), (11, 28)),
    (["11/28(토)"], "서울과기대", "학교생활우수자·창의융합인재", "11/20(금) 14:00", POST, "12쪽", (11, 28), (11, 28)),
    (["11/28 간호·자율전공", "12/5 의예과"], "울산대", "잠재역량", "11/20(금) 16:00 예정", POST, "6쪽", (11, 28), (12, 5)),
    (["11/28 자연캠퍼스 단위", "11/29 인문캠퍼스 단위"], "명지대", "명지인재면접 · 면접은 서울", "11/20(금) 15:00", POST, "10쪽", (11, 28), (11, 29)),
    (["11/28(토)~29(일)", "모집단위별"], "숙명여대", "숙명인재(면접형)", "11/19(목) 18시", DAY, "6쪽", (11, 28), (11, 29)),
    (["11/28 인문·예체능", "11/29 자연"], "서울시립대", "학생부종합Ⅰ(면접형)", "11/20(금) 예정", POST, "14쪽", (11, 28), (11, 29)),
    (["11/29 디자인학부", "12/5·6 단과대학별"], "경기대", "KGU학생부종합 · 수원", "11/20(금)", POST, "9쪽", (11, 29), (12, 6)),
    (["12/1(화)~4(금)", "단과대학별"], "충남대", "학생부종합Ⅰ(면접전형)", "11/20(금) 15:00 이후", POST, "32쪽", (12, 1), (12, 4)),
    (["12/2(수)"], "전남대", "고교생활우수자Ⅰ", "11/13(금) 15:00 예정", PRE, "16쪽", (12, 2), (12, 2)),
    (["12/4(금)"], "제주대", "학생부종합(면접 모집단위)", "11/13(금) 10:00", PRE, "1쪽", (12, 4), (12, 4)),
    (["12/4(금)", "의대·수의대 12/5(토)"], "서울대", "지역균형", "11/27(금) 18:00 이후", POST, "1쪽", (12, 4), (12, 5)),
    (["12/5(토)"], "부산대", "학생부종합·지역인재", "12/1(화) 16시", POST, "5쪽", (12, 5), (12, 5)),
    (["12/5(토)"], "가톨릭대", "잠재능력우수자면접(신학과 제외)", "11/27(금) 16:00", POST, "11~12쪽", (12, 5), (12, 5)),
    (["12/5(토)"], "한국교원대", "학생부종합우수자 등", "11/20(금) 10:00", POST, "4쪽", (12, 5), (12, 5)),
    (["12/5(토)~6(일)", "캠퍼스·단과대학별"], "경희대", "네오르네상스", "11/25(수)", POST, "21쪽", (12, 5), (12, 6)),
    (["12/5(토)~6(일)", "모집단위별"], "중앙대", "탐구형인재", "11/26(목) 14시", POST, "21쪽", (12, 5), (12, 6)),
    (["12/5(토)·6(일)", "단과대학별"], "건국대", "KU자기추천", "11/20(금) 14:00 예정", POST, "23쪽", (12, 5), (12, 6)),
    (["12/5 인문계열", "12/6 자연계열"], "단국대", "DKU인재(면접형) · 죽전", "11/20(금) 18:00", POST, "24쪽", (12, 5), (12, 6)),
    (["12/6(일)"], "성균관대", "성균인재 자유전공계열 등", "12/1(화) 면접대상자", POST, "8쪽", (12, 6), (12, 6)),
    (["12/9(수)"], "한림대", "학교생활우수자", "12/3(목) 16:00", POST, "21쪽", (12, 9), (12, 9)),
    (["12/11(금)~13(일)", "모집단위별"], "동국대", "Do Dream", "11/13(금) 예정", PRE, "6쪽", (12, 11), (12, 13)),
    (["12/14(월)"], "아주대", "ACE 의학과·약학과", "12/12(토)", POST, "6쪽", (12, 14), (12, 14)),
]


def after_days(md):
    return (date(2026, *md) - CSAT).days


def days_text(r):
    a, b = after_days(r[6]), after_days(r[7])
    return f"{a}일" if a == b else f"{a}~{b}일"


def fit(d, text, fnt, maxw):
    while d.textlength(text, font=fnt) > maxw and len(text) > 2:
        text = text[:-2] + "…"
    return text


TAGC = {PRE: (BLUE, "white"), DAY: (ACCENT, NAVY_D), POST: (CORAL, "white")}


def make_table(out, rows, title, sub):
    RH = 78
    HEAD = 200
    COLS = [(44, "면접일", 268), (330, "대학 · 전형", 360), (706, "1단계 발표", 286), (1010, "수능 뒤", 160)]
    n = len(rows)
    H = HEAD + 58 + RH * n + 170
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    chip = "2027 수시 · 수능 11/19(목)"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    y = HEAD
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, lab, _ in COLS:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    prev = None
    for k, r in enumerate(rows):
        lines, univ, track, first, tag, pg, a, b = r
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        # 면접일
        f_d = font(23, True)
        f_s = font(19)
        if len(lines) == 1:
            text_fixed(d, (COLS[0][0], y + 24), lines[0], f_d, NAVY)
        else:
            text_fixed(d, (COLS[0][0], y + 10), fit(d, lines[0], f_d, COLS[0][2]), f_d, NAVY)
            text_fixed(d, (COLS[0][0], y + 44), fit(d, lines[1], f_s, COLS[0][2]), f_s, GRAY)
        # 대학 · 전형
        d.text((COLS[1][0], y + 8), univ, font=font(27, True), fill=TEXT)
        text_fixed(d, (COLS[1][0], y + 46), fit(d, track, font(19), COLS[1][2] - 6), font(19), GRAY)
        # 1단계 발표 + 수능 전/후 칩
        text_fixed(d, (COLS[1 + 1][0], y + 10), first, font(22, True), TEXT)
        bg, fg = TAGC[tag]
        ft = font(17, True)
        tw = d.textlength(tag, font=ft)
        d.rounded_rectangle([COLS[2][0], y + 44, COLS[2][0] + tw + 20, y + 68], radius=12, fill=bg)
        d.text((COLS[2][0] + 10, y + 45), tag, font=ft, fill=fg)
        text_fixed(d, (COLS[2][0] + tw + 30, y + 46), f"요강 {pg}", font(17), GRAY)
        # 수능 뒤 N일
        da = after_days(a)
        col = CORAL if da <= 3 else (BLUE if da <= 10 else NAVY)
        d.text((COLS[3][0], y + 20), days_text(r), font=font(28, True), fill=col)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    pdfnote = "인쇄 쪽수, 'PDF'는 PDF 쪽수" if any(r[5].startswith("PDF") for r in rows) else "인쇄 쪽수"
    text_fixed(d, (40, y), f"출처: 각 대학 2027학년도 수시모집요강 전형일정 표(쪽수는 각 행, {pdfnote}). 모집단위마다 날짜가 다른 대학이 있습니다.", font(19), GRAY)
    text_fixed(d, (40, y + 30), "수능 뒤 N일 = 면접일 − 수능일(11/19), 이 글에서 계산한 값. 날짜·시간은 1단계 발표 때 입학처 공지로 다시 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size)


FLOW = [
    ("1", "수능", "11/19(목)", "시험에 집중합니다. 면접 답변 초안은 수능 전에 만들어 둡니다.", NAVY),
    ("2", "가채점 · 최저 · 발표 확인", "11/19 ~ 11/20", "가채점으로 수능최저 충족 여부를 가늠하고, 1단계 발표일과 2단계 전형료 마감을 확인합니다.", BLUE),
    ("3", "남은 날에 맞춰 면접 준비", "수능 뒤 2~25일", "2~3일: 확인 + 모의면접 1번 · 1주 안팎: 질문 뽑기 → 녹음 → 모의면접 · 2주 이상: 이 순서를 두 번", CORAL),
    ("4", "면접", "11/21 ~ 12/14", "전날 수험표·신분증·입실 시각·장소를 다시 보고, 새 답변은 만들지 않습니다.", NAVY_D),
]


def make_flow(out):
    from promo_style import wrap_chars
    BOX = 150
    GAP = 46
    HEAD = 180
    H = HEAD + (BOX + GAP) * len(FLOW) - GAP + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "수능 → 가채점·최저 확인 → 면접 준비 → 면접", font=font(42, True), fill="white")
    d.text((48, 90), "단계 순서와 기간 구분은 이 글이 제안하는 방법입니다. 대학이 정한 기준이 아닙니다.", font=font(23), fill=PALE)
    y = HEAD
    x0, x1 = 40, W - 40
    for i, (num, title, when, desc, col) in enumerate(FLOW):
        d.rounded_rectangle([x0, y, x1, y + BOX], radius=16, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 200, y + BOX], radius=16, fill=col)
        d.rectangle([x0 + 180, y, x0 + 200, y + BOX], fill=col)
        d.text((x0 + 26, y + 14), num, font=font(60, True), fill=ACCENT if col != NAVY_D else ACCENT)
        text_fixed(d, (x0 + 26, y + 96), when, font(20, True), "white")
        d.text((x0 + 226, y + 16), title, font=font(32, True), fill=NAVY)
        f_d = font(21)
        for j, ln in enumerate(wrap_chars(d, desc, f_d, x1 - x0 - 260)[:3]):
            text_fixed(d, (x0 + 226, y + 64 + 27 * j), ln, f_d, TEXT)
        if i < len(FLOW) - 1:
            cx = x0 + 100
            d.polygon([(cx - 18, y + BOX + 8), (cx + 18, y + BOX + 8), (cx, y + BOX + GAP - 8)], fill=GRAY)
        y += BOX + GAP
    y += 4
    text_fixed(d, (40, y), "날짜별 면접 대학과 1단계 발표일은 본문 표를 보세요. 수능최저가 있는 전형은 면접을 봐도 최저를 못 맞추면 합격할 수 없습니다.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("flow", out, img.size)


def jobs_after():
    make_thumb(HERE / "thumb-after.png", "수능 끝나고", line2="면접 보는 대학", line3="날짜별 총정리")
    make_table(HERE / "after-table-1.png", ROWS1, "수능 뒤 면접 ① 11월 21일 ~ 27일", f"{len(ROWS1)}개 전형 · 날짜순")
    make_table(HERE / "after-table-2.png", ROWS2, "수능 뒤 면접 ② 11월 28일 ~ 12월 14일", f"{len(ROWS2)}개 전형 · 날짜순")
    make_flow(HERE / "after-flow.png")


if __name__ == "__main__":
    jobs_after()
