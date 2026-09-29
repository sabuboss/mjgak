# 간호학과 면접 안내 예시 이미지를 Pillow 로 직접 그린다 (브라우저 캡처가 파일로 저장되지 않아 대체).
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).with_name("nursing-interview-notice.png")
F = "C:/Windows/Fonts/malgun.ttf"
FB = "C:/Windows/Fonts/malgunbd.ttf"
W = 1200
rows = [
    ("면접 방식", "학생부 기반 개별 면접 (면접위원 2~3인 대 지원자 1인)"),
    ("면접 시간", "지원자 1인당 약 10분 (질문 5~7개)"),
    ("평가 요소", "전공 적합성(간호사 직업 이해) · 인성 및 의사소통 · 학업 역량 · 발전 가능성"),
    ("반영 비율", "1단계 서류 100% → 2단계 서류 70% + 면접 30% (대학별 상이)"),
    ("면접 일정", "1단계 합격자 발표 후 1~2주 이내 (10월 중순 ~ 11월, 수능 전·후 대학별 상이)"),
    ("준비물", "수험표, 신분증 (학생부·자기소개서 사본은 대학에 따라 요구)"),
    ("복장", "블라인드 면접 원칙 — 교복 등 출신 학교를 알 수 있는 복장 금지, 단정한 평상복"),
    ("유의 사항", "면접 시작 30분 전 대기실 입실 · 전자기기 제출 · 지각 시 응시 불가"),
]
f_tag = ImageFont.truetype(F, 20); f_h1 = ImageFont.truetype(FB, 38); f_sub = ImageFont.truetype(F, 21)
f_th = ImageFont.truetype(FB, 23); f_td = ImageFont.truetype(F, 23); f_note = ImageFont.truetype(F, 20); f_foot = ImageFont.truetype(F, 18)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

PAD = 60; ROW_H = 64
H = 1000
img = Image.new("RGB", (W, H), "#f3f4f6"); d = ImageDraw.Draw(img)
d.rectangle([30, 30, W - 30, H - 30], fill="white", outline="#d9dee5")
y = PAD
d.rounded_rectangle([PAD, y, PAD + 300, y + 34], radius=8, fill="#e8eef8"); d.text((PAD + 12, y + 5), "2027학년도 수시 학생부종합전형", font=f_tag, fill="#2b4c7e"); y += 52
d.text((PAD, y), "간호학과 면접고사 안내 (예시)", font=f_h1, fill="#1c2430"); y += 58
for ln in wrap(d, "아래는 여러 대학 모집요강의 간호학과 면접 안내를 일반화한 예시입니다. 실제 날짜·시간·반영 비율은 지원 대학 모집요강에서 확인하세요.", f_sub, W - 2 * PAD):
    d.text((PAD, y), ln, font=f_sub, fill="#66717f"); y += 30
y += 16
x0, x1, xm = PAD, W - PAD, PAD + 190
for th, td in rows:
    lines = wrap(d, td, f_td, x1 - xm - 28)
    h = max(ROW_H, 24 + 30 * len(lines))
    d.rectangle([x0, y, xm, y + h], fill="#f6f8fb", outline="#cfd6de"); d.rectangle([xm, y, x1, y + h], fill="white", outline="#cfd6de")
    d.text((x0 + 16, y + 16), th, font=f_th, fill="#2b4c7e")
    for i, ln in enumerate(lines): d.text((xm + 14, y + 14 + 30 * i), ln, font=f_td, fill="#1c2430")
    y += h
y += 26
note = "주의  이 표는 면접 준비를 돕기 위한 예시이며 특정 대학의 공식 안내가 아닙니다. 면접 방식과 반영 비율은 대학·전형마다 다르고 해마다 바뀌므로 반드시 해당 학년도 모집요강과 입학처 공지를 확인하세요."
for i, ln in enumerate(wrap(d, note, f_note, W - 2 * PAD)):
    d.text((PAD, y), ln, font=f_note, fill="#c0392b" if i == 0 and False else "#66717f"); y += 28
d.text((PAD, y - 28 * len(wrap(d, note, f_note, W - 2 * PAD))), "주의", font=ImageFont.truetype(FB, 20), fill="#c0392b")
y += 20
foot = "정리: 면접각 mjgak.com"; d.text((x1 - d.textlength(foot, font=f_foot), y), foot, font=f_foot, fill="#9aa4b0"); y += 40
img = img.crop((0, 0, W, min(H, y + 40)))
img.save(OUT); print(OUT, img.size)
