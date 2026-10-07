"""면접각 자동 감시 — 매달 GitHub Actions 가 실행한다 (.github/workflows/monitor.yml).

확인하는 것 세 가지:
  1. 새 학년도 수시 모집요강 PDF 가 서울진로진학정보센터 CDN 에 올라왔는지 (블로그 글에 쓴 대학 기준)
     + 새 선행학습 영향평가 보고서(전년도 기출)가 올라왔는지 (기출 공개 대학 기준)
  2. 사이트에 임베드한 유튜브 영상이 아직 재생되는지 (oembed 200)
  3. 전국 대학 목록의 홈페이지 링크가 살아 있는지

결과는 monitor/state.json 에 저장하고, 지난달과 달라진 것만 monitor/report.md 에 쓴다.
report.md 가 비어 있지 않으면 워크플로가 GitHub 이슈를 연다.

로컬 실행:  python monitor/check.py            (회사망처럼 SSL 검사가 막히면 MJGAK_INSECURE=1)
"""
from __future__ import annotations
import glob, json, os, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests, urllib3

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "monitor" / "state.json"
REPORT = ROOT / "monitor" / "report.md"
VERIFY = os.environ.get("MJGAK_INSECURE") != "1"
if not VERIFY:
    urllib3.disable_warnings()
H = {"User-Agent": "Mozilla/5.0 (compatible; mjgak-monitor/1.0; +https://mjgak.com)"}
CDN = "https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info{y}/{u}/{u}_{yy}학년도_{doc}.pdf"

# 블로그 글(docs/promo/naver-*.md)과 캡처(promo_style.py / jobs_*.py)에 쓴 대학. CDN 에 없는 교대·울산·경남·남부는 뺀다.
GUIDE_UNIVS = [
    "강남대학교", "강원대학교", "건국대학교", "경기대학교", "경희대학교", "광운대학교", "국민대학교", "남서울대학교",
    "덕성여자대학교", "동국대학교", "명지대학교", "백석대학교", "부산대학교", "삼육대학교", "서울시립대학교", "선문대학교",
    "성신여자대학교", "세종대학교", "숙명여자대학교", "숭실대학교", "아주대학교", "용인대학교", "을지대학교", "이화여자대학교",
    "인하대학교", "전남대학교", "전북대학교", "제주대학교", "중앙대학교", "청주대학교", "충남대학교", "한국교원대학교",
    "한국외국어대학교", "한림대학교", "한세대학교", "호서대학교",
]
# 면접 기출을 공개하는 대학(선행학습 영향평가 보고서) — site 의 실제 기출 출처
REPORT_UNIVS = ["서울대학교", "고려대학교", "연세대학교", "성균관대학교", "한양대학교", "부산대학교", "아주대학교", "중앙대학교", "인하대학교", "대진대학교"]


def today():
    return datetime.date.today()


def next_guide_year():
    """지금 사이트가 쓰는 학년도 다음 해. 2026년 10월이면 2028학년도(2027년 5~6월 공개)."""
    d = today()
    return d.year + 2 if d.month >= 7 else d.year + 1


def head_ok(url, timeout=20):
    try:
        r = requests.head(url, headers=H, timeout=timeout, verify=VERIFY, allow_redirects=True)
        if r.status_code == 405:
            r = requests.get(url, headers=H, timeout=timeout, verify=VERIFY, stream=True)
        return r.status_code, r.headers.get("Content-Length")
    except requests.RequestException as e:
        return None, type(e).__name__


def check_pdfs():
    yy = next_guide_year()
    y = yy - 1
    found = {}
    for u in GUIDE_UNIVS:
        code, size = head_ok(CDN.format(y=y, u=u, yy=yy, doc="수시모집요강"))
        if code == 200:
            found[u] = size
        time.sleep(0.2)
    ry = y  # 선행학습 보고서는 그해 봄에 "해당 학년도" 이름으로 올라온다 (2027학년도 보고서 → univ_info2027)
    reports = {}
    for u in REPORT_UNIVS:
        code, size = head_ok(CDN.format(y=ry, u=u, yy=ry, doc="선행학습영향평가"))
        if code == 200:
            reports[u] = size
        time.sleep(0.2)
    return {"guide_year": yy, "guides": found, "report_year": ry, "reports": reports}


def all_videos():
    out = []
    for f in sorted(glob.glob(str(ROOT / "site" / "content" / "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        items = d.get("departments") or d.get("universities") or []
        for it in items:
            for v in it.get("videos", []):
                out.append({"file": Path(f).name, "owner": it.get("slug") or it.get("code"), "id": v["id"], "title": v.get("title", "")})
    return out


def _video(v):
    try:
        r = requests.get("https://www.youtube.com/oembed", params={"url": "https://www.youtube.com/watch?v=" + v["id"], "format": "json"},
                         headers=H, timeout=15, verify=VERIFY)
        return None if r.status_code == 200 else {**v, "status": r.status_code}
    except requests.RequestException as e:
        return {**v, "status": type(e).__name__}


def check_videos():
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(_video, all_videos()))
    return {r["id"]: r for r in res if r}


def all_sites():
    out = []
    u = json.load(open(ROOT / "site" / "content" / "universities.json", encoding="utf-8"))
    for reg in u.get("regions", []):
        for x in reg.get("universities", []):
            if x.get("url"):
                out.append({"code": x["code"], "name": x["name"], "url": x["url"]})
    return out


def _site(s):
    try:
        r = requests.get(s["url"], headers=H, timeout=12, verify=VERIFY, allow_redirects=True)
        return None if r.status_code < 400 else {**s, "status": r.status_code}
    except requests.exceptions.SSLError:
        return None  # 대학 사이트의 인증서 문제는 흔하고 브라우저에선 대개 열린다 — 경고하지 않음
    except requests.RequestException as e:
        return {**s, "status": type(e).__name__}


def check_sites():
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(_site, all_sites()))
    return {r["code"]: r for r in res if r}


def main():
    prev = json.load(open(STATE, encoding="utf-8")) if STATE.exists() else {}
    first = not prev
    cur = {"checked": today().isoformat(), "pdfs": check_pdfs(), "dead_videos": check_videos(), "bad_sites": check_sites()}

    lines = []
    p, q = cur["pdfs"], prev.get("pdfs", {})
    new_guides = sorted(set(p["guides"]) - set(q.get("guides", {}))) if q.get("guide_year") == p["guide_year"] else sorted(p["guides"])
    if new_guides:
        lines.append(f"## {p['guide_year']}학년도 수시 모집요강이 새로 올라온 대학 {len(new_guides)}곳 (전체 {len(p['guides'])}/{len(GUIDE_UNIVS)})")
        lines += [f"- {u}" for u in new_guides]
        lines.append("")
        lines.append("→ docs/MAINTENANCE.md '연간 갱신' 순서대로: PDF 내려받기 → jobs_*.py 로 캡처 재생성 → 블로그 글 숫자 갱신 → 네이버 기존 글 수정.")
        lines.append("")
    new_reports = sorted(set(p["reports"]) - set(q.get("reports", {}))) if q.get("report_year") == p["report_year"] else sorted(p["reports"])
    if new_reports:
        lines.append(f"## {p['report_year']}학년도 선행학습 영향평가 보고서(전년도 면접 기출)가 올라온 대학 {len(new_reports)}곳")
        lines += [f"- {u}" for u in new_reports]
        lines.append("")
        lines.append("→ pipeline/bulk_reports.py 로 받아 기출을 추가한다.")
        lines.append("")

    dv, pv = cur["dead_videos"], prev.get("dead_videos", {})
    newly_dead = {k: v for k, v in dv.items() if k not in pv}
    revived = sorted(set(pv) - set(dv))
    if newly_dead or (first and dv):
        show = dv if first else newly_dead
        lines.append(f"## 재생되지 않는 유튜브 영상 {len(show)}개" + ("" if first else f" (새로 생김, 누적 {len(dv)}개)"))
        for v in show.values():
            lines.append(f"- `{v['id']}` {v['title'][:40]} — {v['file']} / {v['owner']} (상태 {v['status']})")
        lines.append("")
        lines.append("→ 해당 json 의 videos 에서 빼거나 같은 대학 공식 채널의 다른 영상으로 바꾼다.")
        lines.append("")
    if revived:
        lines.append(f"## 다시 재생되는 영상 {len(revived)}개: " + ", ".join(revived))
        lines.append("")

    # 대학 홈페이지는 한 달만 안 열리는 경우(점검·해외 IP 차단)가 흔해서, 두 달 연속 실패한 곳만 한 번 알린다.
    bs, pb = cur["bad_sites"], prev.get("bad_sites", {})
    confirmed = {k: v for k, v in bs.items() if k in pb}
    to_report = {k: v for k, v in confirmed.items() if k not in set(prev.get("reported_sites", []))}
    cur["reported_sites"] = sorted(confirmed)
    if to_report:
        lines.append(f"## 두 달 연속 열리지 않는 대학 홈페이지 {len(to_report)}곳")
        for s in to_report.values():
            lines.append(f"- {s['name']} {s['url']} (상태 {s['status']})")
        lines.append("")
        lines.append("→ 브라우저로 열어 보고 주소가 바뀌었으면 site/content/universities.json 의 url 을 고친다. 브라우저에선 열리면 해외 IP 차단이니 무시.")
        lines.append("")

    REPORT.write_text("\n".join(lines).strip() + ("\n" if lines else ""), encoding="utf-8")
    STATE.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = (f"checked {cur['checked']}: guides {len(p['guides'])}/{len(GUIDE_UNIVS)} for {p['guide_year']}, reports {len(p['reports'])}/{len(REPORT_UNIVS)}, "
               f"dead videos {len(dv)}, bad sites {len(bs)}, report lines {len(lines)}")
    print(summary)
    (ROOT / "monitor" / "summary.txt").write_text(summary + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
