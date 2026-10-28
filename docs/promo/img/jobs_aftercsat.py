# 수능 직후 면접 준비 날짜별 할 일(naver-92) 블로그 글 이미지. python jobs_aftercsat.py
# 표의 날짜·규정은 검수 끝난 사이트 데이터만 썼다.
#   면접일·1단계 발표: site/content/rich/univ/*.json 의 tracks[].date·first
#     (inu, knu, snue, hanyang-erica, eulji, ewha, duksung, sejong, sungshin, hufs, inha, kookmin, hanyang, ajou)
#   정답 확정 12/1(화) 17시·성적 통지 12/11(금): site/site.json milestones, templates/suneung.html
#   한양대 공과대학 제시문 기출 공개: hanyang.json notes / 성신여대 대기실 규정: sungshin.json notes
# 할 일의 순서와 나누기는 이 글의 제안이다(대학이 정한 기준이 아님).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

# (날짜, 요일 꼬리표, 공통 항목 또는 None, 21일 면접 (제목, 항목), 22일 면접 (제목, 항목))
ROWS = [
    ("11/19", "목 · 수능 저녁",
     ["가채점(수험표 뒷면 가채점표)으로 등급 가늠", "지원 전형에 수능최저가 있는지 확인",
      "면접 공지 다시 열기: 시간·장소·준비물", "면접 연습은 쉬고 평소 시각에 잠자리"],
     None, None),
    ("11/20", "금",
     None,
     ("면접 전날", ["준비물 챙기기(1단계 합격 공지·대학 안내대로)", "장소·이동 시간 확인, 출발 시각 정하기",
                   "모의면접 1회(지원 대학 면접 시간에 맞춰)", "이름·학교·부모 직업 언급 걸러 내기",
                   "가방 싸 두고 평소 시각에 잠자리"]),
     ("준비 1일차", ["학생부 처음부터 다시 읽기", "예상 질문 목록 점검, 1분 답변 녹음",
                    "제시문 면접이면 공개 기출 1개 풀기", "면접 공지·장소 확인"])),
    ("11/21", "토",
     None,
     ("면접 당일", ["입실 시각에서 거꾸로 세어 출발", "대기실 안내 따르기(전자기기 등)",
                   "끝나면 받은 질문을 짧게 메모"]),
     ("면접 전날", ["모의면접 1회", "준비물·장소·입실 시각 다시 확인", "가방 싸 두고 평소 시각에 잠자리"])),
    ("11/22", "일",
     None,
     ("다음 일정 확인", ["11/28·29 면접이 있으면 다시 준비", "정답 확정 12/1(화) 17시"]),
     ("면접 당일", ["입실 시각에서 거꾸로 세어 출발", "끝나면 다음 일정 확인(성적 통지 12/11)"])),
]


def box(d, x, y):
    d.rounded_rectangle([x, y, x + 24, y + 24], radius=5, outline=NAVY, width=3, fill="white")


def items_h(d, items, maxw, f):
    n = 0
    for it in items:
        n += len(wrap_chars(d, it, f, maxw))
    return n * 30 + len(items) * 10


def draw_items(d, x, y, items, maxw, f):
    for it in items:
        lines = wrap_chars(d, it, f, maxw)
        box(d, x, y + 5)
        for j, ln in enumerate(lines):
            text_fixed(d, (x + 36, y + 30 * j), ln, f, TEXT)
        y += 30 * len(lines) + 10
    return y


def make_checklist(out):
    tmp = Image.new("RGB", (W, 4000), BG)
    d = ImageDraw.Draw(tmp)
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 10], fill=NAVY)
    chip = "2027 수시 · 수능 11/19(목) 직후"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), "수능 저녁부터 면접까지 날짜별 할 일", font=font(46, True), fill="white")
    text_fixed(d, (40, 152), "11월 21일(토) 면접 / 11월 22일(일) 면접, 내 날짜 칸만 따라가세요", font(23), PALE)

    X0, XD, XA, XB, X1 = 32, 44, 236, 716, W - 32
    WA, WB = XB - XA - 60, X1 - XB - 56
    f = font(21)
    y = HEAD + 18
    # 열 머리
    d.rounded_rectangle([XA - 8, y, XB - 20, y + 50], radius=12, fill=CORAL)
    d.text((XA + 10, y + 9), "11/21(토) 면접", font=font(26, True), fill="white")
    d.rounded_rectangle([XB - 8, y, X1, y + 50], radius=12, fill=BLUE)
    d.text((XB + 10, y + 9), "11/22(일) 면접", font=font(26, True), fill="white")
    y += 66
    for date, tag, common, a, b in ROWS:
        if common:
            h = max(64 + items_h(d, common[:2], WA, f), 64 + items_h(d, common[2:], WB, f)) + 8
        else:
            h = max(64 + items_h(d, a[1], WA, f), 64 + items_h(d, b[1], WB, f)) + 8
        h = max(h, 120)
        d.rounded_rectangle([X0, y, X1, y + h], radius=14, fill="white", outline=LINE, width=2)
        # 날짜 칸
        d.rounded_rectangle([X0, y, XA - 24, y + h], radius=14, fill=NAVY if common else PALE)
        d.rectangle([XA - 44, y, XA - 24, y + h], fill=NAVY if common else PALE)
        dc = "white" if common else NAVY_D
        d.text((XD, y + 18), date, font=font(40, True), fill=dc)
        for j, ln in enumerate(wrap_chars(d, tag, font(21, True), XA - XD - 34)):
            text_fixed(d, (XD, y + 70 + 28 * j), ln, font(21, True), dc)
        if common:
            d.text((XA, y + 16), "두 경우 모두", font=font(25, True), fill=NAVY)
            draw_items(d, XA, y + 58, common[:2], WA, f)
            draw_items(d, XB, y + 58, common[2:], WB, f)
        else:
            for (title, its), xx, ww, col in ((a, XA, WA, CORAL), (b, XB, WB, BLUE)):
                d.text((xx, y + 16), title, font=font(25, True), fill=col)
                draw_items(d, xx, y + 58, its, ww, f)
            d.line([XB - 20, y + 16, XB - 20, y + h - 16], fill="#e3e7ed", width=2)
        y += h + 16
    y += 10
    text_fixed(d, (40, y), "면접일·공지는 면접각 대학 페이지(각 대학 2027학년도 수시모집요강), 정답 확정·성적 통지일은 평가원 실시요강 기준.", font(19), GRAY)
    text_fixed(d, (40, y + 28), "할 일의 순서는 이 글의 제안입니다. 준비물·복장·입실 시각은 지원 대학 입학처 공지로 확인하세요.", font(19), GRAY)
    H = y + 28 + 100
    img = tmp.crop((0, 0, W, H))
    d = ImageDraw.Draw(img)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("checklist", out, img.size)


def jobs_aftercsat():
    make_thumb(HERE / "thumb-aftercsat.png", "수능 다음 날", line2="면접 전날까지", line3="날짜별 할 일", chip="11월 21·22일 면접")
    make_checklist(HERE / "aftercsat-checklist.png")


if __name__ == "__main__":
    jobs_aftercsat()
