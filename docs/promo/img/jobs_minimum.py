# 수능 가채점 후 수능최저 확인 + 수능 뒤 면접·최저 있는 전형 블로그 글 이미지. python jobs_minimum.py
# 전형·최저 적용 모집단위·면접일은 site/content/rich/univ/<code>.json 의 tracks[].min·date(각 대학 2027학년도 모집요강 확인)에서 옮겼다.
# 수능 일정은 site/templates/suneung.html(평가원 실시요강·시행기본계획 대조 검수본).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, make_capture, pdf, font, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

TIMELINE = [
    ("11/19(목)", "수능 · 가채점", "가채점표(수험표 뒷면)는 시험 시간 안에 적습니다. 문제·정답은 매 교시 뒤 평가원 홈페이지에 공개됩니다.", NAVY),
    ("11/19 ~ 23(월)", "정답 이의신청", "평가원 이의신청 게시판. 가채점 결과로 지원 전형의 수능최저부터 확인합니다.", BLUE),
    ("11/21 ~ 12/15", "수능 뒤 면접", "이 글의 표에 넣은 수능최저 있는 면접 전형 54개가 이 기간에 면접을 봅니다.", CORAL),
    ("12/1(화) 17:00", "정답 확정", "평가원이 정답을 확정 발표합니다.", NAVY_D),
    ("12/11(금)", "성적 통지", "등급이 확정되는 날입니다. 표 54개 중 52개는 이보다 먼저 면접을 봅니다(아주대·가천대 의약학 제외).", NAVY),
    ("~ 12/18(금)", "최초합격자 발표", "수시 최초합격자 발표 마감일(대교협 공통 일정)입니다.", GRAY),
]

PARTS = [
    ("1", "반영 영역", "국어·수학·영어·과학탐구", "이 영역 중에서 고릅니다. 사회탐구를 인정하는지, 직업탐구·제2외국어를 빼는지 대학마다 다릅니다."),
    ("2", "선택과목 조건", "수학(미적분/기하)", "확률과 통계를 고르면 최저에 넣을 수 없거나 등급을 낮춰 계산하는 대학이 있습니다."),
    ("3", "탐구 계산", "과탐 2과목 평균(소수점 절사)", "2과목 평균인지, 상위 1과목인지, 평균을 자르는지(절사) 반올림하는지 확인합니다."),
    ("4", "몇 개 · 합", "수학 포함 3개 영역 합 5 이내", "가장 좋은 등급 3개를 고르되, 수학을 꼭 넣어야 하는 조건입니다."),
    ("5", "별도 조건", "한국사 4등급 이내", "합과 따로 맞춰야 합니다. 영어 등급을 따로 정한 대학도 있습니다."),
]

# (면접일, 대학, 전형, 최저 적용 모집단위)
R1 = [
    ("11/21(토)", "서울교대", "학교장추천·교직인성우수자 등", "전 모집단위"),
    ("11/21(토)", "경북대", "지역인재·지역의사선발", "의예·치의예·약학"),
    ("11/21(토)", "경북대", "지역인재 학교장추천", "치의예과"),
    ("11/21(토)", "경북대", "모바일과학인재(정원외)", "해당 전형"),
    ("11/21(토)", "울산대", "지역교과·지역의사제", "의예과"),
    ("11/21(토)", "인제대", "의예·약학전형 등", "의예과·약학과"),
    ("11/21(토)", "인제대", "지역인재Ⅰ", "약학과·간호학과"),
    ("11/21(토)", "계명대", "학생부교과 일반·지역기회균형", "의예과"),
    ("11/21(토)", "영남대", "창의인재", "전공자유선택학부"),
    ("11/22(일)", "계명대", "학생부교과 지역", "의예과"),
    ("11/25~26", "경상국립대", "학생부종합 일반(면접)", "의예·약학·수의예"),
    ("11/25~26", "경상국립대", "지역인재·지역의사선발 등", "의예과"),
    ("11/26(목)", "전북대", "큰사람", "간호·수의예·약학·의예·치의예"),
    ("11/26(목)", "한국해양대", "지역인재(학생부교과)", "전 모집단위"),
    ("11/27(금)", "서울대", "일반전형(미술대학)", "디자인과"),
    ("11/27(금)", "동아대", "지역인재종합·지역의사제 광역권", "의예과"),
    ("11/27(금)", "목포대", "지역인재(종합)", "약학과"),
    ("11/27~29", "수원대", "고교추천", "해당 전형"),
    ("11/28(토)", "가톨릭대", "지역균형", "의예과"),
    ("11/28(토)", "차의과대", "CHA학생부교과·학생부종합", "약학대학"),
    ("11/28(토)", "단국대(천안)", "DKU인재(면접형)·지역의료인재 등", "의학·약학계열"),
    ("11/28(토)", "인제대", "지역인재Ⅰ", "의예과"),
    ("11/28(토)", "동아대", "지역의사제 진료권", "의예과"),
    ("11/28(토)", "강원대", "지역인재면접(춘천)", "의예과"),
    ("11/28(토)", "계명대", "학생부종합 일반·지역의사진료", "의예과"),
    ("11/28(토)", "전북대", "지역인재 1유형·2유형", "간호·수의예·약학·의예·치의예"),
    ("11/28(토)", "울산대", "지역인재(기초생활/차상위 포함)", "의예과"),
]
R2 = [
    ("11/28(토)", "영남대", "지역인재·지역의사선발", "의예과"),
    ("11/28(토)", "연세대(미래)", "학생부종합·학생부교과", "의예과"),
    ("11/29(일)", "계명대", "학생부종합 지역", "의예과"),
    ("11/29(일)", "조선대", "학생부종합 면접전형", "의예·치의예·약학"),
    ("11/29(일)", "POSTECH", "일반전형Ⅱ", "해당 전형"),
    ("12/1(화)", "충남대", "학생부종합Ⅱ(지역인재)", "의예과"),
    ("12/1(화)", "원광대", "지역인재종합·지역인재기회균형", "의·치·한의예, 약학·한약학"),
    ("12/2(수)", "충남대", "학생부종합Ⅰ(면접전형)", "간호·의과·수의과대학"),
    ("12/2(수)", "원광대", "학생부종합·지역의사선발", "의·치·한의예, 약학·한약학"),
    ("12/2(수)", "전남대", "고교생활우수자Ⅰ", "의학과·치전원·수의예·약학부"),
    ("12/2(수)", "전남대", "지역의사(진료권)", "의학과"),
    ("12/2~9", "경찰대학", "일반·특별전형", "해당 전형"),
    ("12/3(목)", "충남대", "학생부교과(일반·지역인재)", "국어·수학·화학공학·기술교육과"),
    ("12/4(금)", "충남대", "학생부종합Ⅰ(면접전형)", "사범대학(1개 학과 제외)"),
    ("12/4(금)", "서울대", "지역균형(수의·의과대학 12/5)", "전 모집단위"),
    ("12/5(토)", "가톨릭대", "학교장추천", "약학과·의예과"),
    ("12/5(토)", "인제대", "지역의사", "의예과"),
    ("12/5(토)", "계명대", "학생부교과(면접전형)·지역의사광역", "문예창작학과 외"),
    ("12/5(토)", "한국교원대", "학생부종합우수자(일반)", "초등·불어교육과 외"),
    ("12/5(토)", "부산대", "학생부종합", "치의예과"),
    ("12/5(토)", "부산대", "지역인재·지역의사선발", "간호·약학·의예·치의예"),
    ("12/5(토)", "울산대", "잠재역량", "의예과"),
    ("12/5~6", "홍익대(서울)", "미술우수자", "해당 전형"),
    ("12/6(일)", "경희대", "네오르네상스", "의예·한의예·치의예·약학"),
    ("12/9(수)", "한림대", "학교생활우수자·지역인재·지역의사", "의학과"),
    ("12/14(월)", "아주대", "ACE·지역의사선발", "의학과·약학과"),
    ("12/14~15", "가천대", "가천의약학·교육기회균형", "의예 12/14·약학 12/15"),
]


def header(d, title, sub, chip="2027 수시 · 수능최저"):
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
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if cur and d.textlength(t, font=fnt) > maxw:
            out.append(cur); cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def make_timeline(out):
    BOX, GAP, HEAD = 128, 30, 180
    H = HEAD + (BOX + GAP) * len(TIMELINE) - GAP + 130
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "수능부터 최종 발표까지, 날짜 순서", font=font(42, True), fill="white")
    d.text((48, 90), "표의 면접 54개 중 52개가 성적 통지(12/11) 전이라, 가채점으로 판단해야 합니다.", font=font(23), fill=PALE)
    y = HEAD
    x0, x1 = 40, W - 40
    for i, (when, title, desc, col) in enumerate(TIMELINE):
        d.rounded_rectangle([x0, y, x1, y + BOX], radius=16, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 270, y + BOX], radius=16, fill=col)
        d.rectangle([x0 + 250, y, x0 + 270, y + BOX], fill=col)
        text_fixed(d, (x0 + 24, y + 44), when, font(28, True), "white")
        d.text((x0 + 296, y + 12), title, font=font(30, True), fill=NAVY)
        f_d = font(21)
        for j, ln in enumerate(wrap_words(d, desc, f_d, x1 - x0 - 330)[:2]):
            text_fixed(d, (x0 + 296, y + 58 + 27 * j), ln, f_d, TEXT)
        y += BOX + GAP
    text_fixed(d, (40, y + 4), "출처: 한국교육과정평가원 「2027학년도 수능 실시요강」·「시행기본계획」, 한국대학교육협의회 수시 일정. 면접일은 이 글의 표.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("timeline", out, img.size)


def make_parts(out):
    BOX, GAP, HEAD = 132, 22, 300
    H = HEAD + (BOX + GAP) * len(PARTS) - GAP + 300
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((48, 28), "수능최저 문장, 5조각으로 읽기", font=font(42, True), fill="white")
    d.text((48, 90), "아래 문장은 여러 대학 요강 형태를 본떠 이 글에서 만든 예시입니다.", font=font(23), fill=PALE)
    d.rounded_rectangle([40, 172, W - 40, 272], radius=14, fill="white", outline=CORAL, width=3)
    ex = "국어·수학(미적분/기하)·영어·과탐(2과목 평균, 소수점 절사) 중 수학 포함 3개 영역 등급 합 5 이내 + 한국사 4등급 이내"
    for j, ln in enumerate(wrap_words(d, ex, font(24, True), W - 140)[:2]):
        text_fixed(d, (66, 188 + 36 * j), ln, font(24, True), NAVY_D)
    y = HEAD
    for num, title, piece, desc in PARTS:
        d.rounded_rectangle([40, y, W - 40, y + BOX], radius=14, fill="white", outline=LINE, width=2)
        d.ellipse([60, y + 30, 120, y + 90], fill=NAVY)
        d.text((90 - d.textlength(num, font=font(34, True)) / 2, y + 36), num, font=font(34, True), fill=ACCENT)
        d.text((146, y + 14), title, font=font(28, True), fill=NAVY)
        tw = d.textlength(title, font=font(28, True))
        fp = font(22, True)
        pw = d.textlength(piece, font=fp)
        d.rounded_rectangle([146 + tw + 18, y + 14, 146 + tw + 18 + pw + 28, y + 52], radius=12, fill=PALE)
        d.text((146 + tw + 32, y + 19), piece, font=fp, fill=NAVY_D)
        for j, ln in enumerate(wrap_words(d, desc, font(21), W - 230)[:2]):
            text_fixed(d, (146, y + 66 + 27 * j), ln, font(21), TEXT)
        y += BOX + GAP
    # 계산 예시
    y += 10
    d.rounded_rectangle([40, y, W - 40, y + 200], radius=14, fill="#fff7e0", outline=ACCENT, width=2)
    d.text((66, y + 16), "계산 예시 (가상의 가채점 결과)", font=font(26, True), fill=NAVY_D)
    lines = ["국어 2 · 수학(미적분) 2 · 영어 1 · 과탐 2과목 2와 3 · 한국사 3",
             "과탐 평균 2.5 → 소수점 절사 2   ·   수학 포함 가장 좋은 3개: 영어 1 + 수학 2 + 국어 2 = 5",
             "합 5 이내 충족 · 한국사 3등급(4등급 이내) 충족 → 이 예시는 최저 충족"]
    for j, ln in enumerate(lines):
        text_fixed(d, (66, y + 62 + 40 * j), ln, font(22), TEXT)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("parts", out, img.size)


def make_table(out, rows, title, sub):
    RH = 64
    COLS = [(44, 190), (250, 190), (450, 370), (830, 330)]
    n = len(rows)
    H = 200 + 58 + RH * n + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, title, sub)
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    for (x, _), lab in zip(COLS, ["면접일", "대학", "전형", "최저 적용 모집단위"]):
        d.text((x, y + 17), lab, font=font(22, True), fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    prev = None
    for k, (day, univ, track, unit) in enumerate(rows):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        if day != prev:
            text_fixed(d, (COLS[0][0], y + 17), day, font(24, True), NAVY)
        prev = day
        for (x, w), val, f, col in ((COLS[1], univ, font(24, True), TEXT), (COLS[2], track, font(20), GRAY), (COLS[3], unit, font(21, True), CORAL)):
            t = val
            while d.textlength(t, font=f) > w - 10 and len(t) > 2:
                t = t[:-2] + "…"
            text_fixed(d, (x, y + 19), t, f, col)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 모집요강. 최저 기준(영역·합·한국사)은 모집단위마다 다르니 블로그 본문 링크의 수능최저 모아보기에서 확인하세요.", font(19), GRAY)
    text_fixed(d, (40, y + 30), "수능 전에 면접을 보는 전형과 최저가 없는 전형은 넣지 않았습니다. 같은 대학도 전형·모집단위마다 면접일이 다릅니다.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size, n)


def jobs_minimum():
    make_thumb(HERE / "thumb-minimum.png", "수능최저", line2="가채점 확인법", line3="수능 뒤 면접 54개 전형", chip="2027 수시 수능최저")
    make_timeline(HERE / "minimum-timeline.png")
    make_parts(HERE / "minimum-parts.png")
    make_table(HERE / "minimum-table-1.png", R1, "수능 뒤 면접 + 수능최저 ①", f"11/21 ~ 11/28 · {len(R1)}개")
    make_table(HERE / "minimum-table-2.png", R2, "수능 뒤 면접 + 수능최저 ②", f"11/28 ~ 12/15 · {len(R2)}개")
    make_capture(HERE / "pnu-2027-minimum.png", pdf("부산대학교"), 61, "학생부종합(학생부종합전형, 지역인재전형", ("after", "상기 외 모집단위는 수능최저학력기준을 적용하지 않음"),
                 "부산대학교", "2027학년도 수시모집요강 58쪽(PDF 61쪽)", "학생부종합 수능최저: 전형·모집단위마다 영역 수와 합이 다릅니다",
                 start_pad=4, end_pad=10)


if __name__ == "__main__":
    jobs_minimum()
