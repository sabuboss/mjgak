# 블로그 원고(md) → 네이버 스마트에디터에 붙여 넣을 서식 페이지(html).
# 발행된 1편(간호학과)의 서식을 그대로 따른다:
#   본문 16px · 소제목 "N. 제목" 굵게 · 질문/Q 줄 노란 형광(#fff8b2) · "답변 예시:" 굵게
#   2주 계획 줄 전체 굵게 + 날짜 빨강(#ff0010) · 링크 "→면접각 바로가기" 굵게 · 문단 사이 빈 줄
#   python make_paste.py ../naver-04-컴퓨터공학과-v2.md
import html, re, sys
from pathlib import Path

src = Path(sys.argv[1])
raw = src.read_text(encoding="utf-8").split("=" * 20)[0].strip().splitlines()
title = raw[0].replace("제목:", "").strip()
lines = raw[1:]

E = html.escape
BODY = "font-size:16px;line-height:1.8;color:#333333;"
out, n_sec, tags, img_list = [], 0, "", []


def p(inner="", style=""):
    out.append(f'<p style="{BODY}{style}">{inner or "&#8203;"}</p>')


for ln in lines:
    s = ln.strip()
    if not s:
        p(); continue
    if s.startswith("#"):
        tags = s; continue
    m = re.match(r"\[(썸네일|캡처 \d|이미지 \d|도식)[^\]]*\]", s)
    if m:
        img_list.append(s.strip("[]"))
        out.append(f'<p class="ph" style="{BODY}background:#fdecea;border:2px dashed #e8795a;padding:10px;color:#c0392b;font-weight:bold;">'
                   f'📷 여기에 이미지 넣기 — {E(s.strip("[]"))}</p>')
        continue
    if s.startswith("■ "):
        n_sec += 1
        p(f"<b>{n_sec}. {E(s[2:])}</b>", "font-size:24px;color:#23406e;")
        continue
    if s.startswith("▶ ") or s.startswith("Q. "):
        p(f'<span style="background-color:#fff8b2;">{E(s)}</span>')
        continue
    if s == "답변 예시:":
        p("<b>답변 예시:</b>"); continue
    m = re.match(r"^(\d+~\d+일차:|\d+일차:|전날:)(.*)$", s)
    if m:
        p(f'<b><span style="color:#ff0010;">{E(m.group(1))}</span>{E(m.group(2))}</b>'); continue
    m = re.match(r"^→\s*(https?://\S+)", s)
    if m:
        p(f'<b><a href="{E(m.group(1))}" style="color:#23406e;">→면접각 바로가기</a></b>'); continue
    p(E(s))

body = "\n".join(out)
imgs = "".join(f"<li>{E(x)}</li>" for x in img_list)
page = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>붙여넣기용 · {E(title)}</title>
<style>
body{{margin:0;background:#f3f5f8;font-family:"Malgun Gothic",sans-serif;color:#1c2430}}
.guide{{max-width:860px;margin:24px auto 0;background:#23406e;color:#fff;border-radius:12px;padding:20px 24px;line-height:1.7}}
.guide b{{color:#ffd166}} .guide ol{{margin:8px 0 0 18px;padding:0}} .guide code{{background:#172c4d;padding:2px 6px;border-radius:4px}}
.row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}
button{{border:0;border-radius:8px;padding:10px 16px;font-size:15px;font-weight:bold;cursor:pointer}}
.b1{{background:#ffd166;color:#172c4d}} .b2{{background:#e8eef8;color:#172c4d}}
.box{{max-width:860px;margin:16px auto;background:#fff;border:1px solid #cfd6de;border-radius:12px;padding:28px 36px}}
.lbl{{font-size:13px;color:#66717f;margin:0 0 6px}}
#title{{font-size:22px;font-weight:bold}}
#toast{{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#172c4d;color:#fff;padding:10px 16px;border-radius:10px;display:none}}
</style></head><body>
<div class="guide">
<b>네이버 블로그 붙여넣기 순서</b>
<ol>
<li>블로그 글쓰기 → 카테고리 <b>대학면접</b> 선택</li>
<li>아래 <b>[제목 복사]</b> → 에디터 제목 칸에 붙여넣기</li>
<li><b>[본문 복사]</b> → 에디터 본문 첫 줄 클릭 후 <code>Ctrl+V</code> (서식 유지됨)</li>
<li>본문의 <b>분홍 칸 "📷 여기에 이미지 넣기"</b>를 지우고 그 자리에 해당 이미지 삽입 (목록은 맨 아래)</li>
<li>"1. ~ 6." 굵은 제목 줄은 선택 후 툴바의 <b>소제목</b>으로 바꾸면 1편과 똑같아집니다</li>
<li><b>[태그 복사]</b> → 에디터 하단 태그 칸에 붙여넣기 → 썸네일을 대표 이미지로 지정 → 발행</li>
</ol>
<div class="row"><button class="b1" onclick="cp('title')">제목 복사</button><button class="b1" onclick="cp('body',true)">본문 복사</button><button class="b2" onclick="cp('tags')">태그 복사</button></div>
</div>
<div class="box"><p class="lbl">제목</p><div id="title">{E(title)}</div></div>
<div class="box"><p class="lbl">본문 (이 영역 전체가 복사됩니다)</p><div id="body">
{body}
</div></div>
<div class="box"><p class="lbl">태그 (#은 에디터가 자동으로 붙이므로 그대로 붙여 넣어도 됩니다)</p><div id="tags">{E(tags)}</div></div>
<div class="box"><p class="lbl">넣을 이미지 목록 (docs/promo/img 폴더)</p><ol>{imgs}</ol></div>
<div id="toast"></div>
<script>
async function cp(id, rich){{
  const el=document.getElementById(id); const text=el.innerText;
  try{{
    if(rich && window.ClipboardItem){{
      await navigator.clipboard.write([new ClipboardItem({{"text/html":new Blob([el.innerHTML],{{type:"text/html"}}),"text/plain":new Blob([text],{{type:"text/plain"}})}})]);
    }} else {{ await navigator.clipboard.writeText(text); }}
  }}catch(e){{
    const r=document.createRange(); r.selectNodeContents(el); const s=getSelection(); s.removeAllRanges(); s.addRange(r); document.execCommand("copy"); s.removeAllRanges();
  }}
  const t=document.getElementById("toast"); t.textContent=({{title:"제목",body:"본문",tags:"태그"}})[id]+" 복사됨"; t.style.display="block"; setTimeout(()=>t.style.display="none",1500);
}}
</script></body></html>"""
dst = Path(__file__).parent / (src.stem.replace("-v2", "") + "-붙여넣기.html")
dst.write_text(page, encoding="utf-8")
print(dst, "sections:", n_sec, "images:", len(img_list))
