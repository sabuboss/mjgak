# 전국 교대 수시 면접 총정리(naver-91) 블로그 글 이미지. python jobs_edu.py
# 표의 내용은 검수 끝난 사이트 데이터 site/content/rich/univ/*.json 의
# tracks[].units·method·interview·first·date 문장을 줄인 것이다(쪽수는 각 json 의 source).
#   서울교대(snue)          : 2027학년도 수시모집요강 3·5·7·9~12·14·15·20·21쪽
#   청주교대(cje)           : 모집요강 1·2·8·10·24·25·45쪽
#   전주교대(jnue)          : 모집요강 1·2·5·7·9·28쪽
#   대구교대(dnue)          : 모집요강 1·2·14~17쪽
#   부산교대(bnue)          : 2027학년도 부산대학교 수시모집요강(연제캠퍼스) 82·83·85·97·98쪽
#   진주교대(cue)           : 모집요강 1·2·4·9·10쪽
#   광주교대(gnue)          : 모집요강(HWP) 1·2·3·20~30·35쪽
#   제주대(jejunu)          : 모집요강 1·5·25·31·32쪽
#   경인교대(kgu-gyeongin)  : 모집요강 3·5·7·23·24·26쪽
#   공주교대(gjue)·춘천교대(cnue): summary(면접 없음, 서류 100%)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200
POST, DONE, NONE = "수능 후", "종료", "면접 없음"

# (학교, 전형, 인원·배수, 1단계 발표, 면접일, 태그, 면접 형식, 서류:면접)
ROWS = [
    ("서울교대", "교직인성우수자 · 기회균형Ⅰ·Ⅱ", "150 · 15 · 30명 · 2배수",
     "11/13(금) 10:00", "11/21(토)", POST,
     "복수 면접위원 심층 문답 · 별도 자기소개 없음 · 학생부 기반 60 + 교직 적·인성 40", "50 : 50"),
    ("서울교대", "학교장추천(학생부교과)", "40명 · 2배수",
     "11/13(금) 10:00", "11/21(토)", POST,
     "복수 면접위원 심층 문답 · 교직 적·인성", "80 : 20|(1단계 교과)"),
    ("청주교대", "지역인재 · 특별 5개 전형", "132명 2배수 · 35명 3배수",
     "11/13(금) 10:00", "11/27(금)", POST,
     "개별면접 10분 · 제출서류 참조 질의 · 복수 면접위원", "60 : 40"),
    ("전주교대", "교직적성우수자 · 지역인재선발 · 고른기회", "48 · 114명 300% · 33명 200%",
     "11/13(금) 15:00", "11/27(금)", POST,
     "학생부 기반 면접 · 개인별 8분 이내", "70 : 30"),
    ("대구교대", "학생부종합 9개 전형", "310명 · 2~5배수(참스승 5배수)",
     "11/13(금) 10:00 예정", "11/28(토)", POST,
     "학생부 활용 · 다수 평가위원 종합 평가 · 블라인드", "70 : 30|(700:300점)"),
    ("부산교대", "학생부종합 6개 전형(부산대 연제캠퍼스 요강)", "초등교직적성자 65 · 지역인재Ⅱ 125명 등 · 3배수",
     "11/20(금) 17:00 예정", "11/28(토) 예정", POST,
     "다대다: 3명 내외 한 조 · 면접위원 3인 · 제시문 기반 · 조당 25분 내외", "60 : 40|(실질 80:20)"),
    ("진주교대", "학생부종합 8개 전형", "228명 · 2.5배수",
     "11/13(금) 14:00 예정", "11/28(토)", POST,
     "개별면접 · 면접위원 3인 · 학생부·교직관 질의 · 1인 15분 이내", "70 : 30|(실질|63.6:36.4)"),
    ("광주교대", "대면 면접 6개 전형", "교육감추천 60 · 지역인재 50 · 교육감다문화 10명 2.5배수 · 사회통합·장애인·만학도 27명 4배수",
     "11/13(금) 14:00 예정", "11/28(토)|11:00 예정", POST,
     "대면 개별면접 · 평가위원 2인 · 학생부 기반 · 1인 10분 내외", "70 : 30"),
    ("제주대", "학생부종합(일반학생) 초등교육학부", "1단계 3배수",
     "11/13(금) 10:00", "12/4(금)", POST,
     "다수 면접위원 개별 블라인드 면접 · 15분 내외 질의응답", "70 : 30"),
    ("경인교대", "학교장추천 · 교직적성 · 기회균형", "110 · 226 · 66명 · 일괄합산",
     "없음", "영상 제출|9/21~23", DONE,
     "공개 문항 답변 영상 제출 · Pass/Fail", "70 : 30|(학교장추천|교과 70)"),
    ("광주교대", "비대면: 교직적성우수자 · 농어촌 · 기초/차상위/한부모", "53 · 7 · 10명 · 일괄합산",
     "없음", "영상 업로드|9/29", DONE,
     "공개 문항 답변 영상 제출 · A·B·C·F 평가", "70 : 30"),
    ("공주교대|춘천교대", "학생부종합 전 전형", "177명 · 184명",
     "-", "-", NONE,
     "2027학년도 수시 면접 없음 · 서류평가 100%", "서류 100"),
]

TAGC = {POST: (CORAL, "white"), DONE: ("#9aa3ad", "white"), NONE: (BLUE, "white")}


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
    X = [40, 168, 432, 584, 752, 1040]
    WD = [X[1] - X[0] - 10, X[2] - X[1] - 16, X[3] - X[2] - 14, X[4] - X[3] - 14, X[5] - X[4] - 18, W - 36 - X[5]]
    f_tr = font(21, True)
    f_sm = font(17)
    f_c = font(19)
    f_cb = font(20, True)
    f_r = font(22, True)
    rows = []
    for r in ROWS:
        school, track, units, first, date, tag, fmt, ratio = r
        sl = school.split("|")
        tl = wrap_words(tmp, track, f_tr, WD[1])
        ul = wrap_words(tmp, units, f_sm, WD[1])
        fl = wrap_words(tmp, first, f_cb, WD[2])
        dl = date.split("|")
        ml = wrap_words(tmp, fmt, f_c, WD[4])
        rl = ratio.split("|")
        h_tr = 28 * len(tl) + 24 * len(ul) + 4
        h_d = 28 * len(dl) + 34
        h = max(h_tr, 28 * len(fl), h_d, 27 * len(ml), 34 + 24 * (len(rl) - 1), 30 * len(sl), 56) + 30
        rows.append((school, sl, tl, ul, fl, dl, tag, ml, rl, h))
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
    d.text((40, 90), "전국 교대 면접 한눈에", font=font(46, True), fill="white")
    sub = "면접일 순 · 영상 제출이 끝난 전형은 아래"
    d.text((W - 40 - d.textlength(sub, font=font(23)), 112), sub, font=font(23), fill=PALE)
    y = HEAD
    d.rounded_rectangle([24, y, W - 24, y + body_h + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(20, True)
    for x, lab in zip(X, ["학교", "전형 · 인원 · 배수", "1단계 발표", "면접일", "면접 형식", "서류 : 면접"]):
        d.text((x, y + 18), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    prev = None
    for k, (school, sl, tl, ul, fl, dl, tag, ml, rl, h) in enumerate(rows):
        dim = tag != POST
        if dim:
            d.rectangle([26, y, W - 26, y + h], fill="#eef0f3")
        elif k % 2 == 1:
            d.rectangle([26, y, W - 26, y + h], fill="#f7f9fc")
        main = GRAY if tag == DONE else TEXT
        if school != prev:
            for j, ln in enumerate(sl):
                d.text((X[0], y + 14 + 30 * j), ln, font=font(23, True), fill=GRAY if tag == DONE else NAVY)
        yy = y + 15
        for ln in tl:
            text_fixed(d, (X[1], yy), ln, f_tr, main); yy += 28
        yy += 2
        for ln in ul:
            text_fixed(d, (X[1], yy), ln, f_sm, GRAY); yy += 24
        for j, ln in enumerate(fl):
            text_fixed(d, (X[2], y + 16 + 28 * j), ln, f_cb, main)
        for j, ln in enumerate(dl):
            text_fixed(d, (X[3], y + 16 + 28 * j), ln, f_cb, GRAY if tag == DONE else NAVY)
        bg, fg = TAGC[tag]
        ft = font(16, True)
        tw = d.textlength(tag, font=ft)
        ty = y + 16 + 28 * len(dl) + 4
        d.rounded_rectangle([X[3], ty, X[3] + tw + 18, ty + 24], radius=12, fill=bg)
        d.text((X[3] + 9, ty + 1), tag, font=ft, fill=fg)
        d.rectangle([X[4] - 12, y + 18, X[4] - 9, y + h - 18], fill="#b8bfc8" if dim else CORAL)
        for j, ln in enumerate(ml):
            text_fixed(d, (X[4], y + 16 + 27 * j), ln, f_c, main)
        for j, ln in enumerate(rl):
            fnt = f_r if j == 0 else f_sm
            ry = y + 15 if j == 0 else y + 15 + 34 + 24 * (j - 1)
            text_fixed(d, (X[5], ry), ln, fnt, GRAY if tag == DONE else NAVY)
        y += h
        nxt = rows[k + 1][0] if k + 1 < len(rows) else None
        d.line([40, y, W - 40, y], fill=LINE if nxt != school else "#edf0f4", width=2 if nxt != school else 1)
        prev = school
    y += 40
    text_fixed(d, (40, y), "출처: 각 대학 2027학년도 수시모집요강(부산교대는 「2027학년도 부산대학교 수시모집요강(연제캠퍼스)」).", font(19), GRAY)
    text_fixed(d, (40, y + 30), "서류 : 면접은 최종(2단계·일괄합산) 반영 비율. 면접 시간·장소는 1단계 발표 때 입학처 공지로 다시 확인하세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size)


def jobs_edu():
    make_thumb(HERE / "thumb-edu-gyodae.png", "전국 교대", line2="면접 방식·일정", line3="10개 교대 한눈에")
    make_table(HERE / "edu-table.png")


if __name__ == "__main__":
    jobs_edu()
