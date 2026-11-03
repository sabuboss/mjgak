# ChatGPT로 수시 면접 준비하는 법 블로그 글(naver-126) 이미지. python jobs_gpt.py
# 질문 틀 3가지 문구: site/pages/record.md(면접각 '내 생기부로 면접 예상 질문 만들기')를 글자 그대로 옮겼다.
# 지울 것 표: 단국대학교(죽전) 83쪽(PDF 85) · 숭실대학교 57쪽(PDF 62) · 신한대학교 71쪽(PDF 73) 면접 유의사항 + record.md 개인정보 안내.
# 캡처: src/m_숭실대학교.pdf PDF 62쪽(인쇄 57쪽), src/m_건국대학교.pdf 72쪽(인쇄 쪽 = PDF 쪽).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, make_thumb, make_capture, pdf, font, text_fixed, brand,
                         NAVY, NAVY_D, PALE, BG, LINE, TEXT, GRAY, ACCENT, CORAL, BLUE)

W = 1200

# ---------------------------------------------------------------- 질문 틀 (record.md 원문 그대로)
FRAME1 = [
    "나는 [대학 이름] [전형 이름]에 지원한 수험생이야. 이 전형 면접은 [면접 방식: 예) 면접위원 2명, 10분 내외, 학생부 기반 개별면접]이야.",
    "아래는 내 학생부 일부야(개인정보는 지웠어).",
    "",
    "[학생부 문장 붙여 넣기]",
    "",
    "1) 이 문장들에서 면접관이 물을 만한 질문 10개를 만들어 줘.",
    "2) 질문마다 학생부의 어느 문장에서 나왔는지, 왜 묻는지 한 줄로 적어 줘.",
    "3) 꼬리 질문도 질문마다 하나씩 붙여 줘.",
    "4) 답은 만들지 마. 내가 답을 쓰면 결론이 먼저 나왔는지, 근거가 구체적인지만 고쳐 줘.",
]
FRAME2 = [
    ("왜", "이 활동(주제)을 왜 했나요? 계기는 무엇이었나요?"),
    ("어떻게", "구체적으로 무엇을 했고, 어려웠던 점은 어떻게 풀었나요? (자료, 숫자, 방법)"),
    ("그래서", "무엇을 배웠고, 그 뒤 무엇이 달라졌나요? 지원 학과에서 어떻게 이어 가고 싶나요?"),
]
FRAME3 = ["\"그 결과가 틀렸다면?\"", "\"다시 한다면 무엇을 바꾸겠나요?\"", "\"관련 개념을 설명해 보세요.\""]

# ---------------------------------------------------------------- 지울 것 표: (지울 것, 바꿔 쓰기, 근거)
ERASE = [
    ("내 이름", "지우기", "단국대 · 숭실대 · 신한대 블라인드 규정"),
    ("수험번호", "지우기", "단국대 · 숭실대 · 신한대 블라인드 규정"),
    ("학교 이름 · 고교 유형 · 학교 주소", "○○고", "단국대(고교명 · 고교유형 · 고교주소)"),
    ("부모 이름 · 직업 · 직장 · 직위", "지우기", "단국대 등 블라인드 규정"),
    ("가족관계 · 출신 지역", "지우기 / ○○ 지역", "신한대(가족관계 · 출신지역)"),
    ("주민등록번호 · 주소 · 전화번호", "지우기", "면접각 안내(개인정보 보호)"),
    ("선생님 이름", "○○ 선생님", "면접각 안내(개인정보 보호)"),
]


def wrap_words(d, text, fnt, maxw):
    """띄어쓰기 단위로 줄바꿈(낱말 중간에서 끊지 않는다). jobs_dayof.py 에서 복사."""
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


def header(d, title, sub, chip="2027 수시 · ChatGPT 면접 준비"):
    HEAD = 200
    d.rectangle([0, 0, W, HEAD - 24], fill=NAVY)
    fc = font(26, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 40, 26 + 48], radius=24, fill=ACCENT)
    d.text((60, 32), chip, font=fc, fill=NAVY_D)
    d.text((40, 90), title, font=font(44, True), fill="white")
    fs = font(23)
    d.text((W - 40 - d.textlength(sub, font=fs), 112), sub, font=fs, fill=PALE)
    return HEAD


def card_title(d, x, y, num, title):
    d.rounded_rectangle([x, y, x + 96, y + 44], radius=22, fill=CORAL)
    fb = font(24, True)
    d.text((x + 48 - d.textlength(num, font=fb) / 2, y + 6), num, font=fb, fill="white")
    d.text((x + 116, y + 2), title, font=font(30, True), fill=NAVY)


def make_frames(out):
    img = Image.new("RGB", (W, 3000), BG)
    d = ImageDraw.Draw(img)
    y = header(d, "면접각 질문 틀 3가지", "[ ] 부분만 바꿔 쓰세요")
    x0, x1 = 32, W - 32
    # 틀 1
    f1 = font(22)
    lines = []
    for ln in FRAME1:
        if not ln:
            lines.append(("", False)); continue
        for w in wrap_words(d, ln, f1, x1 - x0 - 110):
            lines.append((w, ln.startswith("4)")))
    h1 = 76 + 34 * len(lines) + 40
    d.rounded_rectangle([x0, y, x1, y + h1], radius=16, fill="white", outline=LINE, width=2)
    card_title(d, x0 + 24, y + 20, "틀 1", "ChatGPT에 붙여 넣는 질문 틀")
    by = y + 80
    d.rounded_rectangle([x0 + 24, by, x1 - 24, by + 34 * len(lines) + 20], radius=10, fill="#f7f9fc", outline="#e1e6ee")
    ty = by + 10
    for t, hi in lines:
        if t:
            if hi:
                d.rectangle([x0 + 40, ty + 2, x0 + 48 + d.textlength(t, font=font(22, True)), ty + 32], fill="#fff1c2")
                text_fixed(d, (x0 + 44, ty), t, font(22, True), NAVY_D)
            else:
                col = CORAL if t.startswith("[학생부") else TEXT
                text_fixed(d, (x0 + 44, ty), t, f1, col)
        ty += 34
    y += h1 + 26
    # 틀 2
    f2 = font(22)
    rows = [(lab, wrap_words(d, txt, f2, x1 - x0 - 230)) for lab, txt in FRAME2]
    h2 = 80 + sum(20 + 32 * len(r[1]) for r in rows) + 30
    d.rounded_rectangle([x0, y, x1, y + h2], radius=16, fill="white", outline=LINE, width=2)
    card_title(d, x0 + 24, y + 20, "틀 2", "활동 하나에서 질문 3개 만들기")
    ry = y + 84
    for lab, ls in rows:
        rh = 32 * len(ls) + 8
        d.rounded_rectangle([x0 + 24, ry, x0 + 160, ry + max(rh, 44)], radius=10, fill=PALE)
        fb = font(24, True)
        d.text((x0 + 92 - d.textlength(lab, font=fb) / 2, ry + max(rh, 44) / 2 - 16), lab, font=fb, fill=NAVY)
        for j, t in enumerate(ls):
            text_fixed(d, (x0 + 184, ry + 6 + 32 * j), t, f2, TEXT)
        ry += max(rh, 44) + 20
    y += h2 + 26
    # 틀 3
    h3 = 84 + 3 * 44 + 64
    d.rounded_rectangle([x0, y, x1, y + h3], radius=16, fill="white", outline=LINE, width=2)
    card_title(d, x0 + 24, y + 20, "틀 3", "꼬리 질문 하나 더")
    qy = y + 84
    for q in FRAME3:
        d.ellipse([x0 + 40, qy + 12, x0 + 52, qy + 24], fill=CORAL)
        text_fixed(d, (x0 + 68, qy), q, font(23, True), TEXT)
        qy += 44
    text_fixed(d, (x0 + 40, qy + 8), "학생부에 적혀 있지만 잘 기억나지 않는 활동부터 정리하세요.", font(21), GRAY)
    y += h3 + 22
    text_fixed(d, (40, y), "출처: 면접각 「내 생기부로 면접 예상 질문 만들기」(mjgak.com/record) 문구 그대로.", font(19), GRAY)
    text_fixed(d, (40, y + 28), "학생부 문장은 개인정보를 지운 뒤 붙여 넣고, 질문이 내 학생부에 실제로 있는 내용인지 다시 확인합니다.", font(19), GRAY)
    H = y + 110
    brand(d, W - 230, H - 50, size=24)
    img = img.crop((0, 0, W, H))
    img.save(out)
    print("frames", out, img.size)


def make_erase(out):
    RH = 74
    n = len(ERASE)
    H = 200 + 58 + RH * n + 170
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, "ChatGPT에 붙여 넣기 전에 지울 것", "학생부 문장 · 내가 덧붙이는 설명 모두")
    colx = [48, 470, 720]
    heads = ["지울 것", "바꿔 쓰기", "근거"]
    d.rounded_rectangle([24, y, W - 24, y + 58 + RH * n + 14], radius=14, fill="white", outline=LINE, width=2)
    for x, lab in zip(colx, heads):
        d.text((x, y + 17), lab, font=font(22, True), fill=GRAY)
    d.line([40, y + 56, W - 40, y + 56], fill=LINE, width=2)
    y += 58
    for k, (a, b, c) in enumerate(ERASE):
        if k % 2 == 1:
            d.rectangle([26, y, W - 26, y + RH], fill="#f7f9fc")
        text_fixed(d, (colx[0], y + 20), a, font(25, True), TEXT)
        text_fixed(d, (colx[1], y + 22), b, font(23, True), CORAL if b.startswith("지우기") else BLUE)
        text_fixed(d, (colx[2], y + 23), c, font(21), GRAY)
        y += RH
        d.line([40, y, W - 40, y], fill="#edf0f4", width=1)
    y += 34
    note = ["출처(2027학년도 수시모집요강 면접 유의사항): 단국대학교(죽전) 83쪽(PDF 85) · 숭실대학교 57쪽(PDF 62) · 신한대학교 71쪽(PDF 73)",
            "주민등록번호 · 주소 · 전화번호 · 선생님 이름은 블라인드 규정이 아니라 면접각 「내 생기부로 면접 예상 질문 만들기」의 안내입니다.",
            "대학마다 금지 범위가 다르니 지원 대학 모집요강의 면접 유의사항을 함께 확인하세요."]
    for j, ln in enumerate(note):
        text_fixed(d, (40, y + 30 * j), ln, font(18), GRAY)
    brand(d, W - 230, H - 50, size=24)
    img.save(out)
    print("erase", out, img.size)


def jobs_gpt():
    make_thumb(HERE / "thumb-gpt.png", "ChatGPT로", line2="수시 면접 준비", line3="생기부로 예상 질문", chip="2027 수시 면접")
    make_erase(HERE / "gpt-erase.png")
    make_frames(HERE / "gpt-frames.png")
    make_capture(HERE / "ssu-2027-gpt-interview.png", pdf("숭실대학교"), 62, "학생부종합전형 면접평가 안내", ("after", "해 기울였던 노력에 대해 이야기해 주세요."),
                 "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", "학생부종합 면접 · 발언하면 안 되는 내용과 면접질문 예시",
                 start_pad=8, end_pad=10, lr=30)
    make_capture(HERE / "konkuk-2027-gpt-banned.png", pdf("건국대학교"), 72, "4) 면접형식", ("after", "독서활동 대입 미반영"),
                 "건국대학교", "2027학년도 수시모집요강 72쪽", "KU자기추천 · 기재금지 항목 · 공정성 강화방안 내용은 면접에서 언급 불가",
                 start_pad=3, end_pad=14, lr=30)


if __name__ == "__main__":
    jobs_gpt()
