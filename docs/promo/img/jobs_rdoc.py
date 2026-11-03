# 2027 지역의사제 전형 총정리(naver-128) 블로그 글 이미지. 실행: python -I jobs_rdoc.py
# 숫자·날짜는 site/content/regional_doctor.json(독립 검수 2회)에서 옮겼고, 2026-11-03 각 대학 2027학년도 수시모집요강 PDF 로 다시 확인했다.
# 표 디자인은 jobs_results.py 의 header / make_date_table / make_time_table 을 복사해 고쳐 썼다.
# 동아·영남·인제·조선대 요강은 그림 PDF(글자 추출 불가)라 make_capture(글자 검색) 대신 좌표로 자르는 make_capture_y 를 이 파일에 두었다
# (promo_style.make_capture 와 같은 틀).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf
from PIL import Image, ImageDraw
from promo_style import (HERE, SRC, make_thumb, make_capture, pdf, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

# ---------------------------------------------------------------- 표 1: 면접 있는 지역의사 전형 (면접일 순)
# (대학, 전형, 인원 "총(진료권·광역권)", 1단계 발표, 면접일)
T1 = [
    ("순천향대", "학생부교과 지역의사선발", "18 (12·6)", "10/21(수) 17:00", "10/31(토)"),
    "수능",
    ("경북대", "학생부종합 지역의사선발", "26 (18·8)", "11/6(금) 16:00", "11/21(토)"),
    ("울산대", "학생부교과형 지역의사제 특별", "5 (5·0)", "11/17(화) 16:00", "11/21(토)"),
    ("인하대", "학생부종합 지역의사선발", "6 (6·0)", "11/17(화)", "11/21(토)"),
    ("경상국립대", "학생부종합 지역의사선발", "22 (16·6)", "11/13(금) 16:00", "11/25(수)~26(목)"),
    ("동아대", "지역의사제 광역권", "5 (0·5)", "11/20(금) 14:00", "11/27(금) 08:00"),
    ("건국대(글로컬)", "학생부교과 지역의사제", "7 (5·2)", "11/19(목)", "11/28(토)"),
    ("계명대", "학생부종합 지역의사진료", "11 (11·0)", "11/14(토)", "11/28(토)"),
    ("단국대(천안)", "지역의료인재(진료권)", "11 (11·0)", "11/20(금) 18:00", "11/28(토)"),
    ("단국대(천안)", "지역의료인재(광역권)", "4 (0·4)", "11/20(금) 18:00", "11/28(토)"),
    ("동아대", "지역의사제 진료권(5개 권역)", "12 (12·0)", "11/20(금) 14:00", "11/28(토) 08:00"),
    ("연세대(미래)", "강원인재(지역의사)", "11 (8·3)", "일괄 선발", "11/28(토)"),
    ("영남대", "학생부종합 지역의사선발(진료권)", "9 (9·0)", "11/13(금) 17:00", "11/28(토) 15:00"),
    ("원광대", "학생부종합 지역의사선발", "17 (12·5)", "11/20(금)", "12/2(수)"),
    ("전남대", "학생부종합 지역의사_진료권", "22 (22·0)", "11/13(금) 15:00", "12/2(수)"),
    ("제주대", "학생부종합 지역의사(광역권 제주)", "2 (0·2)", "11/13(금) 10:00", "12/4(금)"),
    ("계명대", "학생부교과 지역의사광역", "4 (0·4)", "11/14(토)", "12/5(토)"),
    ("부산대", "학생부종합 지역의사선발", "31 (22·9)", "12/1(화) 16:00", "12/5(토)"),
    ("인제대", "학생부교과 지역의사", "15 (11·4)", "11/4(수) 14:00", "12/5(토)"),
    ("성균관대", "학생부종합 성균인재-지역인재", "3 (3·0)", "12/1(화)", "12/6(일)"),
    ("한림대", "학생부종합 지역의사(의학과)", "7 (6·1)", "12/3(목) 16:00", "12/9(수)"),
    ("아주대", "학생부종합 지역의사선발(의학과)", "6 (6·0)", "12/12(토)", "12/14(월)"),
]

# ---------------------------------------------------------------- 표 2: 면접 없는 지역의사 전형
# (대학, 전형, 인원, 선발 방법, 수능최저 요약)
T2 = [
    ("가천대", "학생부교과 지역의사선발", "7 (7·0)", "교과 100%", "국·수·영·탐 중 3개 영역 각 1등급"),
    ("강원대", "학생부교과 지역의사선발", "39 (27·12)", "교과 100%", "국·수·영·과탐 중 3합 7|수학·과탐 필수 반영"),
    ("영남대", "학생부교과 지역의사선발(광역권)", "4 (0·4)", "학생부 100%", "수학 포함 3합 4"),
    ("을지대", "학생부교과 지역의사선발", "6 (5·1)", "교과 100%", "3합 5|과탐 필수, 생명과학 1과목 이상"),
    ("전북대", "학생부교과 지역의사선발|(광역권·5개 진료권)", "21 (15·6)", "교과 100%", "수학 포함 3합 6"),
    ("제주대", "학생부교과 지역의사(진료권 2·광역권)", "18 (13·5)", "교과 100%", "수학 포함 3합 6"),
    ("조선대", "학생부교과 지역의사선발", "19 (13·6)", "학생부 100%", "3합 6(수학 의무 반영)"),
    ("충남대", "학생부종합Ⅱ(지역의사선발)", "27 (19·8)", "서류 100%", "국·영·과탐 상위 2개 + 수학 합 6"),
    ("충북대", "학생부교과 지역의사(진료권 3·광역권)", "26 (18·8)", "교과 100%", "상위 3합 6"),
]

# ---------------------------------------------------------------- 표 3: 수능최저 기준별 (칩), True = 사회탐구도 인정
T3 = [
    ("최저 없음", [("성균관대", False), ("인하대", False), ("제주대(종합)", False)]),
    ("4개 영역 각 2등급", [("인제대", False)]),
    ("3개 영역 각 1등급", [("가천대", True)]),
    ("4개 영역 합 6", [("아주대", True)]),
    ("3개 영역 합 4", [("계명대(광역)", False), ("동아대(광역)", True), ("부산대 +한국사 4", True), ("영남대(광역)", False)]),
    ("3개 영역 합 5", [("경북대", True), ("계명대(진료)", False), ("단국대(광역)", False), ("동아대(진료)", True),
                    ("순천향대", True), ("연세대(미래) +한국사 4", False), ("영남대(진료)", False),
                    ("울산대 +한국사 4", False), ("을지대", False), ("한림대", False)]),
    ("3개 영역 합 6", [("건국대(글로컬) +한국사 4", False), ("경상국립대", False), ("단국대(진료)", False), ("원광대", False),
                    ("전남대", False), ("전북대", False), ("제주대(교과)", False), ("조선대", False),
                    ("충북대", False), ("충남대(상위 2 + 수학)", False)]),
    ("3개 영역 합 7", [("강원대", False)]),
]

FOOT = "출처: 각 대학 2027학년도 수시모집요강. 면접 시각·장소는 1단계 발표 때 입학처 공지로 다시 확인하세요."


def header(d, title, sub, chip="2027 지역의사 선발전형"):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    return HEAD


def fit(d, text, size, bold, maxw, minsize=15):
    """maxw 안에 들어갈 때까지 글자 크기를 줄인다."""
    s = size
    while s > minsize and d.textlength(text, font=font(s, bold)) > maxw:
        s -= 1
    return font(s, bold)


def make_table1(out):
    COLS = [(44, 196, "대학"), (246, 360, "전형"), (612, 150, "인원(진료·광역)"), (770, 200, "1단계 발표"), (982, 178, "면접일")]
    RH, DIV = 62, 44
    rows = [r for r in T1 if r != "수능"]
    H = 200 + 58 + RH * len(rows) + DIV + 190
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    seats_sum = sum(int(r[2].split()[0]) for r in rows)
    y = header(d, "면접 있는 지역의사 전형, 면접일 순", f"{len({r[0] for r in rows})}개 대학 · 수시 {seats_sum}명")
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * len(rows) + DIV + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(21, True)
    for x, _, lab in COLS:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    k = 0
    for r in T1:
        if r == "수능":
            d.rectangle([26, y, W - 26, y + DIV], fill="#fff4d6")
            t = "11/19(목) 수능  ·  아래는 수능 뒤 면접"
            text_fixed(d, (44, y + 9), t, font(21, True), NAVY_D)
            y += DIV
            continue
        univ, track, seats, first, date = r
        done = univ == "순천향대"
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        cu = GRAY if done else TEXT
        d.text((COLS[0][0], y + 15), univ, font=fit(d, univ, 25, True, COLS[0][1]), fill=cu)
        text_fixed(d, (COLS[1][0], y + 19), track, fit(d, track, 20, False, COLS[1][1]), GRAY)
        d.text((COLS[2][0], y + 16), seats, font=fit(d, seats, 23, True, COLS[2][1]), fill=GRAY if done else NAVY)
        text_fixed(d, (COLS[3][0], y + 18), first, fit(d, first, 21, False, COLS[3][1]), GRAY if done else TEXT)
        d.text((COLS[4][0], y + 15), date, font=fit(d, date, 24, True, COLS[4][1]), fill=GRAY if done else CORAL)
        y += RH
        k += 1
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    notes = [
        "인원: 수시 모집인원(진료권·광역권). 1단계 발표 시각은 모집요강에 적힌 것만 넣었습니다(일부 '예정' 표기).",
        "경상국립대는 학생부종합 면접 공통 기간(의예과 날짜 따로 없음). 연세대(미래)는 일괄 선발, 면접장소 공개 11/24(화) 17:00.",
        "순천향대 면접(10/31)은 수능 전에 끝났습니다. " + FOOT,
    ]
    for j, t in enumerate(notes):
        text_fixed(d, (40, y + 30 * j), t, fit(d, t, 19, False, W - 80), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table1", out.name, img.size, len(rows))


def make_table2(out):
    COLS = [(44, 130, "대학"), (184, 330, "전형"), (524, 140, "인원(진료·광역)"), (676, 130, "선발 방법"), (816, 344, "수능최저")]
    RH = 84
    H = 200 + 58 + RH * len(T2) + 170
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    total = sum(int(r[2].split()[0]) for r in T2)
    y = header(d, "면접 없는 지역의사 전형", f"{len(T2)}개 대학 · 수시 {total}명")
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * len(T2) + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(21, True)
    for x, _, lab in COLS:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    for k, (univ, track, seats, how, mn) in enumerate(T2):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        d.text((COLS[0][0], y + 26), univ, font=fit(d, univ, 25, True, COLS[0][1]), fill=TEXT)
        ft = font(20)
        tl = track.split("|") if "|" in track else wrap_chars(d, track, ft, COLS[1][1])[:2]
        for j, ln in enumerate(tl):
            text_fixed(d, (COLS[1][0], y + (30 if len(tl) == 1 else 15) + 28 * j), ln, ft, GRAY)
        d.text((COLS[2][0], y + 27), seats, font=fit(d, seats, 23, True, COLS[2][1]), fill=NAVY)
        text_fixed(d, (COLS[3][0], y + 29), how, fit(d, how, 21, False, COLS[3][1]), TEXT)
        fm = font(20, True)
        ml = mn.split("|") if "|" in mn else wrap_chars(d, mn, fm, COLS[4][1])[:2]
        for j, ln in enumerate(ml):
            d.text((COLS[4][0], y + (29 if len(ml) == 1 else 14) + 28 * j), ln, font=fm, fill=CORAL)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    notes = ["인원: 수시 모집인원(진료권·광역권). 전북대·제주대·충북대는 진료권별로 나뉜 전형을 한 줄로 묶었습니다.",
             "수능최저의 탐구 과목 수·평균 처리·지정 과목은 대학마다 다릅니다. " + FOOT]
    for j, t in enumerate(notes):
        text_fixed(d, (40, y + 30 * j), t, fit(d, t, 19, False, W - 80), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table2", out.name, img.size, total)


def make_table3(out):
    """수능최저 기준별: 왼쪽 기준 칸 + 오른쪽 대학 칩(줄바꿈). 사회탐구도 인정하는 곳은 다른 색."""
    LX, CX, CW = 44, 300, W - 300 - 44
    fchip = font(22, True)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    SA = "#fde4da"

    def layout(names):
        rows, cur, x = [], [], 0
        for n, sa in names:
            w = tmp.textlength(n, font=fchip) + 32
            if cur and x + w > CW:
                rows.append(cur); cur, x = [], 0
            cur.append((n, sa, w)); x += w + 12
        rows.append(cur)
        return rows

    blocks = [(t, layout(ns)) for t, ns in T3]
    CH, GAP = 44, 10
    body = sum(len(r) * (CH + GAP) - GAP + 26 for _, r in blocks)
    H = 200 + 20 + body + 20 + 160
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    total = sum(len(ns) for _, ns in T3)
    y = header(d, "지역의사 전형 수능최저, 기준별", "26개 대학 · 수시 지역의사 전형")
    d.rounded_rectangle([24, y, W - 24, y + body + 20], radius=14, fill="white", outline=LINE, width=2)
    y += 20
    for k, (t, rows) in enumerate(blocks):
        h = len(rows) * (CH + GAP) - GAP
        ft = fit(d, t, 28, True, CX - LX - 20)
        d.text((LX, y + (h - 34) / 2), t, font=ft, fill=NAVY if t != "최저 없음" else GRAY)
        yy = y
        for r in rows:
            x = CX
            for n, sa, w in r:
                d.rounded_rectangle([x, yy, x + w, yy + CH], radius=12, fill=SA if sa else PALE)
                d.text((x + 16, yy + 8), n, font=fchip, fill=NAVY_D)
                x += w + 12
            yy += CH + GAP
        y += h + 16
        if k < len(blocks) - 1:
            d.line([40, y, W - 40, y], fill="#edf0f4", width=2)
        y += 10
    y += 20
    d.rounded_rectangle([40, y + 2, 64, y + 24], radius=6, fill=SA)
    text_fixed(d, (74, y), "사회탐구도 인정(순천향대는 과학탐구가 아니면 0.5등급 하향)", font(20, True), TEXT)
    d.rounded_rectangle([700, y + 2, 724, y + 24], radius=6, fill=PALE)
    text_fixed(d, (734, y), "과학탐구만 반영 또는 최저 없음", font(20, True), TEXT)
    t = "'3개 영역 합'은 수학 포함 여부·탐구 1과목/2과목 평균 등 세부 조건이 대학마다 다릅니다. " + "모집요강 원문을 확인하세요."
    text_fixed(d, (40, y + 40), t, fit(d, t, 19, False, W - 80), GRAY)
    text_fixed(d, (40, y + 70), "출처: 각 대학 2027학년도 수시모집요강 수능최저학력기준. 묶음과 색 구분은 이 글에서 정리한 것입니다.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table3", out.name, img.size, total)


# ---------------------------------------------------------------- 좌표로 자르는 캡처 (그림 PDF 용, make_capture 와 같은 틀)
def make_capture_y(out, pdf_path, page, x0, y0, x1, y1, univ, doc_label, note, dpi=200):
    pg = pymupdf.open(pdf_path)[page - 1]
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    Wc = shot.width + 80
    HEAD, FOOT_H = 104, 92
    img = Image.new("RGB", (Wc, HEAD + shot.height + 40 + FOOT_H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, Wc, HEAD], fill=NAVY)
    fc = font(30, True)
    chip = "2027학년도 모집요강"
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 44, 26 + 52], radius=26, fill=ACCENT)
    d.text((40 + 22, 31), chip, font=fc, fill=NAVY_D)
    d.text((40 + cw + 70, 30), univ, font=font(38, True), fill="white")
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    fy = HEAD + shot.height + 40
    text_fixed(d, (40, fy + 10), f"출처: {univ} {doc_label}", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((Wc - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture_y", out.name, img.size)


def jobs_rdoc():
    make_thumb(HERE / "thumb-rdoc.png", "지역의사제", line2="전형 총정리", line3="면접일·수능최저·10년",
               chip="2027 지역의사 선발전형")
    make_table1(HERE / "rdoc-table-1.png")
    make_table2(HERE / "rdoc-table-2.png")
    make_table3(HERE / "rdoc-table-3.png")
    # 캡처 1: 영남대 12쪽(그림 PDF, 인쇄 쪽 = PDF 쪽) 지역의사제란? + 의무복무조건
    make_capture_y(HERE / "yu-2027-rdoc-define.png", pdf("영남대학교"), 12, 50, 96, 552, 326,
                   "영남대학교", "2027학년도 수시 신입생 모집요강 12쪽", "졸업 후 10년, 근무 시작한 날부터 셈")
    # 캡처 2: 조선대 32쪽(PDF 38쪽, 그림 PDF) 진료권·광역권 선발 지원 가능 여부
    make_capture_y(HERE / "chosun-2027-rdoc-move.png", pdf("조선대학교"), 38, 132, 462, 532, 574,
                   "조선대학교", "2027학년도 수시모집요강 32쪽(PDF 38쪽)", "고교 때 전학·이사하면 지원 가능한 권역이 달라집니다")
    # 캡처 3: 계명대 8쪽(인쇄 = PDF) 의무복무 안내
    make_capture(HERE / "kmu-2027-rdoc-duty.png", pdf("계명대학교"), 8, "전형 신설",
                 ("after", "지역의사 지원 등에 관한 고시"), "계명대학교", "2027학년도 신입생 수시모집요강 8쪽",
                 "면허 취득 순간부터 최소 10년, 근무지 자유 변경 불가", start_pad=6, end_pad=6)


if __name__ == "__main__":
    jobs_rdoc()
