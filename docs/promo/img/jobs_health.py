# 보건계열 면접 질문 총정리(naver-89) 블로그 글 이미지. python jobs_health.py
# 표의 질문·답변 방향은 각 학과 블로그 원고(docs/promo/naver-*-v2.md)의 질문 문장과 "답변 구조"를 줄인 것이다.
#   간호 naver-36 Q1 · 방사선 naver-17 Q2 · 임상병리 naver-85 Q2 · 응급구조 naver-15 Q2
#   치위생 naver-14 Q1 · 작업치료 naver-16 Q1 · 물리치료 naver-09 Q2 · 식품영양 naver-24 Q2
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, font, text_fixed, wrap_chars, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL)

W = 1200

# (학과, 근거 원고, 대표 질문, 답변 방향)
ROWS = [
    ("간호학과", "사이트 질문 1",
     "간호사가 되고 싶은 이유는 무엇인가요? 간호사의 역할을 어떻게 이해하나요?",
     "계기 경험 → 그때 본 간호사의 역할(관찰·판단·보고·교육) → 확인해 본 행동 → 지원"),
    ("방사선학과", "학과 글 질문 2",
     "방사선은 위험하지 않나요? 본인과 환자를 어떻게 보호하나요?",
     "시간·거리·차폐 원칙 → 필요한 최소 선량 → 재촬영 줄이기 → 개인 선량계"),
    ("임상병리학과", "학과 글 질문 2",
     "작은 실수가 큰 결과를 낳는 일입니다. 정확성을 지킨 경험이 있나요?",
     "정확성이 필요했던 상황 → 내가 쓴 방법(이중 확인·기록) → 결과 → 검체 검사와 연결"),
    ("응급구조학과", "학과 글 질문 2",
     "심폐소생술 순서를 설명해 보세요. 직접 해 본 적이 있나요?",
     "반응 확인 → 신고·자동심장충격기 요청 → 호흡 확인 → 가슴압박 30회(분당 100~120회, 성인 깊이 약 5cm) → 인공호흡 2회"),
    ("치위생학과", "학과 글 질문 1",
     "치과위생사가 되고 싶은 이유는? 치과위생사와 간호조무사는 어떻게 다른가요?",
     "스케일링·불소도포·구강보건교육을 직접 하는 국가면허 전문가라는 차이를 한 문장으로"),
    ("작업치료학과", "학과 글 질문 1",
     "작업치료사가 되고 싶은 이유는? 물리치료와 작업치료는 어떻게 다른가요?",
     "물리치료 = 움직임·관절·근력, 작업치료 = 일상생활 동작·손 기능·인지·감각"),
    ("물리치료학과", "학과 글 질문 2",
     "재활은 오래 걸리고 환자가 포기하기 쉽습니다. 포기하려는 환자에게 어떻게 동기를 주겠습니까?",
     "포기하려는 이유 듣기 → 작은 목표·측정·기록으로 변화가 보이게 → 치료사의 역할"),
    ("식품영양학과", "학과 글 질문 2",
     "유행하는 다이어트나 건강 정보를 어떻게 판단하나요?",
     "출처가 누구인가 · 사람 대상 연구인가 · 나에게 해당하는가 → 맞는 부분과 과장된 부분"),
]


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
    f_q = font(23, True)
    f_a = font(21)
    C1, C2, C3 = 44, 262, 742          # 학과 · 대표 질문 · 답변 방향
    WQ, WA = C3 - C2 - 30, W - 44 - C3
    rows = []
    for dept, src, q, a in ROWS:
        ql = wrap_words(tmp, q, f_q, WQ)
        al = wrap_words(tmp, a, f_a, WA)
        h = max(34 * len(ql), 31 * len(al), 64) + 34
        rows.append((dept, src, ql, al, h))
    HEAD = 210
    H = HEAD + 58 + sum(r[4] for r in rows) + 14 + 150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    chip = "2027 수시 면접"
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 92), "보건계열 학과별 면접 대표 질문", font=font(46, True), fill="white")
    sub = "8개 학과 · 학과마다 질문 1개"
    d.text((W - 40 - d.textlength(sub, font=font(23)), 116), sub, font=font(23), fill=PALE)
    y = HEAD
    body_h = 58 + sum(r[4] for r in rows)
    d.rounded_rectangle([24, y, W - 24, y + body_h + 14], radius=14, fill="white", outline=LINE, width=2)
    fh = font(22, True)
    for x, lab in [(C1, "학과"), (C2, "대표 질문"), (C3, "답변 방향(학과 글의 답변 구조)")]:
        d.text((x, y + 17), lab, font=fh, fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    for k, (dept, src, ql, al, h) in enumerate(rows):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + h], fill="#f7f9fc")
        d.text((C1, y + 16), dept, font=font(26, True), fill=NAVY)
        text_fixed(d, (C1, y + 54), src, font(17), GRAY)
        for j, ln in enumerate(ql):
            text_fixed(d, (C2, y + 16 + 34 * j), ln, f_q, TEXT)
        d.rectangle([C3 - 14, y + 18, C3 - 10, y + h - 18], fill=CORAL)
        for j, ln in enumerate(al):
            text_fixed(d, (C3, y + 18 + 31 * j), ln, f_a, TEXT)
        y += h
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 40
    text_fixed(d, (40, y), "질문은 각 학과 글에서 모집요강 평가 항목과 연결해 정리한 예상 질문입니다(대학이 공개한 질문이 아닙니다).", font(19), GRAY)
    text_fixed(d, (40, y + 30), "답변 방향은 학과 글의 '답변 구조'를 줄인 것입니다. 실제 답변은 본인 경험으로 만드세요.", font(19), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("table", out, img.size)


def jobs_health():
    make_thumb(HERE / "thumb-health.png", "보건계열 면접", line2="학과별 핵심 질문", line3="8개 학과 총정리")
    make_table(HERE / "health-table.png")


if __name__ == "__main__":
    jobs_health()
