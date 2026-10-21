# 2027 수능 D-30 체크리스트 블로그 글 이미지. python jobs_csat.py
# 사실 근거(모두 원문에서 다시 확인):
#   시간표·문항 수: 평가원 「2027학년도 대학수학능력시험 시행기본계획」(2026.3.31.) 2쪽,
#                  「2027학년도 대학수학능력시험 수험생 유의사항」 붙임1 시험시간표(14쪽, PDF 16쪽)
#   준비물·반입 금지: 「수험생 유의사항」 1~3쪽(PDF 3~5쪽)·13쪽(PDF 15쪽), 「실시요강」(2026.8.) 25~26쪽(PDF 26~27쪽)
#   일정: 「실시요강」 19~20쪽(PDF 20~21쪽), 대교협 「2027학년도 대학입학전형시행계획 주요사항」(2025.4.30.) 1쪽
#   면접일: 각 대학 2027학년도 수시모집요강(이화여대 9쪽, 한국외대 19쪽, 숙명여대 14쪽, 건국대 31쪽, 동국대 18쪽)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, wrap_chars, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200


def header(d, chip, title, sub, h):
    d.rectangle([0, 0, W, h], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    if sub:
        text_fixed(d, (40, 152), sub, font(23), PALE)


# ------------------------------------------------------------------ ① 시간표
# (교시, 영역, 시간, 소요, 문항, 메모, 종류) 종류: main=시험, rest=쉬는 시간, key=입실
TT = [
    ("입실", "모든 수험생", "08:10까지", "", "", "1교시 미선택자도 08:10까지 입실", "key"),
    ("1교시", "국어", "08:40 ~ 10:00", "80분", "45", "", "main"),
    ("", "휴식", "10:00 ~ 10:20", "20분", "", "", "rest"),
    ("2교시", "수학", "10:30 ~ 12:10", "100분", "30", "단답형 30% 포함", "main"),
    ("", "점심", "12:10 ~ 13:00", "50분", "", "점심·마실 물은 제공되지 않음", "rest"),
    ("3교시", "영어", "13:10 ~ 14:20", "70분", "45", "듣기 17문항, 13:10부터 25분 이내", "main"),
    ("", "휴식", "14:20 ~ 14:40", "20분", "", "4교시는 14:40(예비령)까지 입실", "rest"),
    ("4교시", "한국사", "14:50 ~ 15:20", "30분", "20", "필수 영역 · 안 보면 성적 전체 무효", "main"),
    ("", "문·답지 회수·배부", "15:20 ~ 15:35", "15분", "", "탐구 미선택자는 대기실로 이동", "rest"),
    ("", "탐구 제1선택", "15:35 ~ 16:05", "30분", "20", "1과목 선택자는 이 시간 대기", "main"),
    ("", "문제지 회수", "16:05 ~ 16:07", "2분", "", "", "rest"),
    ("", "탐구 제2선택", "16:07 ~ 16:37", "30분", "20", "1과목 선택자는 이 시간에 응시", "main"),
    ("", "휴식", "16:37 ~ 16:55", "18분", "", "", "rest"),
    ("5교시", "제2외국어/한문", "17:05 ~ 17:45", "40분", "30", "", "main"),
]


def make_timetable(out):
    HEAD = 200
    RH_M, RH_R = 74, 50
    COLS = [(44, "교시"), (170, "영역"), (420, "시간"), (640, "문항"), (730, "메모")]
    body_h = sum(RH_M if r[6] != "rest" else RH_R for r in TT)
    H = HEAD + 20 + 54 + body_h + 24 + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "2027학년도 수능 · 2026년 11월 19일(목)", "수능 날 시간표", "2~5교시는 시험 시작 10분 전까지 입실 · 시험실에는 시계가 없습니다", HEAD - 10)
    y = HEAD + 20
    d.rounded_rectangle([24, y, W - 24, y + 54 + body_h + 12], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, lab in COLS:
        d.text((x, y + 15), lab, font=fh, fill=GRAY)
    d.line([40, y + 52, W - 40, y + 52], fill=LINE, width=2)
    y += 54
    for kyo, area, tm, dur, q, memo, kind in TT:
        if kind == "rest":
            rh = RH_R
            d.rectangle([26, y, W - 26, y + rh], fill="#f7f9fc")
            text_fixed(d, (COLS[1][0], y + 11), area, font(21), GRAY)
            text_fixed(d, (COLS[2][0], y + 11), f"{tm}  ({dur})", font(21), GRAY)
            if memo:
                text_fixed(d, (COLS[4][0], y + 11), memo, font(20), GRAY)
        else:
            rh = RH_M
            if kind == "key":
                d.rectangle([26, y, W - 26, y + rh], fill=PALE)
            if kyo:
                fk = font(25, True)
                if kind == "main":
                    kw = d.textlength(kyo, font=fk)
                    d.rounded_rectangle([COLS[0][0] - 6, y + 18, COLS[0][0] + kw + 12, y + 56], radius=10, fill=NAVY)
                    d.text((COLS[0][0] + 3, y + 21), kyo, font=fk, fill="white")
                else:
                    d.text((COLS[0][0], y + 21), kyo, font=fk, fill=CORAL)
            d.text((COLS[1][0], y + 20), area, font=font(27, True), fill=NAVY)
            d.text((COLS[2][0], y + 14), tm, font=font(25, True), fill=CORAL if kind == "key" else TEXT)
            if dur:
                text_fixed(d, (COLS[2][0], y + 46), dur, font(18), GRAY)
            if q:
                d.text((COLS[3][0], y + 20), q, font=font(25, True), fill=TEXT)
            if memo:
                lines = wrap_chars(d, memo, font(20), W - 50 - COLS[4][0])
                yy = y + (24 if len(lines) == 1 else 10)
                for ln in lines[:2]:
                    text_fixed(d, (COLS[4][0], yy), ln, font(20), TEXT); yy += 28
        y += rh
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 한국교육과정평가원 「2027학년도 대학수학능력시험 시행기본계획」(2026.3.31.) 2쪽,", font(19), GRAY)
    text_fixed(d, (40, y + 28), "「2027학년도 대학수학능력시험 수험생 유의사항」 붙임1 시험시간표(14쪽)·1쪽·9쪽·13쪽. 문항 수는 탐구 과목당.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("timetable", out, img.size)


# ------------------------------------------------------------------ ② 준비물·반입 금지
BRING = [
    ("수험표", "잃어버렸다면 원서와 같은 사진 1장·신분증을 들고 당일 08:00까지 시험관리본부"),
    ("신분증", "주민등록증·운전면허증·여권·청소년증·학교장 직인 사진 학생증 등. 모바일 신분증은 안 됨"),
    ("아날로그 시계", "시침·분침(초침)이 있는 것. 통신·결제 기능, LCD·LED 화면이 없어야 함. 1·3교시 점검"),
    ("검은색 컴퓨터용 사인펜", "시험실에서 지급. 2027학년도부터 개인 지참 가능(빨간 사인펜 붙은 것은 안 됨)"),
    ("흰색 수정테이프 · 흑색 연필 · 지우개 · 샤프심(흑색 0.5mm)", "샤프는 시험실에서 나눠 주는 것만. 개인 샤프는 안 됨"),
    ("점심 · 마실 물", "시험장에서 제공되지 않습니다"),
]
BAN = [
    ("휴대폰 · 스마트워치 · 스마트안경 · 태블릿 · 이어폰", "통신(블루투스 포함)·결제 기능이 있는 모든 물품"),
    ("전자사전 · 화면표시기 있는 시계·텀블러", "LCD·LED 등 전자식 화면표시기가 있는 모든 물품"),
    ("전자담배 · 보조배터리", "그 밖의 충전식 물품 일체"),
]
BREAK = [
    ("교과서 · 참고서 · 기출문제지", "시험 중 갖고 있다 적발되면 부정행위"),
    ("연습장 · 기름종이 · 개인 샤프 · 플러스펜 · 볼펜", "시험 중 적발되면 압수"),
]


def check_box(d, x, y, kind):
    if kind == "ok":
        d.rounded_rectangle([x, y, x + 30, y + 30], radius=6, outline=NAVY, width=3, fill="white")
        d.line([(x + 6, y + 15), (x + 13, y + 23), (x + 25, y + 7)], fill=NAVY, width=4)
    elif kind == "ban":
        d.ellipse([x, y, x + 30, y + 30], fill=CORAL)
        d.line([(x + 9, y + 9), (x + 21, y + 21)], fill="white", width=4)
        d.line([(x + 21, y + 9), (x + 9, y + 21)], fill="white", width=4)
    else:
        d.rounded_rectangle([x, y, x + 30, y + 30], radius=6, fill=ACCENT)
        d.rectangle([x + 8, y + 13, x + 22, y + 17], fill=NAVY_D)


def section(d, y, title, color, items, kind, note=None):
    x0, x1 = 40, W - 40
    tmp_h = 64
    rows = []
    for name, desc in items:
        nl = wrap_chars(d, name, font(25, True), x1 - x0 - 100)
        dl = wrap_chars(d, desc, font(21), x1 - x0 - 100)
        rows.append((nl, dl, 18 + 34 * len(nl) + 30 * len(dl) + 14))
    h = tmp_h + sum(r[2] for r in rows) + (50 if note else 10)
    d.rounded_rectangle([x0, y, x1, y + h], radius=14, fill="white", outline=LINE, width=2)
    d.rounded_rectangle([x0, y, x1, y + 56], radius=14, fill=color)
    d.rectangle([x0, y + 40, x1, y + 56], fill=color)
    d.text((x0 + 24, y + 10), title, font=font(28, True), fill="white" if color != ACCENT else NAVY_D)
    yy = y + tmp_h
    for nl, dl, rh in rows:
        check_box(d, x0 + 26, yy + 18, kind)
        ty = yy + 14
        for ln in nl:
            d.text((x0 + 74, ty), ln, font=font(25, True), fill=TEXT); ty += 34
        for ln in dl:
            text_fixed(d, (x0 + 74, ty), ln, font(21), GRAY); ty += 30
        yy += rh
    if note:
        d.rounded_rectangle([x0 + 20, yy + 2, x1 - 20, yy + 40], radius=10, fill="#fdecea")
        text_fixed(d, (x0 + 36, yy + 8), note, font(21, True), CORAL)
    return y + h + 22


def make_checklist(out):
    HEAD = 200
    tmp = Image.new("RGB", (W, 4000), BG)
    d = ImageDraw.Draw(tmp)
    header(d, "2027학년도 수능 · 평가원 유의사항 기준", "준비물 · 반입 금지 체크리스트", "시험장에 가져갈 것, 가져가지 말 것, 쉬는 시간에만 볼 수 있는 것", HEAD - 10)
    y = HEAD + 20
    y = section(d, y, "챙길 것 (점심·물을 빼면 시험 중에도 휴대 가능)", NAVY, BRING, "ok")
    y = section(d, y, "가져가지 말 것 (시험장 반입 금지)", CORAL, BAN, "ban",
                note="가져왔다면 1교시 시작 전 감독관에게 제출. 안 내면 부정행위")
    y = section(d, y, "쉬는 시간에만 (매 교시 시작 전 가방에 넣어 제출)", ACCENT, BREAK, "mid")
    y += 8
    text_fixed(d, (40, y), "스마트워치·스마트안경을 1교시 시작 전에 내지 않고 시험 중 착용만 해도", font(21, True), NAVY)
    text_fixed(d, (40, y + 30), "그해 시험 무효, 다음 연도 1년간 응시자격 정지.", font(21, True), NAVY)
    y += 80
    text_fixed(d, (40, y), "출처: 한국교육과정평가원 「2027학년도 대학수학능력시험 수험생 유의사항」 1~3쪽·5쪽·13쪽,", font(19), GRAY)
    text_fixed(d, (40, y + 28), "「2027학년도 대학수학능력시험 실시요강」(2026.8.) 25~26쪽. 전체 목록은 평가원 원문을 확인하세요.", font(19), GRAY)
    H = y + 28 + 100
    img = tmp.crop((0, 0, W, H))
    d = ImageDraw.Draw(img)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("checklist", out, img.size)


# ------------------------------------------------------------------ ③ 흐름 도식
FLOW = [
    ("10/20(화)", "D-30", "남은 기간 계획", "수능 공부와 면접 준비 시간을 나눠 둡니다(이 글의 제안)", PALE),
    ("11/19(목)", "수능", "08:10까지 입실", "종료령 뒤 가채점표 작성은 부정행위 · 옮겨 적기는 시험 시간 안에(이 글의 제안)", CORAL),
    ("11/19(목)~", "가채점", "정답 공개 · 수능최저 대조", "매 교시 종료 뒤 평가원 홈페이지 공개 · 이의신청 11/23(월)까지", ACCENT),
    ("11/21(토)~", "면접", "수능 뒤 면접", "예) 이화여대·한국외대 11/21~22 · 숙명여대 11/28~29 · 건국대 12/5·6 · 동국대 12/11~13", PALE),
    ("12/1(화)", "정답 확정", "17:00 평가원 홈페이지", "가채점을 확정 정답으로 다시 맞춰 봅니다", PALE),
    ("12/11(금)", "성적 통지", "성적통지표", "재학생 학교 09:00 이후·온라인 14:00부터 / 졸업생 온라인 09:00부터", NAVY),
    ("12/18(금)까지", "수시 발표", "수시 합격자 발표", "등록 12/21(월)~23(수)", PALE),
]


def make_flow(out):
    HEAD = 200
    RH = 128
    H = HEAD + 20 + RH * len(FLOW) + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "2027학년도 수능 전후 일정", "D-30부터 수시 발표까지", "날짜는 평가원 실시요강·시행기본계획, 대교협 시행계획, 각 대학 모집요강 기준", HEAD - 10)
    y = HEAD + 24
    x0, x1 = 40, W - 40
    for i, (date, tag, title, desc, col) in enumerate(FLOW):
        dark = col in (CORAL, NAVY)
        d.rounded_rectangle([x0, y, x1, y + RH - 22], radius=14, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 210, y + RH - 22], radius=14, fill=col)
        d.rectangle([x0 + 190, y, x0 + 210, y + RH - 22], fill=col)
        tc = "white" if dark else NAVY_D
        d.text((x0 + 20, y + 12), tag, font=font(32, True), fill=tc)
        text_fixed(d, (x0 + 20, y + 58), date, font(21, True), tc)
        d.text((x0 + 234, y + 12), title, font=font(28, True), fill=NAVY)
        lines = wrap_chars(d, desc, font(20), x1 - x0 - 260)
        for j, ln in enumerate(lines[:2]):
            text_fixed(d, (x0 + 234, y + 52 + 26 * j), ln, font(20), TEXT)
        y += RH
        if i < len(FLOW) - 1:
            cx = x0 + 105
            d.polygon([(cx - 12, y - 20), (cx + 12, y - 20), (cx, y - 2)], fill=NAVY)
    y += 4
    text_fixed(d, (40, y), "면접일 예시 5곳 중 4곳(이화여대·한국외대·숙명여대·건국대)은 성적 통지(12/11) 전에 면접을 봅니다(이 글에서 센 값).", font(19), GRAY)
    text_fixed(d, (40, y + 28), "그래서 면접 전에는 가채점으로 수능최저를 가늠해 둡니다. 모집단위별 면접일은 지원 대학 모집요강·입학처 공지로 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("flow", out, img.size)


def jobs_csat():
    make_thumb(HERE / "thumb-csat.png", "2027 수능", line2="D-30 체크리스트", line3="시간표·준비물·면접", chip="11월 19일(목) 수능")
    make_timetable(HERE / "csat-timetable.png")
    make_checklist(HERE / "csat-checklist.png")
    make_flow(HERE / "csat-flow.png")


if __name__ == "__main__":
    jobs_csat()
