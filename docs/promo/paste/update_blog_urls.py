# 공개 RSS(최근 50개)에서 발행된 블로그 글 목록을 받아 ../blog-urls.tsv 에 합친다(이미 있는 주소는 그대로).
# 사용자 허락(2026-10-17) 하에 공개 RSS 만 읽는다. 네이버 로그인·글쓰기 화면은 건드리지 않는다.
#   python update_blog_urls.py
import re, subprocess, sys, html
from pathlib import Path

TSV = Path(__file__).parent.parent / "blog-urls.tsv"
RSS = "https://rss.blog.naver.com/sabuboss.xml"

xml = subprocess.run(["curl", "-s", "--max-time", "30", RSS], capture_output=True).stdout.decode("utf-8", "replace")
items = re.findall(r"<item>(.*?)</item>", xml, re.S)
if not items:
    sys.exit("RSS 를 읽지 못했습니다")


def tag(s, name):
    m = re.search(rf"<{name}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{name}>", s, re.S)
    return html.unescape(m.group(1).strip()) if m else ""


lines = TSV.read_text(encoding="utf-8").splitlines()
have = {ln.split("\t")[2] for ln in lines if ln and not ln.startswith("#")}
new = []
for it in items:
    url = re.sub(r"\?.*$", "", tag(it, "link"))
    if not url or url in have:
        continue
    d = re.search(r"\d{1,2} \w{3} \d{4}", tag(it, "pubDate"))
    new.append("\t".join([d.group(0) if d else "", tag(it, "category"), url, tag(it, "title")]))
if new:
    head, body = lines[:1], lines[1:]
    TSV.write_text("\n".join(head + new + body) + "\n", encoding="utf-8")
print(f"RSS {len(items)}개 중 새 글 {len(new)}개 추가")
for n in new:
    print(" ", n.split("\t")[3][:60])
