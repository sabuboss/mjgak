# 2027 수시 면접 일정 총정리 글 이미지. python jobs_schedule.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, font, text_fixed, brand, make_thumb, NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)
from schedule_data import SECTIONS, PRE, AFTER1, AFTER2, DEC

W = 1200
COLS = [(40, "면접일", 230), (270, "대학", 150), (420, "전형 · 모집단위", 560), (980, "1단계 발표", 180)]


def fit(d, text, fnt, maxw):
    while d.textlength(text, font=fnt) > maxw and len(text) > 2:
        text = text[:-2] + "…"
    return text


def make_table(out, title, sub, rows, idx, total):
    RH = 78
    HEAD = 190
    H = HEAD + 56 + RH * len(rows) + 110
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 20], fill=NAVY)
    chip = f"2027 수시 면접 일정 {idx}/{total}"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 88), title, font=font(46, True), fill="white")
    d.text((40 + d.textlength(title, font=font(46, True)) + 24, 104), sub, font=font(24), fill=PALE)
    y = HEAD
    d.rounded_rectangle([24, y, W - 24, y + 56 + RH * len(rows) + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, lab, _ in COLS:
        d.text((x, y + 16), lab, font=fh, fill=GRAY)
    d.line([40, y + 54, W - 40, y + 54], fill=LINE, width=2)
    y += 56
    prev_date = None
    for i, (date, univ, track, unit, first, memo) in enumerate(rows):
        if i % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        fd = font(26, True)
        if date != prev_date:
            d.text((COLS[0][0], y + 22), fit(d, date, fd, COLS[0][2] - 10), font=fd, fill=CORAL)
        prev_date = date
        d.text((COLS[1][0], y + 22), univ, font=font(28, True), fill=NAVY)
        f1 = font(23, True); f2 = font(21)
        d.text((COLS[2][0], y + 10), fit(d, track, f1, COLS[2][2] - 10), font=f1, fill=TEXT)
        line2 = unit + (f"  ·  {memo}" if memo else "")
        text_fixed(d, (COLS[2][0], y + 42), fit(d, line2, f2, COLS[2][2] - 10), f2, GRAY)
        text_fixed(d, (COLS[3][0], y + 24), first, font(22), TEXT)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강. 시간·장소는 1단계 발표 때 입학처에서 다시 확인하세요.", font(20), GRAY)
    brand(d, W - 230, H - 52, size=24)
    img.save(out)
    print("table", out, img.size)


def make_timeline(out):
    """한 장 요약: 주차별 막대."""
    weeks = [
        ("10월 셋째 주", "10/14~20", "남부·백석·청주 (교과 면접)", 0),
        ("10월 넷째 주", "10/24~25", "청주 항공·한세·삼육", 0),
        ("10월 말", "10/31~11/1", "광운 참빛Ⅰ·선문", 0),
        ("11월 첫째 주", "11/7~8", "강남 학교생활우수자2", 0),
        ("수능", "11/19(목)", "", 2),
        ("수능 직후", "11/21~22", "서울교대·을지·덕성·이화·인하·국민·세종·성신·아주", 1),
        ("11월 마지막 주", "11/27~29", "숭실·명지·아주·울산·숙명·경기", 1),
        ("12월 첫째 주", "12/2~6", "전남·충남·제주·경희·중앙·건국·부산·울산 의예·경기", 1),
        ("12월 둘째 주", "12/11~14", "동국 Do Dream·아주 의·약", 1),
    ]
    RH = 92
    H = 200 + RH * len(weeks) + 120
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 170], fill=NAVY)
    d.text((40, 34), "2027 수시 면접, 언제 몰리나", font=font(48, True), fill="white")
    d.text((40, 104), "30개 대학 모집요강 기준 · 수능 2026년 11월 19일(목)", font=font(24), fill=PALE)
    y = 200
    for lab, rng, who, kind in weeks:
        if kind == 2:
            d.rounded_rectangle([40, y + 14, W - 40, y + RH - 14], radius=12, fill=CORAL)
            d.text((64, y + 26), f"수능 {rng}", font=font(30, True), fill="white")
            t = "수능 전 면접은 위, 수능 후 면접은 아래"
            d.text((W - 64 - d.textlength(t, font=font(22)), y + 32), t, font=font(22), fill="white")
        else:
            col = PALE if kind == 0 else "#fff3d6"
            d.rounded_rectangle([40, y + 8, W - 40, y + RH - 8], radius=12, fill="white", outline=LINE, width=2)
            d.rounded_rectangle([40, y + 8, 300, y + RH - 8], radius=12, fill=col)
            d.rectangle([280, y + 8, 300, y + RH - 8], fill=col)
            d.text((60, y + 18), lab, font=font(24, True), fill=NAVY)
            d.text((60, y + 50), rng, font=font(22), fill=GRAY)
            text_fixed(d, (324, y + 32), fit(d, who, font(25, True), W - 380), font(25, True), TEXT)
        y += RH
    y += 20
    text_fixed(d, (40, y), "날짜는 대표 일정입니다. 학과별 날짜는 본문 표와 각 대학 입학처 공지에서 확인하세요.", font(20), GRAY)
    brand(d, W - 230, H - 52, size=24)
    img.save(out)
    print("timeline", out, img.size)


def jobs_schedule():
    make_thumb(HERE / "thumb-schedule.png", "면접 일정", line2="30개 대학 날짜", line3="수능 전·후 총정리")
    make_timeline(HERE / "schedule-2027-timeline.png")
    names = ["schedule-2027-pre.png", "schedule-2027-1121.png", "schedule-2027-1127.png", "schedule-2027-dec.png"]
    for i, ((title, sub, rows), name) in enumerate(zip(SECTIONS, names), 1):
        make_table(HERE / name, title, sub, rows, i, len(SECTIONS))


if __name__ == "__main__":
    jobs_schedule()
