# 수시 면접 날짜 겹칠 때 총정리 블로그 글(naver-127) 이미지. python jobs_clash.py
# 날짜는 site/content/rich/univ/*.json 의 tracks[].date 에서 뽑아, 각 대학 2027학년도 수시모집요강 PDF(src/)의 전형일정 쪽에서 다시 확인했다.
# 근거 쪽수는 원고(naver-127-면접날짜겹칠때-v2.md) 작업용 메모 [근거 쪽수]에 있다.
# 표 그리기는 jobs_results.py 의 header()·make_time_table() 을 복사해 고쳤다(칩 안에 모집단위 꼬리말, 여러 날 대학 노란 칸).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf
from PIL import Image, ImageDraw
from promo_style import (HERE, SRC, make_thumb, make_capture, pdf, font, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL)

W = 1200
MULTI = "#fff1c7"   # 다른 날에도 면접이 있는 대학 칩

# (날짜, [(대학, 꼬리말)]) — 꼬리말은 그날 면접 보는 전형·모집단위 요약
D1121 = ("11/21(토)", [
    ("서울교대", ""), ("을지대", "성남캠퍼스"), ("인천대", ""), ("경북대", ""), ("한양대 ERICA", ""),
    ("덕성여대", "모집단위별"), ("이화여대", "모집단위별"), ("인하대", "경영·사범 등"), ("국민대", "자연계"),
    ("세종대", "창의소프트 등"), ("한국외대", "서울캠 모집단위"), ("성신여대", "모집단위별"),
    ("아주대", "첨단융합인재 등"), ("대진대", "학생부우수자 등"), ("총신대", "고른기회 등"),
    ("계명대", "의예과(교과)"), ("울산대", "의예과(교과)"), ("인제대", "의예·약학·간호"), ("영남대", "전공자유선택"),
])
D1122 = ("11/22(일)", [
    ("한양대", "공과대학 등"), ("아주대", "공과·첨단ICT"), ("덕성여대", "모집단위별"), ("이화여대", "모집단위별"),
    ("인하대", "공과·자연·의과 등"), ("국민대", "인문·예체능계"), ("세종대", "인문·자연계열"),
    ("한국외대", "글로벌캠 모집단위"), ("성신여대", "모집단위별"), ("계명대", "의예과(교과 지역)"), ("대진대", "일부 학과(원문 표기 차이)"),
])
D1128 = ("11/28(토)", [
    ("서울대", "수의·의·치의학과"), ("서울여대", ""), ("서울과기대", "학교생활우수자 등"), ("명지대", "자연캠 모집단위"),
    ("숙명여대", "모집단위별"), ("서울시립대", "인문·예체능"), ("성신여대", "모집단위별"), ("아주대", "SW·자연·간호"),
    ("가톨릭대", "의예과(지역균형)"), ("서강대", "특성화고교졸업자"), ("한국공학대", "창의인재"), ("수원대", "11/27~29 중 지정"),
    ("단국대(천안)", "의예·치의예·약학"), ("홍익대(세종)", "미술우수자 등"), ("연세대(미래)", "의예과"), ("강원대", "지역인재(춘천)"),
    ("차의과대", "약학대학"), ("조선대", "모집단위별"), ("전북대", "지역인재"), ("동아대", "사회과학·경영 등"),
    ("울산대", "간호·자율전공 등"), ("계명대", "의예과(종합)"), ("인제대", "의예과"), ("영남대", "의예과"),
    ("목포대", "장애인전형"),
])
D1129 = ("11/29(일)", [
    ("명지대", "인문캠 모집단위"), ("숙명여대", "모집단위별"), ("서울시립대", "자연계열"), ("성신여대", "모집단위별"),
    ("아주대", "경영·인문·사회과학"), ("서울과기대", "기회균형 등"), ("경기대", "디자인학부 등"), ("수원대", "11/27~29 중 지정"),
    ("단국대(천안)", "문예창작·군사학과"), ("홍익대(세종)", "영상·애니 등"), ("조선대", "모집단위별"), ("계명대", "의예과(종합 지역)"),
])
D1205 = ("12/5(토)", [
    ("서울대", "수의·의과대학 등"), ("중앙대", "모집단위별"), ("경희대", "모집단위별"), ("건국대", "이과·공과 등"),
    ("한양대", "의과대학"), ("가톨릭대", "잠재능력우수자 등"), ("단국대(죽전)", "인문계열"), ("홍익대(서울)", "미술우수자 등"),
    ("경기대", "인문·창의공과 등"), ("부산대", ""), ("한국교원대", "오전반·오후반"), ("가천대", "12/5~7 지역균형"),
    ("계명대", "면접전형 등"), ("울산대", "의예과"), ("인제대", "의예과(지역의사)"),
])
D1206 = ("12/6(일)", [
    ("중앙대", "모집단위별"), ("경희대", "모집단위별"), ("건국대", "문과·경영 등"), ("한양대", "사범대학"),
    ("성균관대", "자유전공·의예 등"), ("단국대(죽전)", "자연계열·SW인재"), ("홍익대(서울)", "디자인학부 등"),
    ("경기대", "사회과학 등"), ("가천대", "12/5~7 지역균형"),
])
ALL = [D1121, D1122, D1128, D1129, D1205, D1206]


def base(n):
    """단국대(천안)·홍익대(서울) 처럼 캠퍼스 표시를 떼고 대학 하나로 센다."""
    return n.split("(")[0] if n.startswith(("단국대", "홍익대")) else n


def counts():
    from collections import Counter
    c = Counter()
    for _, rows in ALL:
        for u in {base(n) for n, _ in rows}:
            c[u] += 1
    return c


def header(d, title, sub, chip):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(44, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    return HEAD


def make_clash_table(out, days, title, sub, chip):
    """jobs_results.make_time_table 을 고친 것: 왼쪽 날짜·대학 수 + 오른쪽 대학 칩(이름 + 회색 꼬리말)."""
    LX, CX = 44, 236
    CW = W - CX - 44
    fn, fh = font(23, True), font(18)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    multi = {u for u, k in counts().items() if k > 1}

    def chip_w(n, h):
        w = 16 + tmp.textlength(n, font=fn) + 16
        if h:
            w += tmp.textlength(h, font=fh) + 8
        return w

    def layout(rows):
        lines, cur, x = [], [], 0
        for n, h in rows:
            w = chip_w(n, h)
            if cur and x + w > CW:
                lines.append(cur); cur, x = [], 0
            cur.append((n, h, w)); x += w + 10
        lines.append(cur)
        return lines

    blocks = [(dt, rows, layout(rows)) for dt, rows in days]
    CH, GAP = 46, 10
    body = sum(max(len(ls) * (CH + GAP) - GAP, 84) + 26 for _, _, ls in blocks)
    H = 200 + 20 + body + 20 + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, title, sub, chip)
    d.rounded_rectangle([24, y, W - 24, y + body + 20], radius=14, fill="white", outline=LINE, width=2)
    y += 20
    for k, (dt, rows, ls) in enumerate(blocks):
        h = max(len(ls) * (CH + GAP) - GAP, 84)
        n_univ = len({base(n) for n, _ in rows})
        d.text((LX, y + 2), dt, font=font(32, True), fill=NAVY)
        d.text((LX, y + 46), f"{n_univ}곳", font=font(28, True), fill=CORAL)
        yy = y
        for line in ls:
            x = CX
            for n, hint, w in line:
                fill = MULTI if base(n) in multi else PALE
                d.rounded_rectangle([x, yy, x + w, yy + CH], radius=12, fill=fill)
                d.text((x + 16, yy + 8), n, font=fn, fill=NAVY_D)
                if hint:
                    hx = x + 16 + d.textlength(n, font=fn) + 8
                    text_fixed(d, (hx, yy + 13), hint, fh, GRAY)
                x += w + 10
            yy += CH + GAP
        y += h + 16
        if k < len(blocks) - 1:
            d.line([40, y, W - 40, y], fill="#edf0f4", width=2)
        y += 10
    y += 22
    d.rounded_rectangle([40, y + 2, 64, y + 24], radius=5, fill=MULTI)
    text_fixed(d, (74, y), "노란 칸: 전형·모집단위에 따라 두 표의 다른 날에도 면접이 있는 대학", font(19), GRAY)
    text_fixed(d, (40, y + 32), "출처: 각 대학 2027학년도 수시모집요강 전형일정. 대학 수는 이 글에서 센 값(캠퍼스가 달라도 1곳).", font(19), GRAY)
    text_fixed(d, (40, y + 62), "개인별 면접 시각은 대학이 따로 공지합니다. 내 모집단위 날짜는 모집요강 원문으로 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 46, size=24)
    img.save(out)
    print("table", out, img.size, [(dt, len({base(n) for n, _ in r})) for dt, r in days])


def cap_boxes(out, pdf_path, page, boxes, univ, doc_label, note, dpi=200, gap=18):
    """promo_style.make_capture 와 같은 틀. 글자 층이 없는 이미지 PDF 용: boxes=[(x0, y0, x1, y1) PDF 포인트]를 세로로 이어 붙인다."""
    pg = pymupdf.open(pdf_path)[page - 1]
    shots = []
    for b in boxes:
        pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(*b))
        shots.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    sw = max(s.width for s in shots)
    sh = sum(s.height for s in shots) + gap * (len(shots) - 1)
    shot = Image.new("RGB", (sw, sh), "white")
    yy = 0
    for k, s in enumerate(shots):
        shot.paste(s, (0, yy)); yy += s.height
        if k < len(shots) - 1:
            dd = ImageDraw.Draw(shot)
            dd.line([20, yy + gap // 2, sw - 20, yy + gap // 2], fill=LINE, width=2)
            yy += gap
    Wc = shot.width + 80
    HEAD, FOOT = 104, 92
    img = Image.new("RGB", (Wc, HEAD + shot.height + 40 + FOOT), BG)
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
    print("capture", out, img.size)


def y_of(pdf_path, page, text, idx=0, edge="y0"):
    r = pymupdf.open(pdf_path)[page - 1].search_for(text)[idx]
    return getattr(r, edge)


def jobs_clash():
    c = counts()
    print("대학 수(전체):", len(c), "| 여러 날:", sorted(u for u, k in c.items() if k > 1))
    for a, b in [(D1121, D1122), (D1128, D1129), (D1205, D1206)]:
        print(a[0], b[0], "합집합", len({base(n) for n, _ in a[1]} | {base(n) for n, _ in b[1]}))

    make_thumb(HERE / "thumb-clash.png", "면접 날짜", line2="겹칠 때 총정리",
               line3="시간 조정 되는 곳·안 되는 곳", chip="2027 수시 면접 일정")
    u12 = len({base(n) for n, _ in D1121[1]} | {base(n) for n, _ in D1122[1]})
    make_clash_table(HERE / "clash-table-1.png", [D1121, D1122], "수능 뒤 첫 주말 면접 대학",
                     f"이틀 중 하루라도 {u12}곳", "2027 수시 · 11/21(토)·22(일)")
    u34 = len({base(n) for n, _ in D1128[1]} | {base(n) for n, _ in D1129[1]})
    u56 = len({base(n) for n, _ in D1205[1]} | {base(n) for n, _ in D1206[1]})
    make_clash_table(HERE / "clash-table-2.png", [D1128, D1129, D1205, D1206], "11월 마지막 주말·12월 첫 주말",
                     f"11/28·29 {u34}곳 · 12/5·6 {u56}곳", "2027 수시 · 11/28(토)·29(일) · 12/5(토)·6(일)")

    cau = str(SRC / "cau.pdf")   # 2026-08-05 InDesign 판(인쇄 쪽수 = PDF 쪽수)
    make_capture(HERE / "cau-2027-clash-adjust.png", cau, 27, "2) 모집단위별 면접 일정 및 면접 배수", ("after", "조정 방법 안내"),
                 "중앙대학교", "2027학년도 수시모집요강 27쪽", "다른 대학과 시간이 겹치면 같은 날 안에서 시간 조정 신청(날짜는 불가)",
                 start_pad=8, end_pad=8)
    cuk = pdf("가톨릭대학교")
    y1 = 642   # 비고 칸("…교리문답 실시")이 논술 행까지 이어져, 논술 블록 아래 가로선(y=640)까지 자름
    make_capture(HERE / "cuk-2027-clash-order.png", cuk, 13, "학생부종합(잠재능력우수자면접전형)", y1,
                 "가톨릭대학교", "2027학년도 수시모집요강 11쪽(PDF 13쪽)", "고사 3일 전 시간 공지 · 타 대학 일정 중복으로 인한 순서 변경 불가",
                 start_pad=10)
    inje = pdf("인제대학교")   # 글자 층 없는 이미지 PDF: 좌표로 자른다(110dpi 화면에서 잰 값을 포인트로 바꿈)
    P = 72 / 110
    cap_boxes(HERE / "inje-2027-clash-campus.png", inje, 11,
              [(110 * P, 596 * P, 842 * P, 742 * P), (110 * P, 1142 * P, 842 * P, 1183 * P)],
              "인제대학교", "2027학년도 수시모집요강 11쪽", "응시순서 조정 불가 · 김해-부산 캠퍼스 같은 날 중복면접 불가")


if __name__ == "__main__":
    jobs_clash()
