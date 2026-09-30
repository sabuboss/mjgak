# 면접 답변 구조 4단계 도식 (결론 → 경험 → 배운 점 → 연결) 이미지 생성
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).with_name("answer-structure-4steps-ece.png")
F = "C:/Windows/Fonts/malgun.ttf"; FB = "C:/Windows/Fonts/malgunbd.ttf"
W, H = 1200, 1120
NAVY, BLUE, LIGHT, GRAY, TEXT, RED = "#2b4c7e", "#3b6db3", "#e8eef8", "#66717f", "#1c2430", "#c0392b"

steps = [
    ("1", "결론", "질문에 대한 답을 한 문장으로 먼저", "\"유아기의 경험이 평생을 좌우한다는 걸 알게 돼서, 아이를 좋아하는 마음을 전문성으로 키우고 싶어 지원했습니다.\""),
    ("2", "경험", "그렇게 생각하게 된 경험 하나 (언제·무엇·숫자)", "\"어린이집 봉사에서 말이 늦던 아이가 선생님과 매일 그림책을 읽으며 한 학기 만에 문장으로 말하는 걸 봤습니다.\""),
    ("3", "배운 점", "그 경험 전후로 무엇이 달라졌나", "\"아이를 좋아하는 마음만으로는 안 되고 발달을 이해하고 관찰하는 전문성이 필요하다는 걸 알았습니다.\""),
    ("4", "연결", "그래서 이 학과에서 무엇을 하고 싶은가", "\"이 학과에서 아동발달과 놀이지도를 배워, 한 아이의 속도를 읽어 내는 교사가 되고 싶습니다.\""),
]

f_title = ImageFont.truetype(FB, 40); f_sub = ImageFont.truetype(F, 22)
f_num = ImageFont.truetype(FB, 30); f_label = ImageFont.truetype(FB, 30); f_desc = ImageFont.truetype(F, 22)
f_ex = ImageFont.truetype(F, 21); f_small = ImageFont.truetype(F, 19); f_foot = ImageFont.truetype(F, 18)

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for ch in text:
        t = cur + ch
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = ch
    if cur: out.append(cur)
    return out

img = Image.new("RGB", (W, H), "#f3f4f6"); d = ImageDraw.Draw(img)
d.rectangle([30, 30, W - 30, H - 30], fill="white", outline="#d9dee5")
PAD = 60; y = 60
d.text((PAD, y), "면접 답변 구조 4단계", font=f_title, fill=TEXT); y += 56
d.text((PAD, y), "어떤 질문이든 이 순서로 40~60초. 외우는 게 아니라 구조를 익히는 것입니다.", font=f_sub, fill=GRAY); y += 50

box_x0, box_x1 = PAD, W - PAD
for i, (n, label, desc, ex) in enumerate(steps):
    ex_lines = wrap(d, ex, f_ex, (box_x1 - 16) - (box_x0 + 170 + 46) - 16)
    h = 96 + 28 * len(ex_lines)
    d.rounded_rectangle([box_x0, y, box_x1, y + h], radius=14, fill="white", outline="#cfd6de", width=2)
    d.rounded_rectangle([box_x0, y, box_x0 + 150, y + h], radius=14, fill=LIGHT)
    d.rectangle([box_x0 + 120, y, box_x0 + 150, y + h], fill=LIGHT)
    d.ellipse([box_x0 + 22, y + 18, box_x0 + 66, y + 62], fill=NAVY)
    d.text((box_x0 + 44 - d.textlength(n, font=f_num) / 2, y + 22), n, font=f_num, fill="white")
    d.text((box_x0 + 22, y + h - 52), label, font=f_label, fill=NAVY)
    tx = box_x0 + 170
    d.text((tx, y + 18), desc, font=f_desc, fill=TEXT)
    d.rounded_rectangle([tx, y + 56, box_x1 - 16, y + 56 + 28 * len(ex_lines) + 16], radius=8, fill="#f6f8fb")
    d.text((tx + 12, y + 60), "예)", font=f_small, fill=BLUE)
    for j, ln in enumerate(ex_lines):
        d.text((tx + 46, y + 62 + 28 * j), ln, font=f_ex, fill=TEXT)
    y += h
    if i < len(steps) - 1:
        cx = box_x0 + 75
        d.polygon([(cx - 12, y + 6), (cx + 12, y + 6), (cx, y + 24)], fill=NAVY)
        y += 32

y += 26
tips = ["숫자와 고유명사를 넣으면 진짜 경험으로 들립니다.", "[대괄호] 자리는 본인 경험으로 바꾸세요. 예시를 그대로 외우면 면접관이 알아봅니다.", "한 답변이 60초를 넘기면 잘라내세요. 녹음해서 확인."]
d.text((PAD, y), "이렇게 쓰세요", font=ImageFont.truetype(FB, 22), fill=RED); y += 34
for t in tips:
    d.ellipse([PAD + 4, y + 10, PAD + 12, y + 18], fill=NAVY)
    d.text((PAD + 24, y), t, font=f_small, fill=TEXT); y += 30
foot = "정리: 면접각 mjgak.com"
d.text((W - PAD - d.textlength(foot, font=f_foot), H - 70), foot, font=f_foot, fill="#9aa4b0")
img = img.crop((0, 0, W, min(H, max(y + 90, 700))))
d2 = ImageDraw.Draw(img); d2.rectangle([30, img.height - 31, W - 30, img.height - 30], fill="#d9dee5")
img.save(OUT); print(OUT, img.size)
