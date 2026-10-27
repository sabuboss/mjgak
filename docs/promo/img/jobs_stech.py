# 과학기술원 면접 총정리(naver-90) 블로그 글 이미지. python jobs_stech.py
# 표의 내용은 검수 끝난 사이트 데이터 site/content/rich/univ/{unist,kaist,postech,dgist,kentech,gist}.json 의
# tracks[].units·method·interview·first·date 문장을 줄인 것이다(쪽수는 각 json 의 source).
#   UNIST  : 모집요강 30·32·46~48쪽 + 입학처 면접평가 사전 안내(2026.10.23)
#   KAIST  : 모집요강 28·30·59쪽
#   POSTECH: 모집요강 7~9·12쪽
#   DGIST  : 모집요강 48·58·59쪽
#   KENTECH: 모집요강 54·55·57·59쪽
#   GIST   : 입학전형 안내 30~33쪽
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200
PRE, POST, DONE = "수능 전", "수능 후", "종료"

# (학교, 전형, 인원·배수, 1단계 발표, 면접일, 수능 전/후, 면접 형식, 서류:면접)
ROWS = [
    ("UNIST", "탐구우수전형", "70명 내외 · 3배수 내외",
     "11/4(수)", "11/7(토)", PRE,
     "제출서류 기반 질의응답 · 평가위원 2명 · 20분 내외(준비 포함)", "50 : 50"),
    ("UNIST", "그릿인재전형(신설)", "10명 내외 · 3배수 내외",
     "11/4(수)", "11/8(일)", PRE,
     "개인: 포트폴리오 발표 5~10분 + 질의응답 · 단체: 5명 내외 팀 융합 프로젝트 1~2시간", "30 : 70"),
    ("KAIST", "일반 · 고른기회 · 반도체시스템인재", "380 · 60 · 40명 내외 · 2.5배수(고른기회 2배수)",
     "11/11(수) 10:00", "11/26(목)", POST,
     "면접준비실 60분(제시문) → 학업역량 15분(수학·과학·영어) → 적합성 15분", "40 : 60"),
    ("KAIST", "특기자전형", "30명 내외 · 2배수 내외",
     "11/11(수) 10:00", "11/26(목)", POST,
     "준비실 20분 → 특기역량 20분(본인 발표 5분, 영어 포함) → 적합성 15분", "40 : 60"),
    ("POSTECH", "일반전형Ⅰ", "220명 · 3배수",
     "11/20(금) 10:00", "11/28(토)", POST,
     "개인면접 + 개인과제 + 그룹활동(오전~오후)", "50 : 50"),
    ("POSTECH", "일반전형Ⅱ", "70명 · 3배수 · 수능 최저 있음",
     "11/20(금) 10:00", "11/29(일)", POST,
     "개인면접(서류평가 기반 질의응답)", "67 : 33"),
    ("POSTECH", "반도체공학인재(정원 외)", "40명 · 3배수",
     "11/20(금) 10:00", "11/29(일)", POST,
     "통합면접(개인면접 + 제시문면접)", "50 : 50"),
    ("DGIST", "실기/실적 과학인재전형", "기초학부 15명 내외 · 5배수 내외",
     "요강 일정표에 따로 없음", "11/25(수)~|27(금) 중(예정)", POST,
     "다수 평가자 대면면접 · 과학활동 우수성", "50 : 50"),
    ("KENTECH", "학생부종합 일반 · 고른기회", "90명 · 10명(정원 외) · 5배수 내외",
     "11/20(금) 18:00", "11/30(월)", POST,
     "창의성 면접: 준비 30분 → 문답 15분(문제풀이식 구술고사 아님)", "50 : 50"),
    ("GIST", "일반 · 학교장추천 · 고른기회 · 특기자", "2027학년도 면접은 끝남",
     "10/15(목)", "10/22(목)~|23(금)", DONE,
     "전공수학능력(특기자는 특기역량) + 내적역량 구술면접 · 15분 내외", "50 : 50|(특기자는|종합평가)"),
]

TAGC = {PRE: (BLUE, "white"), POST: (CORAL, "white"), DONE: ("#9aa3ad", "white")}


def wrap_words(d, text, fnt, maxw):
    """띄어쓰기 단위로 줄을 나눈다. 한 단어가 한 줄보다 길 때만 글자 단위로 자른다."""
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w) if cur else w
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        elif not cur:
            parts = wrap_chars(d, w, fnt, maxw)
            out.extend(parts[:-1]); cur = parts[-1]
        else:
            out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out


def make_table(out):
    tmp = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    # 열: 학교 · 전형(인원·배수) · 1단계 발표 · 면접일 · 면접 형식 · 서류:면접
    X = [40, 168, 432, 584, 752, 1060]
    WD = [X[1] - X[0] - 10, X[2] - X[1] - 16, X[3] - X[2] - 14, X[4] - X[3] - 14, X[5] - X[4] - 18, W - 36 - X[5]]
    f_tr = font(21, True)
    f_sm = font(17)
    f_c = font(19)
    f_cb = font(20, True)
    f_r = font(22, True)
    rows = []
    for r in ROWS:
        school, track, units, first, date, tag, fmt, ratio = r
        tl = wrap_words(tmp, track, f_tr, WD[1])
        ul = wrap_words(tmp, units, f_sm, WD[1])
        fl = wrap_words(tmp, first, f_cb, WD[2])
        dl = date.split("|")
        ml = wrap_words(tmp, fmt, f_c, WD[4])
        rl = ratio.split("|")
        h_tr = 28 * len(tl) + 24 * len(ul) + 4
        h_d = 28 * len(dl) + 34
        h = max(h_tr, 28 * len(fl), h_d, 27 * len(ml), 30 * len(rl), 56) + 30
        rows.append((school, tl, ul, fl, dl, tag, ml, rl, h))
    HEAD = 200
    body_h = 58 + sum(r[-1] for r in rows)
    H = HEAD + body_h + 14 + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    chip = "2027 수시 · 수능 11/19(목)"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), "과학기술원·과학기술 특성화대 면접 한눈에", font=font(46, True), fill="white")
    sub = "면접 전형 · 면접일 순"
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    y = HEAD
    d.rounded_rectangle([24, y, W - 24, y + body_h + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(20, True)
    for x, lab in zip(X, ["학교", "전형 · 인원 · 배수", "1단계 발표", "면접일", "면접 형식", "서류 : 면접"]):
        d.text((x, y + 18), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    prev = None
    for k, (school, tl, ul, fl, dl, tag, ml, rl, h) in enumerate(rows):
        done = tag == DONE
        if done:
            d.rectangle([26, y, W - 26, y + h], fill="#eef0f3")
        elif k % 2 == 1:
            d.rectangle([26, y, W - 26, y + h], fill="#f7f9fc")
        main = GRAY if done else TEXT
        if school != prev:
            d.text((X[0], y + 14), school, font=font(23 if len(school) > 5 else 25, True), fill=GRAY if done else NAVY)
        yy = y + 15
        for ln in tl:
            text_fixed(d, (X[1], yy), ln, f_tr, main); yy += 28
        yy += 2
        for ln in ul:
            text_fixed(d, (X[1], yy), ln, f_sm, GRAY); yy += 24
        for j, ln in enumerate(fl):
            text_fixed(d, (X[2], y + 16 + 28 * j), ln, f_cb, main)
        for j, ln in enumerate(dl):
            text_fixed(d, (X[3], y + 16 + 28 * j), ln, f_cb, GRAY if done else NAVY)
        bg, fg = TAGC[tag]
        ft = font(16, True)
        tw = d.textlength(tag, font=ft)
        ty = y + 16 + 28 * len(dl) + 4
        d.rounded_rectangle([X[3], ty, X[3] + tw + 18, ty + 24], radius=12, fill=bg)
        d.text((X[3] + 9, ty + 1), tag, font=ft, fill=fg)
        d.rectangle([X[4] - 12, y + 18, X[4] - 9, y + h - 18], fill="#b8bfc8" if done else CORAL)
        for j, ln in enumerate(ml):
            text_fixed(d, (X[4], y + 16 + 27 * j), ln, f_c, main)
        for j, ln in enumerate(rl):
            fnt = f_r if j == 0 else f_sm
            ry = y + 15 if j == 0 else y + 15 + 34 + 24 * (j - 1)
            text_fixed(d, (X[5], ry), ln, fnt, GRAY if done else NAVY)
        y += h
        nxt = rows[k + 1][0] if k + 1 < len(rows) else None
        d.line([40, y, W - 40, y], fill=LINE if nxt != school else "#edf0f4", width=2 if nxt != school else 1)
        prev = school
    y += 40
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 모집요강(GIST는 입학전형 안내). UNIST 면접 시간은 입학처 면접평가 사전 안내(2026.10.23).", font(19), GRAY)
    text_fixed(d, (40, y + 30), "서류 : 면접은 최종(2단계) 반영 비율. 면접 시간·장소는 1단계 발표 때 입학처 공지로 다시 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size)


def jobs_stech():
    make_thumb(HERE / "thumb-stech.png", "과학기술원", line2="면접 방식·일정", line3="KAIST·POSTECH 등")
    make_table(HERE / "stech-table.png")


if __name__ == "__main__":
    jobs_stech()
