# 원고의 ▷ 줄(같은 시기 대학·함께 보면 좋은 글)에 실제 발행된 블로그 글 주소를 붙인다.
#   ▷ 제목 (날짜)  →  ▷ 제목 (날짜) | https://blog.naver.com/sabuboss/...
# 주소는 ../blog-urls.tsv(공개 RSS에서 가져온 발행 글 목록)에서 제목 앞부분이 같은 글을 찾는다.
# 발행되지 않은(목록에 없는) 글의 ▷ 줄은 지우고, ▷ 줄이 하나도 남지 않은 섹션은 제목째 지운다.
#   python fill_links.py ../naver-69-서울여대바롬인재면접-v2.md
import re, sys
from pathlib import Path

HERE = Path(__file__).parent
urls = []
for ln in (HERE.parent / "blog-urls.tsv").read_text(encoding="utf-8").splitlines():
    if ln.startswith("#") or not ln.strip():
        continue
    _, _, url, title = ln.split("\t", 3)
    urls.append((title.split(" (")[0].strip(), url))

src = Path(sys.argv[1])
raw = src.read_bytes()
crlf = b"\r\n" in raw
text = raw.decode("utf-8").replace("\r\n", "\n")
body, sep, memo = text.partition("\n" + "=" * 20)
out, kept, dropped = [], [], []
for ln in body.split("\n"):
    m = re.match(r"^▷\s*(.+?)(\s*\|\s*https?://\S+)?$", ln)
    if m:
        name = m.group(1).split(" (")[0].strip()
        hit = next((u for t, u in urls if t == name), None)
        if hit:
            out.append(f"▷ {m.group(1).strip()} | {hit}")
            kept.append(name)
        else:
            dropped.append(name)
        continue
    out.append(ln)
# ▷ 줄이 없는 '■ 같은 시기…'·'■ 함께 보면…' 섹션은 제목과 안내 문단까지 지운다
blocks = "\n".join(out).split("\n■ ")
res = [blocks[0]]
for b in blocks[1:]:
    head = b.split("\n", 1)[0]
    if (head.startswith("같은 시기") or head.startswith("함께 보면") or head.startswith("대학별 면접 글")) and "▷ " not in b:
        # 섹션 끝(다음 빈 줄 두 개 전까지가 섹션)이 아니라 다음 ■ 까지 통째로이므로, 뒤에 이어지는 마무리 문단은 살린다
        tail = b.split("\n\n")
        rest = [p for p in tail[1:] if p.strip() and not p.lstrip().startswith(("같이 지원했다면", "이 글과 함께", "함께 읽으면"))]
        res[-1] = res[-1].rstrip("\n") + ("\n\n" + "\n\n".join(rest) if rest else "")
        continue
    res.append(b)
body = "\n■ ".join(res)
body = re.sub(r"\n{3,}", "\n\n", body)
text = body + sep + memo
src.write_text(text.replace("\n", "\r\n") if crlf else text, encoding="utf-8", newline="")
print("linked:", kept)
print("dropped (not published):", dropped)
