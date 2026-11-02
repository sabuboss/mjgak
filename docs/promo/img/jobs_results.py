# 2027 수시 합격자 발표일 총정리 블로그 글 이미지. python jobs_results.py
# 날짜·시간은 site/content/rich/univ/<code>.json 의 after(각 대학 2027학년도 수시모집요강에서 확인, 출처 쪽수는 after.source)에서 옮겼다.
# 표에는 '예정'·'이후'·'이전' 같은 꼬리말을 줄였다(각주로 안내). 실기·특기자·재외국민·예체능 서류 전형 날짜는 넣지 않았다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, make_capture, pdf, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

# 12월 18일(금) 최초합격자 발표 — 시간별 (면접이 있는 전형 기준)
T1 = [
    ("09:00", ["한국항공대"]),
    ("10:00", ["서울교대", "진주교대", "대구교대", "제주대", "KAIST", "POSTECH", "한국해양대", "숭실대", "성신여대"]),
    ("13:00", ["전주교대"]),
    ("14:00", ["중앙대", "한국외대", "건국대", "서울과기대", "전북대", "경인교대", "춘천교대", "창원대", "동아대",
               "인제대(의예·약학 등)"]),
    ("15:00", ["충남대", "전남대", "강원대", "한밭대", "총신대", "영남대"]),
    ("16:00", ["가톨릭대", "차의과대", "경상국립대", "경북대", "부산대", "울산대"]),
    ("17:00", ["고려대", "고려대(세종)", "서강대", "숙명여대", "국민대", "세종대", "덕성여대", "동덕여대(약학과)",
               "충북대", "부산교대", "부경대", "순천향대", "서경대", "수원대(고교추천)", "연세대(미래)"]),
    ("18:00", ["서울대", "경희대", "단국대", "한양대 ERICA", "서울여대", "GIST", "목포대"]),
    ("시간 미표기", ["아주대", "한양대", "인하대", "동국대", "서울시립대", "인천대", "가천대(수능일 이후)", "을지대",
                "강남대", "홍익대", "계명대", "조선대", "원광대", "협성대", "나사렛대(간호 최저 적용)"]),
    ("12/18 이전·까지", ["성균관대", "UNIST", "한국공학대", "경기대"]),
]

# 12월 18일이 아닌 날 발표 — (발표일, 시간, 대학, 전형)
T2 = [
    ("10/16(금)", "15:00", "용인대", "일반학생·기타 특별전형"),
    ("10/28(수)", "14:00", "남부대", "수능최저 미적용 학과"),
    ("11/2(월)", "14:00", "삼육대", "수능최저 미적용 전형"),
    ("11/5(목)", "17:00", "경남대", "일반면접전형(수능최저 미적용)"),
    ("11/6(금)", "10:00", "한신대", "참인재전형 등(논술전형 외)"),
    ("11/6(금)", "14:00", "성결대", ""),
    ("11/6(금)", "15:00", "국립경국대", "수능최저 미적용 모집단위"),
    ("11/6(금)", "15:00", "광운대", "광운참빛인재Ⅰ(면접형)·소프트웨어우수인재"),
    ("11/6(금)", "17:00", "수원대", "면접위주교과"),
    ("11/10(화)", "", "한세대", "면접우수자"),
    ("11/10(화)", "", "나사렛대", "수능최저 미적용 전형"),
    ("11/13(금)", "", "안양대", ""),
    ("11/13(금)", "", "한국기술교육대", "창의인재(면접형) 등"),
    ("11/13(금)", "14:00", "대진대", "윈윈대진"),
    ("11/13(금)", "16:00", "성공회대", ""),
    ("11/13(금)", "18:00", "한양대 ERICA", "조기취업형 계약학과"),
    ("11/14(토)", "", "가천대", "수능일 이전 발표분"),
    ("11/16(월)~17(화)", "", "신한대", "학생부교과·실기위주"),
    ("11/17(화)", "11:00", "남서울대", ""),
    ("11/17(화)", "14:00", "청주대", "항공운항학과·군사학과 제외"),
    ("11/17(화)", "17:00", "동덕여대", "동덕창의리더(약학과 제외)"),
    ("11/18(수)", "14:00", "한경국립대", "학생부교과(특수교육대상자)"),
]
T3 = [
    ("11/20(금)", "14:00", "인제대", "면접전형(글로컬리더스 이공 제외) 등"),
    ("11/24(화)", "", "호서대", ""),
    ("11/24(화)", "10:00", "상명대", "천안"),
    ("11/25(수)", "16:00", "선문대", ""),
    ("11/27(금)", "17:00", "백석대", ""),
    ("12/3(목)", "", "이화여대", "미래인재전형(면접형)"),
    ("12/3(목)", "09:00", "상명대", "서울"),
    ("12/9(수)", "15:00", "명지대", ""),
    ("12/11(금)", "14:00", "대진대", "학생부우수자·종단추천자"),
    ("12/11(금)", "18:00", "KENTECH", ""),
    ("12/15(화)", "14:00", "청주대", "항공운항학과·군사학과"),
    ("12/15(화)", "14:00", "삼육대", "수능최저 적용 전형"),
    ("12/16(수)", "14:00", "남부대", "간호학과(일반학생)"),
    ("12/16(수)", "15:00", "용인대", "교과성적우수자"),
    ("12/16(수)", "17:00", "경남대", "수능최저 적용 전형(간호·물리치료, 체육교육과, 군사학과)"),
    ("12/17(목)", "10:00", "한국교원대", ""),
    ("12/17(목)", "16:00", "한림대", "학생부종합"),
    ("2027. 1/4(월)", "17:00", "경찰대학", ""),
]

NOTE_TAIL = "'예정'·'이후'·'이전' 표기는 줄였습니다. 발표 방법과 정확한 시각은 각 대학 입학처 공지로 다시 확인하세요."


def header(d, title, sub, chip="2027 수시 · 최초합격자 발표"):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    return HEAD


def make_time_table(out):
    """12/18 발표 대학을 시간별로: 왼쪽 시간 칸 + 오른쪽 대학 이름 칩(줄바꿈)."""
    LX, CX, CW = 44, 250, W - 250 - 44
    fchip = font(23, True)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    def layout(names):
        rows, cur, x = [], [], 0
        for n in names:
            w = tmp.textlength(n, font=fchip) + 32
            if cur and x + w > CW:
                rows.append(cur); cur, x = [], 0
            cur.append((n, w)); x += w + 12
        rows.append(cur)
        return rows

    blocks = [(t, layout(ns)) for t, ns in T1]
    CH, GAP = 46, 10
    body = sum(len(r) * (CH + GAP) - GAP + 26 for _, r in blocks)
    H = 200 + 20 + body + 20 + 130
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    total = sum(len(ns) for _, ns in T1)
    y = header(d, "12월 18일(금) 발표 대학, 시간별", f"{total}개 대학")
    d.rounded_rectangle([24, y, W - 24, y + body + 20], radius=14, fill="white", outline=LINE, width=2)
    y += 20
    for k, (t, rows) in enumerate(blocks):
        h = len(rows) * (CH + GAP) - GAP
        col = NAVY if ":" in t else GRAY
        ft = font(34 if ":" in t else 24, True)
        d.text((LX, y + (h - (40 if ":" in t else 30)) / 2), t, font=ft, fill=col)
        yy = y
        for r in rows:
            x = CX
            for n, w in r:
                fill = PALE if ":" in t else "#eef0f3"
                d.rounded_rectangle([x, yy, x + w, yy + CH], radius=12, fill=fill)
                d.text((x + 16, yy + 8), n, font=fchip, fill=NAVY_D)
                x += w + 12
            yy += CH + GAP
        y += h + 16
        if k < len(blocks) - 1:
            d.line([40, y, W - 40, y], fill="#edf0f4", width=2)
        y += 10
    y += 20
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강(전형일정·합격자 발표). 같은 대학도 전형마다 발표일이 다를 수 있습니다.", font(19), GRAY)
    text_fixed(d, (40, y + 30), NOTE_TAIL, font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("time", out, img.size, total)


def make_date_table(out, rows, title, sub, chip):
    RH = 66
    COLS = [(44, 300), (360, 120), (490, 670)]
    n = len(rows)
    H = 200 + 58 + RH * n + 160
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, title, sub, chip)
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for (x, _), lab in zip(COLS, ["발표일", "시각", "대학 · 전형"]):
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    prev = None
    for k, (day, tm, univ, track) in enumerate(rows):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        if day != prev:
            text_fixed(d, (COLS[0][0], y + 17), day, font(26, True), NAVY)
        prev = day
        text_fixed(d, (COLS[1][0], y + 19), tm or "-", font(23, True), CORAL if tm else GRAY)
        fu = font(26, True)
        d.text((COLS[2][0], y + 15), univ, font=fu, fill=TEXT)
        if track:
            x = COLS[2][0] + d.textlength(univ, font=fu) + 16
            ft = font(20)
            t = track
            while d.textlength(t, font=ft) > W - 50 - x and len(t) > 2:
                t = t[:-2] + "…"
            text_fixed(d, (x, y + 21), t, ft, GRAY)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강. 실기·특기자·재외국민 등 일부 전형 날짜는 넣지 않았습니다.", font(19), GRAY)
    text_fixed(d, (40, y + 30), NOTE_TAIL, font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("date", out, img.size, n)


FLOW = [
    ("1", "최초합격자 발표", "~ 12/18(금)", "입학처 홈페이지에서 직접 조회합니다. 적어도 57개 대학이 '개별 통보 없음'을 적었습니다.", NAVY),
    ("2", "최초합격자 등록", "12/21(월) ~ 23(수)", "98개 대학이 이 기간입니다. 문서등록 또는 예치금 납부, 마감 시각은 대학마다 다릅니다.", BLUE),
    ("3", "충원(추가) 합격 발표", "12/23(수) ~ 29(화)", "홈페이지 발표 또는 전화 통보. 적어도 86개 대학이 마감을 12/29(화) 18시로 적었습니다.", CORAL),
    ("4", "충원 합격자 등록 마감", "12/30(수)", "충원 합격자도 정해진 시각까지 등록해야 합니다. 대학마다 마감 시각이 다릅니다.", NAVY_D),
    ("5", "등록금 납부(본등록)", "2027. 2/10(수) ~ 12(금)", "75개 대학 이상이 이 기간입니다. 고려대(2/15~16)처럼 기간이 다른 대학도 있습니다.", GRAY),
]


def make_flow(out):
    BOX, GAP, HEAD = 140, 40, 180
    H = HEAD + (BOX + GAP) * len(FLOW) - GAP + 140
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "합격자 발표 → 등록 → 충원 → 본등록", font=font(42, True), fill="white")
    d.text((48, 90), "이 글에서 확인한 101개 대학 수시모집요강의 공통 흐름. 날짜가 다른 대학은 본문 참고.", font=font(23), fill=PALE)
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
        for j, ln in enumerate(wrap_chars(d, desc, f_d, x1 - x0 - 320)[:3]):
            text_fixed(d, (x0 + 286, y + 62 + 27 * j), ln, f_d, TEXT)
        if i < len(FLOW) - 1:
            cx = x0 + 130
            d.polygon([(cx - 18, y + BOX + 6), (cx + 18, y + BOX + 6), (cx, y + BOX + GAP - 6)], fill=GRAY)
        y += BOX + GAP
    y += 4
    text_fixed(d, (40, y), "수시에 최종 합격(충원 합격 포함)하면 등록하지 않아도 정시·추가모집에 지원할 수 없습니다(특별법 설치 대학 등 예외).", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("flow", out, img.size)


def jobs_results():
    make_thumb(HERE / "thumb-results.png", "수시 합격자", line2="발표일 총정리", line3="12/18 시간별 · 등록 · 충원",
               chip="2027 수시 합격자 발표")
    make_flow(HERE / "results-flow.png")
    make_time_table(HERE / "results-table-1.png")
    make_date_table(HERE / "results-table-2.png", T2, "12월 18일이 아닌 날 발표 ① 수능 전", f"{len(T2)}개 전형 · 날짜순", "2027 수시 · 수능 11/19(목) 전 발표")
    make_date_table(HERE / "results-table-3.png", T3, "12월 18일이 아닌 날 발표 ② 수능 뒤", f"{len(T3)}개 전형 · 날짜순", "2027 수시 · 수능 11/19(목) 뒤 발표")
    a = pdf("아주대학교")
    make_capture(HERE / "ajou-2027-results-multi.png", a, 59, "나. 복수 지원 금지사항", ("after", "한국방송통신대학교 등"),
                 "아주대학교", "2027학년도 수시모집요강 57쪽(PDF 59쪽)", "수시 합격자는 등록 의사와 관계없이 정시·추가모집 지원 불가",
                 start_pad=4, end_pad=0)
    make_capture(HERE / "ajou-2027-results-double.png", a, 61, "가. 대입지원방법 위반에 따른 입학취소", ("after", "검출되는 경우 입학이 취소됨"),
                 "아주대학교", "2027학년도 수시모집요강 59쪽(PDF 61쪽)", "수시 등록은 한 대학만, 중복 등록하면 모든 대학 입학 취소",
                 start_pad=4, end_pad=0)


if __name__ == "__main__":
    jobs_results()
