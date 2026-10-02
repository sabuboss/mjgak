# 신설학과 대표 이미지 (1200x630) — docs/promo/img/promo_style.py 와 같은 팔레트·폰트.
# python site/make_new_images.py  → site/static/img/new/<slug>.png
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUT = ROOT / "static" / "img" / "new"
NAVY, NAVY_D, PALE, ACCENT, CORAL, BG = "#23406e", "#172c4d", "#e8eef8", "#ffd166", "#e8795a", "#f3f5f8"
FONT = {"r": "C:/Windows/Fonts/malgun.ttf", "b": "C:/Windows/Fonts/malgunbd.ttf"}


def font(size, bold=False):
    return ImageFont.truetype(FONT["b" if bold else "r"], size)


def wrap(d, text, fnt, maxw):
    """단어(공백·가운뎃점) 단위로 줄바꿈. 한 단어가 너무 길면 글자 단위."""
    words = text.replace(" · ", " · ").split(" ")
    lines, cur = [], ""
    for w in words:
        w = w.replace(" ", " ")
        cand = (cur + " " + w).strip() if cur else w
        if d.textlength(cand, font=fnt) <= maxw:
            cur = cand; continue
        if cur:
            lines.append(cur)
        cur = ""
        for ch in w:
            if d.textlength(cur + ch, font=fnt) > maxw and cur:
                lines.append(cur); cur = ch
            else:
                cur += ch
    if cur:
        lines.append(cur)
    return lines


def make(slug, label, tag, summary, idx):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # 오른쪽 장식: 겹친 원 + 사선 띠 (학과마다 위치가 조금씩 다르게)
    k = idx % 4
    d.ellipse([W - 420 + k * 20, -120 + k * 30, W + 160, 460 - k * 30], fill=NAVY_D)
    d.ellipse([W - 300, 250 + k * 25, W + 60, 610], fill=PALE)
    d.polygon([(W - 520, H), (W - 300, H), (W + 40, H - 260), (W + 40, H - 120)], fill=CORAL)
    d.rectangle([0, H - 14, W, H], fill=ACCENT)
    # 칩
    fc = font(26, True)
    chip = f"신설학과 · {tag}"
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([60, 60, 60 + cw + 40, 60 + 48], radius=24, fill=ACCENT)
    d.text((80, 66), chip, font=fc, fill=NAVY_D)
    # 제목 (두 줄까지)
    ft = font(60, True)
    lines = wrap(d, label, ft, 720)[:2]
    y = 150
    for ln in lines:
        d.text((60, y), ln, font=ft, fill="white"); y += 76
    d.rectangle([60, y + 14, 180, y + 20], fill=ACCENT)
    # 요약 (세 줄까지)
    fs = font(26)
    y += 50
    for ln in wrap(d, summary, fs, 700)[:3]:
        d.text((60, y), ln, font=fs, fill=PALE); y += 40
    # 브랜드
    fb = font(26, True)
    d.text((60, H - 70), "면접 질문 6개 + 답변 예시", font=font(24), fill=PALE)
    bw = d.textlength("면접각 mjgak.com", font=fb)
    d.rounded_rectangle([W - 60 - bw - 28, H - 80, W - 60 + 14, H - 32], radius=12, fill=NAVY_D)
    d.text((W - 60 - bw - 7, H - 73), "면접각 mjgak.com", font=fb, fill=ACCENT)
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / f"{slug}.png", optimize=True)
    print("ok", slug)


if __name__ == "__main__":
    data = json.loads((ROOT / "content" / "new_departments.json").read_text(encoding="utf-8"))
    for i, dep in enumerate(data["departments"]):
        make(dep["slug"], dep["label"], dep["tag"], dep["summary"], i)
