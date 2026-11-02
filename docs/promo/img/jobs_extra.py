# 2027 수시 추가합격(충원) 완벽 정리 블로그 글(naver-125) 이미지. python jobs_extra.py
# 대학 수는 site/content/rich/univ/*.json 의 after.extra 에서 센 값(2026-11-03, 101개 대학 기준).
# 표의 대학별 날짜·규정은 각 대학 2027학년도 수시모집요강에서 직접 확인했다(쪽수는 원고 작업용 메모 [근거 쪽수]).
# 디자인은 jobs_results.py(header·make_date_table·make_flow)를 복사해 맞췄다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, make_capture, pdf, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

# 대학 | 홈페이지 발표 차수 | 전화 통보 차수 | 전화 불통 규정 | 충원 등록 마감
TABLE = [
    ("고려대", "1~6차(전형별 다름) · 1차 12/23(수) 21:00", "6차(계열적합) 12/29(화) 14:00~18:00", "최대 3회 시도, 안 되면 추가 충원 대상 제외", "12/30(수) 10:00"),
    ("경기대", "1·2차 · 1차 12/23(수) 19:00 이후", "3차(12/26(토) 13:00 이후)부터", "3회 이상 시도, 안 되면 미등록 처리", "12/30(수) 12:00"),
    ("강남대", "1~3차 · 1차 12/24(목)", "4차(12/28(월))부터", "5분 간격 3번, 안 되면 다음 순위로", "5차는 발표 때 공지"),
    ("경상국립대", "1차 12/24(목)·2차 12/28(월) 10:00", "3차(최종) 12/29(화) 10:00~18:00", "4회 이상 안 되면 등록 포기 처리", "12/30(수) 16:00"),
    ("부산대", "1차 12/24(목) 18:00·2차 12/27(일) 22:00", "3차 12/29(화) 18:00까지", "최대 3회까지 통화 시도", "12/30(수) 10:00~16:00"),
    ("한국교원대", "1~3차 · 12/24·27·28 10:00", "최종 12/29(화) 10:00~18:00", "3회까지 시도, 안 되면 불합격 처리", "12/29(화) 21:00"),
    ("연세대(미래)", "1~4차 · 12/24(목) 09:00~12/29(화) 14:00", "전화충원 하지 않음", "-", "12/30(수) 16:00"),
]


def header(d, title, sub, chip="2027 수시 · 충원(추가) 합격"):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    return HEAD


def wrap_words(d, text, fnt, maxw):
    """띄어쓰기 단위로 줄을 바꾼다(숫자·시각이 중간에 끊기지 않게). 한 단어가 칸보다 길면 글자 단위로."""
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w) if cur else w
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        elif not cur:
            parts = wrap_chars(d, w, fnt, maxw)
            out += parts[:-1]; cur = parts[-1]
        else:
            out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out


def make_extra_table(out):
    """대학별 충원 발표 방법 표. 칸 안 글자는 두 줄까지 줄바꿈한다."""
    COLS = [(44, 140, "대학"), (184, 275, "홈페이지 발표"), (459, 250, "전화 통보"), (709, 255, "전화 불통 규정"), (964, 196, "충원 등록 마감")]
    RH, HROW = 96, 58
    n = len(TABLE)
    H = 200 + HROW + RH * n + 190
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, "충원 발표, 홈페이지 vs 전화", f"{n}개 대학 · 모집요강 기준")
    d.rounded_rectangle([24, y, W - 24, y + HROW + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, _, lab in COLS:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += HROW
    fc = font(20)
    for k, row in enumerate(TABLE):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        for j, ((x, cw, _), val) in enumerate(zip(COLS, row)):
            if j == 0:
                fu = font(25, True)
                lines = val.replace("(", "|(").split("|") if d.textlength(val, font=fu) > cw - 8 else [val]
                for i, ln in enumerate(lines[:2]):
                    d.text((x, y + (30 if len(lines) == 1 else 16) + 32 * i), ln, font=fu, fill=NAVY)
                continue
            col = TEXT
            if j == 2 and val.startswith("전화충원 하지"):
                col = GRAY
            if j == 4:
                col = CORAL
            f = font(21, True) if j == 4 else fc
            lines = wrap_words(d, val, f, cw - 14)
            if len(lines) > 3:
                raise SystemExit(f"칸 글자가 너무 깁니다: {val}")
            top = y + (RH - 28 * len(lines)) / 2 - 2
            for i, ln in enumerate(lines):
                text_fixed(d, (x, top + 28 * i), ln, f, col)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강(합격자 발표 및 등록, 미등록 충원). 고려대 6차 전화는 계열적합전형만 해당.", font(19), GRAY)
    text_fixed(d, (40, y + 30), "강남대 4차 등록은 12/29(화). 차수별 시각은 바뀔 수 있으니 최초합격자 발표 때 대학 공지로 다시 확인하세요.", font(19), GRAY)
    text_fixed(d, (40, y + 60), "등록 마감은 마지막 차수 기준입니다. 앞 차수는 발표 뒤 몇 시간~사흘 남짓 안에 등록이 끝납니다(대학·차수마다 다름).", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size, n)


FLOW = [
    ("1", "충원 발표 시작", "12/23(수) ~ 12/24(목)", "81개 대학이 12/24(목)에, 10개 대학이 12/23(수)에 첫 충원을 발표합니다(고려대 21시, 경기대 19시 이후 등).", NAVY),
    ("2", "차수별 홈페이지 발표", "12/24(목) ~ 12/28(월)", "표의 7개 대학은 앞 차수를 홈페이지로 발표합니다. 차수별 등록은 발표 뒤 몇 시간~사흘 남짓 안에 끝나고, 성탄절·주말에 발표하는 대학도 있습니다.", BLUE),
    ("3", "마지막 날, 전화 충원", "12/29(화)", "97개 대학이 충원 발표(통보) 마감을 12/29(화)로 적었습니다. 전화(유선) 통보를 적은 대학은 적어도 65곳입니다.", CORAL),
    ("4", "충원 합격자 마지막 등록", "12/30(수)", "적어도 84개 대학이 12/30(수)을 충원 등록 마감일로 적었습니다. 한국교원대는 12/29(화) 21시가 마지막입니다.", NAVY_D),
]


def make_flow(out):
    BOX, GAP, HEAD = 140, 40, 180
    H = HEAD + (BOX + GAP) * len(FLOW) - GAP + 140
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "충원(추가) 합격 기간, 한눈에", font=font(42, True), fill="white")
    d.text((48, 90), "면접각이 확인한 101개 대학 수시 일정에서 센 값. 대학별 시각은 본문과 표를 참고.", font=font(23), fill=PALE)
    y = HEAD
    x0, x1 = 40, W - 40
    for i, (num, title, when, desc, col) in enumerate(FLOW):
        d.rounded_rectangle([x0, y, x1, y + BOX], radius=16, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 260, y + BOX], radius=16, fill=col)
        d.rectangle([x0 + 240, y, x0 + 260, y + BOX], fill=col)
        d.text((x0 + 24, y + 10), num, font=font(56, True), fill=ACCENT)
        text_fixed(d, (x0 + 24, y + 92), when, font(21, True), "white")
        d.text((x0 + 286, y + 14), title, font=font(32, True), fill=NAVY)
        f_d = font(21)
        lines = wrap_chars(d, desc, f_d, x1 - x0 - 320)
        if len(lines) > 3:
            raise SystemExit(f"설명이 너무 깁니다: {desc}")
        for j, ln in enumerate(lines):
            text_fixed(d, (x0 + 286, y + 62 + 27 * j), ln, f_d, TEXT)
        if i < len(FLOW) - 1:
            cx = x0 + 130
            d.polygon([(cx - 18, y + BOX + 6), (cx + 18, y + BOX + 6), (cx, y + BOX + GAP - 6)], fill=GRAY)
        y += BOX + GAP
    y += 4
    text_fixed(d, (40, y), "수시 충원 합격도 합격입니다. 등록하지 않아도 정시·추가모집에 지원할 수 없습니다(특별법 설치 대학 등 예외).", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("flow", out, img.size)


def jobs_extra():
    make_thumb(HERE / "thumb-extra.png", "수시 추가합격", line2="충원 완벽 정리", line3="예비번호 · 전화 3회 · 이중등록",
               chip="2027 수시 충원 12/24~29")
    make_flow(HERE / "extra-flow.png")
    make_extra_table(HERE / "extra-table.png")
    a = pdf("아주대학교")
    make_capture(HERE / "ajou-2027-extra-giveup.png", a, 60, "나. 문서등록 포기", ("after", "등록기간 중에 중복 등록한 대학의 등록을 포기하여야 함"),
                 "아주대학교", "2027학년도 수시모집요강 58쪽(PDF 60쪽)", "등록 뒤 다른 대학에 옮길 땐 포기 신청부터, 의사는 즉시 전달",
                 start_pad=4, end_pad=4)


if __name__ == "__main__":
    jobs_extra()
