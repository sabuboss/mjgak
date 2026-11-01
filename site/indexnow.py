"""배포 직후 새로 생기거나 lastmod 가 바뀐 페이지 주소를 IndexNow(빙 등 공용, 무료)로 알린다.

ChatGPT 검색은 빙 색인을 많이 쓰므로 새 페이지·고친 페이지가 빨리 잡히게 하려는 것.
.github/workflows/site.yml 이 배포 전 실제 사이트의 sitemap.xml 을 old-sitemap.xml 로 받아 두고, 배포 뒤 이 파일을 실행한다.
  python site/indexnow.py <old-sitemap.xml>
"""
import json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
key = site.get("indexnow_key")


def entries(text):
    return dict(re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", text))


new = entries((ROOT / "dist" / "sitemap.xml").read_text(encoding="utf-8"))
old_f = Path(sys.argv[1]) if len(sys.argv) > 1 else None
old = entries(old_f.read_text(encoding="utf-8")) if old_f and old_f.exists() else {}
if not old:
    print("이전 sitemap 을 못 받아 이번엔 보내지 않음")  # 전체를 보내면 남용처럼 보일 수 있어서
    sys.exit(0)
urls = [u for u, d in new.items() if old.get(u) != d]
if not key or not urls:
    print("알릴 주소 없음")
    sys.exit(0)
host = site["url"].split("//", 1)[1].strip("/")
body = {"host": host, "key": key, "keyLocation": f"{site['url']}/{key}.txt", "urlList": urls[:10000]}
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json; charset=utf-8"})
for i in range(3):
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow", r.status, len(urls), "개 주소")
            break
    except urllib.error.HTTPError as e:
        print("IndexNow 응답", e.code, e.read()[:200])  # 403 은 키 파일이 아직 배포 전일 때
        break
    except urllib.error.URLError as e:
        print("연결 실패, 다시 시도", e)
        time.sleep(20)
