# 수시 면접 당일 준비물·입실·휴대폰·복장 규정 총정리 블로그 글 이미지. python jobs_dayof.py
# 규정은 site/content/rich/univ/<code>.json 의 dayof(각 대학 2027학년도 수시모집요강에서 확인, 출처 쪽수는 dayof.source)에서 옮겼다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, make_capture, pdf, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

FLOW = [
    ("1", "전날", "개인별 시간·장소 확인", "입학처 공지에서 내 면접 시각·고사장·입실 마감을 확인하고, 수험표와 실물 신분증을 가방에 넣어 둡니다.", NAVY),
    ("2", "도착·입실", "입실 마감 전", "입실 마감 뒤에는 응시할 수 없다고 적은 대학이 있습니다. 교통체증 같은 개인 사유 지각을 인정하지 않는 대학도 있습니다.", BLUE),
    ("3", "대기실", "본인 확인 · 가번호", "수험표·신분증으로 본인 확인을 하고, 가번호를 받는 대학도 있습니다. 휴대폰·스마트워치는 끄고 제출하거나, 아예 가져올 수 없는 대학도 있습니다.", CORAL),
    ("4", "면접실", "블라인드 면접", "이름·수험번호·출신 고교·부모 직업을 말하지 않습니다. 교복·교표·명찰처럼 학교가 드러나는 것은 입거나 달지 않습니다.", NAVY_D),
    ("5", "퇴실", "안내에 따라 귀가", "면접이 끝나면 대기실로 돌아가지 않고 바로 퇴실하는 대학이 있습니다. 진행요원 안내를 따릅니다.", GRAY),
]

# 신분증: (대학, 모바일 신분증, 그 밖에)
ID_ROWS = [
    ("가톨릭대", "불인정", "사진이 함께 출력된 수험표"),
    ("한양대", "불인정", ""),
    ("서울시립대", "불인정", "2단계 면접평가용 수험표"),
    ("원광대", "불인정", "성명·생년월일·사진 필수"),
    ("청주대", "불인정", "신분증 없으면 응시 불가"),
    ("경찰대학", "불인정", "신분증 원본 미소지 시 응시 불가"),
    ("연세대(미래)", "불인정", "응시표 A4 단면 출력, 기재 금지"),
    ("선문대", "모바일 운전면허증 불가", "면접 공통, 요강에 적힌 신분증만 인정"),
    ("경남대", "인정", ""),
    ("상명대", "인정", "신분증 촬영 이미지 불인정"),
    ("순천향대", "인정", "신분증 촬영 이미지 불인정"),
    ("한국교원대", "인정(주민등록증·운전면허증)", ""),
]

# 꼭 알아 둘 규정: (대학, 규정)
RULES = [
    ("고려대", "교복·교표 등 출신고교를 드러내는 복장 착용 시 불합격"),
    ("가톨릭대", "지각자는 응시 불가·불합격, 개인별 일시·장소는 고사 3일 전 공지"),
    ("한국교원대", "9:00·13:00 뒤 지각은 감점·불합격 가능, 9:20·13:20 뒤 입실 불가"),
    ("경희대", "시험 시작 30분 전까지 입실 완료, 금속탐지기 확인 절차 가능"),
    ("중앙대", "다른 대학과 시간이 겹치면 면접시간 조정 신청 가능(일자 변경 불가)"),
    ("KAIST", "전자기기는 전원 끄고 감독관 제출, 면접 후 일괄 퇴실 때 반환"),
    ("부산대", "휴대전화·스마트워치·블루투스 이어폰·전자담배 소지 불가"),
    ("광운대", "고사실에 모든 전자기기와 귀마개 지참 불가"),
    ("총신대", "수험표를 면접 때 가슴에 부착"),
    ("서울교대", "면접 당일 면접장 건물 내 보호자 출입 통제"),
    ("차의과대", "대기 중 다른 수험생과 면접 정보 교환 시 즉시 퇴실"),
    ("대진대", "개인정보를 고의·반복해 말하면 감점·0점"),
    ("경기대", "공정성 강화를 위해 면접 과정 녹화·녹음·보존"),
]


def wrap_words(d, text, fnt, maxw):
    """띄어쓰기 단위로 줄바꿈(낱말 중간에서 끊지 않는다)."""
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


def header(d, title, sub, chip="2027 수시 · 면접 당일"):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(46, True), fill="white")
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    return HEAD


def make_flow(out):
    BOX, GAP, HEAD = 150, 40, 180
    H = HEAD + (BOX + GAP) * len(FLOW) - GAP + 140
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((48, 28), "면접 당일, 이 순서로 진행됩니다", font=font(42, True), fill="white")
    d.text((48, 90), "여러 대학 모집요강의 면접 유의사항을 순서대로 묶었습니다. 세부 절차는 대학마다 다릅니다.", font=font(23), fill=PALE)
    y = HEAD
    x0, x1 = 40, W - 40
    for i, (num, title, when, desc, col) in enumerate(FLOW):
        d.rounded_rectangle([x0, y, x1, y + BOX], radius=16, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([x0, y, x0 + 260, y + BOX], radius=16, fill=col)
        d.rectangle([x0 + 240, y, x0 + 260, y + BOX], fill=col)
        d.text((x0 + 24, y + 10), num, font=font(56, True), fill=ACCENT)
        text_fixed(d, (x0 + 24, y + 100), when, font(21, True), "white")
        d.text((x0 + 286, y + 14), title, font=font(32, True), fill=NAVY)
        f_d = font(21)
        for j, ln in enumerate(wrap_words(d, desc, f_d, x1 - x0 - 320)[:3]):
            text_fixed(d, (x0 + 286, y + 62 + 27 * j), ln, f_d, TEXT)
        if i < len(FLOW) - 1:
            cx = x0 + 130
            d.polygon([(cx - 18, y + BOX + 6), (cx + 18, y + BOX + 6), (cx, y + BOX + GAP - 6)], fill=GRAY)
        y += BOX + GAP
    y += 4
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강 면접 유의사항. 개인별 시간·장소는 입학처 공지를 따릅니다.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("flow", out, img.size)


def make_rows(out, rows, title, sub, heads, colx, note):
    RH = 72
    n = len(rows)
    H = 200 + 58 + RH * n + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, title, sub)
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    for x, lab in zip(colx, heads):
        d.text((x, y + 17), lab, font=font(22, True), fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    for k, r in enumerate(rows):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        d.text((colx[0], y + 18), r[0], font=font(27, True), fill=TEXT)
        for j, val in enumerate(r[1:], start=1):
            if not val:
                continue
            last = j == len(r) - 1
            maxw = (W - 50 - colx[j]) if last else (colx[j + 1] - colx[j] - 16)
            if len(r) == 2:          # 규정 표: 설명 한 칸
                f, col = font(22), TEXT
            elif not last:           # 신분증 표: 인정/불인정 칸
                f, col = font(22, True), (CORAL if val.startswith("불인정") or "불가" in val else BLUE)
            else:                    # 신분증 표: 함께 볼 것
                f, col = font(21), GRAY
            t = val
            while d.textlength(t, font=f) > maxw and len(t) > 2:
                t = t[:-2] + "…"
            text_fixed(d, (colx[j], y + 22), t, f, col)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 30
    for j, ln in enumerate(note):
        text_fixed(d, (40, y + 30 * j), ln, font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("rows", out, img.size, n)


def jobs_dayof():
    make_thumb(HERE / "thumb-dayof.png", "면접 당일", line2="준비물·입실·복장", line3="대학별 규정 비교", chip="2027 수시 면접")
    make_flow(HERE / "dayof-flow.png")
    make_rows(HERE / "dayof-table-id.png", ID_ROWS, "신분증, 모바일로 될까?", "모집요강에 적힌 대학만",
              ["대학", "모바일 신분증", "함께 볼 것"], [44, 300, 690],
              ["출처: 각 대학 2027학년도 수시모집요강 면접 유의사항. 표에 없는 대학은 실물 신분증을 챙기는 것이 안전합니다.",
               "학생증은 사진·생년월일, 학교장 직인 등 조건을 붙이는 대학이 있습니다. 지원 대학 요강을 확인하세요."])
    make_rows(HERE / "dayof-table-rules.png", RULES, "놓치기 쉬운 면접 당일 규정", f"{len(RULES)}개 대학",
              ["대학", "모집요강 규정"], [44, 250],
              ["출처(2027학년도 수시모집요강, 인쇄 쪽): 고려대 27 · 가톨릭대 66 · 한국교원대 34 · 경희대 21·123 · 중앙대 27 · KAIST 59 · 부산대 21",
               "광운대 53 · 총신대 28 · 서울교대 7 · 차의과대 32 · 대진대 50 · 경기대 43. 규정은 바뀔 수 있으니 입학처 공지를 다시 확인하세요."])
    make_capture(HERE / "knue-2027-dayof-late.png", pdf("한국교원대학교"), 38, "면접 관련 지원자 유의사항", ("after", "감점 등 불이익을 받을 수 있음"),
                 "한국교원대학교", "2027학년도 수시모집요강 34쪽(PDF 38쪽)", "입실 마감 뒤 지각은 감점·불합격 가능, 면접 시작 뒤에는 입실 불가",
                 start_pad=4, end_pad=0)


if __name__ == "__main__":
    jobs_dayof()
