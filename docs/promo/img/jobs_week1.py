# 1단계 합격 발표 후 면접까지 1주일 준비법 블로그 글 이미지. python jobs_week1.py
# 날짜는 각 대학 2027학년도 수시모집요강 전형일정 표에서 직접 확인(쪽수는 ROWS 의 마지막 칸).
# 간격(일수)은 이 글에서 계산한 값: 면접일 - 1단계 발표일.
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, pdf, make_thumb, make_capture, font, wrap_chars, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

LBL = "2027학년도 수시모집요강"
W = 1200

# (대학, 전형, 1단계 발표 표기, 면접일 표기, 1단계 date, 면접 첫날, 면접 마지막날, 근거 쪽)
ROWS = [
    ("동덕여대", "동덕창의리더", "10/27(화) 17:00", "10/31(토)~11/1(일)", (10, 27), (10, 31), (11, 1), "3쪽(PDF 7)"),
    ("광운대", "광운참빛인재Ⅰ(면접형)", "10/28(수) 15:00", "10/31(토) 또는 11/1(일)", (10, 28), (10, 31), (11, 1), "18쪽"),
    ("고려대", "계열적합", "10/30(금) 17:00", "11/7(토) 인문|11/8(일) 자연", (10, 30), (11, 7), (11, 8), "9쪽"),
    ("상명대", "상명인재(서울, 면접 2개 전공)", "10/30(금) 14:00", "11/7(토)", (10, 30), (11, 7), (11, 7), "7쪽(PDF 9)"),
    ("한국항공대", "미래인재", "10/30(금) 09:00", "11/7(토)", (10, 30), (11, 7), (11, 7), "4쪽(PDF 6)"),
    None,  # 수능 줄
    ("이화여대", "미래인재(면접형)", "11/12(목)", "11/21(토)~22(일)", (11, 12), (11, 21), (11, 22), "9쪽(PDF 8)"),
    ("세종대", "세종인재(면접형)", "11/13(금) 17시 이후", "11/21(토) · 11/22(일)", (11, 13), (11, 21), (11, 22), "8쪽"),
    ("한국외대", "학생부종합(면접형)", "11/16(월)", "11/21(토) 서울캠퍼스|11/22(일) 글로벌캠퍼스", (11, 16), (11, 21), (11, 22), "19쪽(PDF 21)"),
    ("인하대", "인하미래인재(면접형)", "11/17(화)", "11/21(토) · 11/22(일)", (11, 17), (11, 21), (11, 22), "8쪽(PDF 11)"),
    ("국민대", "국민프런티어", "11/17(화) 14:00", "11/21(토) 자연계|11/22(일) 인문·예체능계", (11, 17), (11, 21), (11, 22), "10쪽(PDF 12)"),
    ("숙명여대", "숙명인재(면접형)", "11/19(목) 18시", "11/28(토)~29(일)", (11, 19), (11, 28), (11, 29), "14쪽(PDF 18)"),
    ("건국대", "KU자기추천", "11/20(금) 14:00", "12/5(토) · 12/6(일)", (11, 20), (12, 5), (12, 6), "31쪽"),
]


def gap(a, b):
    return (date(2026, *b) - date(2026, *a)).days


def gap_text(r):
    g1, g2 = gap(r[4], r[5]), gap(r[4], r[6])
    return f"{g1}일" if g1 == g2 else f"{g1}~{g2}일"


def fit(d, text, fnt, maxw):
    while d.textlength(text, font=fnt) > maxw and len(text) > 2:
        text = text[:-2] + "…"
    return text


def make_gap_table(out):
    RH = 84
    HEAD = 200
    COLS = [(44, "대학 · 전형", 320), (366, "1단계 발표", 236), (612, "면접일", 300), (926, "간격(계산)", 240)]
    n = len(ROWS)
    H = HEAD + 58 + RH * n + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    chip = "2027 수시 학생부종합 면접"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), "1단계 발표부터 면접까지 며칠?", font=font(46, True), fill="white")
    sub = "12개 대학 · 간격은 이 글에서 계산한 값"
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    y = HEAD
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, lab, _ in COLS:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    maxg = 16
    k = 0
    for r in ROWS:
        if r is None:
            d.rounded_rectangle([34, y + 14, W - 34, y + RH - 14], radius=10, fill=CORAL)
            d.text((56, y + 25), "수능 11/19(목)", font=font(28, True), fill="white")
            t = "아래 이화여대~국민대는 발표와 면접 사이에 수능이 있습니다"
            d.text((W - 56 - d.textlength(t, font=font(22)), y + 30), t, font=font(22), fill="white")
            y += RH
            continue
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        k += 1
        univ, track, first, intv, a, b1, b2, pg = r
        d.text((COLS[0][0], y + 10), univ, font=font(28, True), fill=NAVY)
        text_fixed(d, (COLS[0][0], y + 48), fit(d, track, font(20), COLS[0][2] - 6), font(20), GRAY)
        text_fixed(d, (COLS[1][0], y + 16), first, font(22, True), TEXT)
        text_fixed(d, (COLS[1][0], y + 50), f"요강 {pg}", font(18), GRAY)
        f_i = font(23, True)
        lines = intv.split("|")
        if len(lines) == 1:
            text_fixed(d, (COLS[2][0], y + 27), lines[0], f_i, TEXT)
        else:
            for j, ln in enumerate(lines[:2]):
                text_fixed(d, (COLS[2][0], y + 12 + 32 * j), ln, f_i, TEXT)
        g1, g2 = gap(a, b1), gap(a, b2)
        bx = COLS[3][0]
        bw = 100
        col = CORAL if g1 <= 5 else (BLUE if g1 <= 10 else NAVY)
        d.rounded_rectangle([bx, y + 22, bx + bw, y + 40], radius=9, fill="#edf0f4")
        d.rounded_rectangle([bx, y + 22, bx + max(18, int(bw * g2 / maxg)), y + 40], radius=9, fill=PALE)
        d.rounded_rectangle([bx, y + 22, bx + max(18, int(bw * g1 / maxg)), y + 40], radius=9, fill=col)
        d.text((bx + bw + 14, y + 16), gap_text(r), font=font(25, True), fill=col)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강 전형일정 표(쪽수는 각 행). 간격 = 면접일 − 1단계 발표일(이 글에서 계산).", font(19), GRAY)
    text_fixed(d, (40, y + 30), "모집단위마다 면접일이 다른 대학이 있습니다. 내 모집단위 날짜와 시간은 1단계 발표 때 입학처 공지로 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size)


PLAN = [
    ("발표 당일", "D-7", "결과·공지 확인", "합격 확인 → 2단계 전형료(있으면) → 면접 일시·장소·준비물 → 수험표 출력", "확인 목록 1장"),
    ("1일차", "D-6", "서류 다시 읽기", "학생부를 처음부터 끝까지. 활동마다 왜 했나·무엇을 했나·무엇이 달라졌나 메모", "활동 메모"),
    ("2일차", "D-5", "예상 질문 뽑기", "기본 질문 5개 + 학생부 문장에서 뽑은 질문 15개 정도", "질문 목록"),
    ("3일차", "D-4", "1분 답변 녹음", "질문마다 결론부터 60초. 녹음해서 다시 들어 보기", "녹음 파일"),
    ("4일차", "D-3", "모의면접", "가족·친구·선생님 앞에서 모집요강에 적힌 면접 시간대로 한 번", "막힌 질문 목록"),
    ("5일차", "D-2", "꼬리질문", "막힌 답에 \"왜?\" \"그래서?\" \"다시 한다면?\"을 붙여 연습", "꼬리질문 답"),
    ("전날", "D-1", "쉬기·준비물", "새 답변 만들지 않기. 수험표·신분증·복장·경로·입실 시간 확인 후 일찍 자기", "가방 싸기"),
]


def make_plan(out):
    RH = 108
    HEAD = 180
    H = HEAD + RH * len(PLAN) + 30 + 250
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "1단계 발표 후 면접까지 하루하루", font=font(44, True), fill="white")
    d.text((48, 90), "면접일을 D-day 로 거꾸로 셉니다. 순서·개수·시간은 이 글이 제안하는 연습법입니다.", font=font(23), fill=PALE)
    y = HEAD
    x0, x1 = 40, W - 40
    for i, (day, dn, title, desc, res) in enumerate(PLAN):
        first = i == 0
        last = i == len(PLAN) - 1
        fill_l = ACCENT if first else (CORAL if last else PALE)
        d.rounded_rectangle([x0, y, x1, y + RH - 14], radius=14, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 170, y + RH - 14], radius=14, fill=fill_l)
        d.rectangle([x0 + 150, y, x0 + 170, y + RH - 14], fill=fill_l)
        tc = "white" if last else NAVY_D
        d.text((x0 + 22, y + 12), dn, font=font(34, True), fill=tc)
        d.text((x0 + 22, y + 56), day, font=font(21, True), fill=tc)
        d.text((x0 + 196, y + 12), title, font=font(29, True), fill=NAVY)
        f_d = font(20)
        lines = wrap_chars(d, desc, f_d, 700)
        for j, ln in enumerate(lines[:2]):
            text_fixed(d, (x0 + 196, y + 50 + 25 * j), ln, f_d, TEXT)
        fr = font(20, True)
        rw = d.textlength(res, font=fr)
        d.rounded_rectangle([x1 - 24 - rw - 32, y + 30, x1 - 24, y + 66], radius=18, fill="#f7f9fc", outline=LINE)
        d.text((x1 - 24 - rw - 16, y + 36), res, font=fr, fill=CORAL)
        y += RH
    y += 6
    d.rounded_rectangle([x0, y, x1, y + 200], radius=14, fill=NAVY)
    d.text((x0 + 28, y + 20), "발표부터 면접까지 4~5일뿐이라면", font=font(28, True), fill=ACCENT)
    tips = [
        "발표 당일: D-7 + D-6 (공지 확인하고 학생부 다시 읽기)",
        "다음 날: D-5 + D-4 (질문 뽑고 1분 답변 녹음)",
        "그다음 날: D-3 + D-2 (모의면접 한 번, 막힌 곳 꼬리질문)",
        "전날: D-1 그대로 (쉬기·준비물). 3일이면 '그다음 날'이 곧 전날입니다",
    ]
    for j, t in enumerate(tips):
        d.ellipse([x0 + 32, y + 78 + 28 * j, x0 + 40, y + 86 + 28 * j], fill=ACCENT)
        text_fixed(d, (x0 + 54, y + 68 + 28 * j), t, font(21), "white")
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("plan", out, img.size)


def jobs_week1():
    make_thumb(HERE / "thumb-week1.png", "1단계 합격 후", line2="면접까지 1주일", line3="하루하루 준비법")
    make_gap_table(HERE / "week1-gap-table.png")
    make_plan(HERE / "week1-plan.png")
    # 숙명여대: 1단계 발표가 수능 당일 18시, 2단계 전형료 다음 날 17시까지
    make_capture(HERE / "sm-2027-week1-schedule.png", pdf("숙명여자대학교"), 18, "다. 전형일정", "라. 전형방법",
                 "숙명여자대학교", f"{LBL} 14쪽(PDF 18쪽)", "1단계 11/19(목) 18시 · 2단계 전형료 11/20 17시까지 · 면접 11/28~29",
                 start_pad=8, end_pad=6)
    # 건국대: 2단계 전형료 11/23 14시까지, 면접 고사장·입실 시간은 면접 3~4일 전 공지
    make_capture(HERE / "konkuk-2027-week1-schedule.png", pdf("건국대학교"), 31, "7. 전형일정", "8. 제출서류",
                 "건국대학교", f"{LBL} 31쪽", "1단계 11/20(금) · 전형료 11/23 14시까지 · 고사장은 면접 3~4일 전 공지",
                 start_pad=10, end_pad=10)
    # 한국항공대: 면접 준비물·입실·복장
    make_capture(HERE / "kau-2027-week1-interview.png", pdf("한국항공대학교"), 28, "나. 일반면접", ("after", "불합격 처리합니다."),
                 "한국항공대학교", f"{LBL} 26쪽(PDF 28쪽)", "준비물 수험표·신분증 · 30분 전 입실 · 교복 착용 금지",
                 start_pad=10, end_pad=10, end_idx=-1)


if __name__ == "__main__":
    jobs_week1()
