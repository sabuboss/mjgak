#!/usr/bin/env python3
"""면접각 정적 사이트 생성기.  content/*.json + ../data/seed/profiles + ../pipeline/out/*.jsonl -> dist/

사용법:
  pip install jinja2
  python build.py            # dist/ 생성
  python -m http.server -d dist 8000

원칙 (docs/SPEC.md 1-2):
  - 대학 원문 PDF 는 싣지 않는다. 문항 텍스트·요약과 출처 링크만.
  - 실제 기출(actual) / 대학 예시(example) / 이 사이트가 만든 질문(표준·예상) 을 항상 구분 표시.
"""
from __future__ import annotations

import datetime
import html
import json
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from jinja2 import Environment, FileSystemLoader

import datesparse

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DIST = ROOT / "dist"
TODAY = datetime.date.today()

site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
site["ver"] = datetime.datetime.now().strftime("%Y%m%d%H%M")  # CSS·JS 캐시 무효화
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=False)

# 원문에 상업적 이용·발췌 금지 문구가 있는 대학: 문항 원문은 싣지 않고 공개 현황과 원문 링크만 안내한다.
RESTRICTED = {
    "snu": "이 문서는 상업적인 목적으로 사용할 수 없으며, 문서의 변형 및 발췌를 금지합니다.",
    "skku": "이 문서는 상업적인 목적으로 사용할 수 없으며, 문서의 변형 및 발췌를 금지합니다.",
    "yonsei": "이 보고서의 저작권은 연세대학교에 있습니다. 상업적인 사용을 금합니다.",
    "yonsei-mirae": "이 보고서의 저작권은 연세대학교에 있습니다. 상업적인 사용을 금합니다.",
}
KIND_LABEL = {"actual": "실제 기출", "example": "대학 공개 예시", "predicted": "예상 질문", "none": "문항 미공개"}
CATEGORY_LABEL = {
    "student_record": "서류(학생부) 기반 면접", "essay_based": "제시문 기반 면접", "personality": "인성면접",
    "major": "전공 면접", "english": "영어 면접", "mmi": "적성·인성(MMI) 면접",
}
TYPE_ORDER = ["VOCATIONAL", "GED", "REPEAT", "OVERSEAS_3", "OVERSEAS_12", "ALTERNATIVE", "GENERAL"]


# ---------- 유틸 ----------
def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def ph(text: str) -> str:
    """[대괄호 자리표시자] 를 강조 표시. HTML 이스케이프 후 처리."""
    t = html.escape(text)
    return re.sub(r"\[([^\]]+)\]", r'<mark class="ph">[\1]</mark>', t)


BASE = site.get("base", "").rstrip("/")  # GitHub Pages 처럼 하위 경로에 올릴 때 "/mjgak". 루트 도메인이면 "".
site["url"] = site["url"].rstrip("/") + BASE  # canonical·sitemap·RSS·JSON-LD 는 전체 주소를 쓴다


def with_base(content: str) -> str:
    """루트 절대 링크(href="/…", src="/…")에 BASE 를 붙인다. 외부 링크(//, http)는 건드리지 않는다."""
    if not BASE:
        return content
    content = re.sub(r"((?:href|src|action)=\")/(?!/)", lambda m: m.group(1) + BASE + "/", content)
    return content.replace('fetch("/search.json")', f'fetch("{BASE}/search.json")')


def write(path: str, content: str):
    p = DIST / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if path.endswith((".html", ".js")):
        content = with_base(content)
    p.write_text(content, encoding="utf-8")


def page(path: str, tpl: str, **ctx):
    ctx.setdefault("site", site)
    ctx.setdefault("year", TODAY.year)
    ctx.setdefault("path", "/" + path.rstrip("/") + ("/" if path else ""))
    ctx["base"] = BASE
    write((path + "/index.html") if path else "index.html", env.get_template(tpl).render(**ctx))


def tokens(s: str) -> set[str]:
    return {w for w in re.findall(r"[가-힣]{2,}", s)}


# ---------- 데이터 ----------
def load_common():
    c = load(ROOT / "content" / "common.json")
    for q in c["questions"]:
        q["url"] = f"/q/{q['slug']}/"
        q["cat_label"] = c["categories"][q["category"]]["label"]
    return c


def load_profiles():
    ans = load(ROOT / "content" / "type_answers.json")["answers"]
    out = []
    for code in TYPE_ORDER:
        p = load(REPO / "data" / "seed" / "profiles" / f"{code}.json")
        for q in p["seed_questions"]:
            q["answer"] = ans.get(q["id"])
        p["url"] = f"/type/{code.lower()}/"
        out.append(p)
    return out


def load_actual():
    """pipeline/out/*.jsonl -> {univ_code: [records]} (report 제외, 텍스트 있는 것만)."""
    by: dict[str, list] = {}
    for f in sorted((REPO / "pipeline" / "out").glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if not r.get("text", "").strip():
                continue
            r = clean_actual(r)
            if r is None:
                continue
            by.setdefault(r["university_code"], []).append(r)
    return by


RICH = ROOT / "content" / "rich"
PUA = re.compile("[\ue000-\uf8ff]+")  # PDF 수식 폰트가 깨진 문자(사용자 영역)


def load_rich(kind: str) -> dict:
    d = RICH / kind
    return {p.stem: load(p) for p in sorted(d.glob("*.json"))} if d.exists() else {}


def load_examples() -> dict:
    p = RICH / "examples.json"
    return load(p) if p.exists() else {"common": {}, "majors": {}, "types": {}}


def clean_actual(r: dict) -> dict | None:
    """깨진 수식 문자 정리, 제목만 있는 문항은 제시문 앞부분을 붙이고, 출제 근거 같은 비문항은 뺀다."""
    t = (r.get("text") or "").strip()
    if "출제 근거" in t:
        return None
    for k in ("text", "presented_material", "intent"):
        if r.get(k):
            if PUA.search(r[k]):
                r["has_glyph"] = True
            r[k] = PUA.sub("□", r[k])
    core = re.sub(r"^(\[[^\]]*\]\s*)+", "", r["text"]).strip()
    pm = (r.get("presented_material") or "").strip()
    if not core:
        if not pm:
            return None
        r["text"] = r["text"].strip() + " (제시문) " + (pm[:140] + "…" if len(pm) > 140 else pm)
    return r


def load_univ_seed():
    return {u["code"]: u for u in load(REPO / "data" / "seed" / "universities.json")["universities"]}


def load_departments():
    """content/departments_*.json -> 학과 목록 (group 은 majors.json 의 code)."""
    out = []
    for f in sorted((ROOT / "content").glob("departments_*.json")):
        out += load(f)["departments"]
    seen = set()
    for d in out:
        assert d["slug"] not in seen, f"duplicate dept slug {d['slug']}"
        seen.add(d["slug"])
        d["url"] = f"/dept/{d['slug']}/"
    return out


NICK = {"고려대학교": ["고대"], "연세대학교": ["연대"], "성균관대학교": ["성대"], "중앙대학교": ["중대"], "이화여자대학교": ["이대"],
        "숙명여자대학교": ["숙대"], "한국외국어대학교": ["외대", "한국외대"], "서울시립대학교": ["시립대"], "건국대학교": ["건대"],
        "동국대학교": ["동대"], "홍익대학교": ["홍대"], "한양대학교": ["한대"], "경북대학교": ["경대"], "한양대학교(ERICA)": ["한양에리카", "에리카", "한대 에리카"], "한양대학교 ERICA": ["한양에리카", "에리카", "한대 에리카", "한양대 안산"],
        "한국교원대학교": ["교원대"], "서울과학기술대학교": ["서울과기대", "과기대"], "한국과학기술원(KAIST)": ["카이스트"], "KAIST": ["카이스트", "한국과학기술원"],
        "POSTECH(포항공과대학교)": ["포스텍", "포항공대"], "UNIST(울산과학기술원)": ["유니스트", "울산과기원"], "GIST(광주과학기술원)": ["지스트"], "DGIST(대구경북과학기술원)": ["디지스트"]}


def univ_aliases(name: str) -> list[str]:
    """대학 이름의 흔한 줄임말: 서울교육대학교 → 서울교대, 숙명여자대학교 → 숙명여대, 국립창원대학교 → 창원대 …"""
    out = set()
    bases = {name, re.sub(r"^국립", "", name), re.sub(r"\(.*?\)", "", name).strip()}
    for b in list(bases):
        bases.add(re.sub(r"^국립", "", b))
    for b in bases:
        for pat, rep in (("교육대학교", "교대"), ("여자대학교", "여대"), ("과학기술대학교", "과기대"), ("외국어대학교", "외대"),
                         ("산업대학교", "산업대"), ("공과대학교", "공대"), ("대학교", "대"), ("대학$", "대")):
            if re.search(pat, b):
                out.add(re.sub(pat, rep, b))
        out.add(b)
    out |= set(NICK.get(name, []))
    out.discard(name)
    return sorted(x for x in out if len(x) >= 2)


def load_new_departments():
    """content/new_departments.json -> 신설학과 목록."""
    data = load(ROOT / "content" / "new_departments.json")
    for d in data["departments"]:
        d["url"] = f"/new/{d['slug']}/"
        # 제미나이 실사 이미지: static/img/new/photo-<slug>.(png|jpg|webp) 가 있으면 본문에 노출
        for ext in ("png", "jpg", "jpeg", "webp"):
            if (ROOT / "static" / "img" / "new" / f"photo-{d['slug']}.{ext}").exists():
                d["photo"] = f"/static/img/new/photo-{d['slug']}.{ext}"
                break
    return data


def load_profiles_univ():
    """content/university_profiles*.json 을 합친다. notice/common_questions 는 첫 파일 것."""
    p = load(ROOT / "content" / "university_profiles.json")
    for f in sorted((ROOT / "content").glob("university_profiles_*.json")):
        p["universities"] += load(f)["universities"]
    seen = set()
    for u in p["universities"]:
        assert u["code"] not in seen, f"duplicate univ profile {u['code']}"
        seen.add(u["code"])
        u["url"] = f"/univ/{u['code']}/"
    return p


def jsonld_faq(title: str, desc: str, url_path: str, qa: list):
    url = f"{site['url']}{url_path}"
    ents = [{"@type": "Question", "name": q["question"],
             "acceptedAnswer": {"@type": "Answer", "text": q.get("example") or re.sub(r"\[([^\]]+)\]", r"(\1)", q["answer"])}} for q in qa]
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc,
         "author": {"@type": "Person", "name": site["author"], "url": f"{site['url']}/about/"},
         "publisher": {"@type": "Organization", "name": site["name"], "url": site["url"]},
         "datePublished": site["publish_date"], "dateModified": site["publish_date"], "mainEntityOfPage": url},
        {"@type": "FAQPage", "mainEntity": ents}]}, ensure_ascii=False)


def related_by_keywords(kw: set[str], actual_by, univ_names, limit=3):
    scored = []
    for code, recs in actual_by.items():
        if code in RESTRICTED:
            continue
        for r in recs:
            if r["kind"] not in ("actual", "example") or len(r["text"]) > 220:
                continue
            s = len(kw & tokens(r["text"]))
            if s >= 2:
                scored.append((s, r["year"], code, r))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    return [{"univ": univ_names.get(code, code), "code": code, "year": y, "text": r["text"], "kind": KIND_LABEL[r["kind"]],
             "url": f"/univ/{code}/{y}/"} for s, y, code, r in scored[:limit]]


# ---------- 렌더 조각 ----------
def related_actual(q, actual_by, univ_names, limit=3):
    """공통 질문과 비슷한 실제 기출 3개 (키워드·토큰 겹침 점수)."""
    kw = set(q.get("keywords", [])) | tokens(q["question"])
    scored = []
    for code, recs in actual_by.items():
        if code in RESTRICTED:
            continue
        for r in recs:
            if r["kind"] not in ("actual", "example") or len(r["text"]) > 220:
                continue
            t = tokens(r["text"])
            s = len(kw & t)
            if s >= 2:
                scored.append((s, r["year"], code, r))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    out = []
    for s, y, code, r in scored[:limit]:
        out.append({"univ": univ_names.get(code, code), "code": code, "year": y, "text": r["text"], "kind": KIND_LABEL[r["kind"]],
                    "url": f"/univ/{code}/{y}/", "source_url": r["source_url"]})
    return out


def jsonld_question(q):
    url = f"{site['url']}{q['url']}"
    answer = re.sub(r"\[([^\]]+)\]", r"(\1)", q["answer"])
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": q["question"], "description": q["why"],
             "author": {"@type": "Person", "name": site["author"], "url": f"{site['url']}/about/"},
             "publisher": {"@type": "Organization", "name": site["name"], "url": site["url"]},
             "datePublished": site["publish_date"], "dateModified": site["publish_date"], "mainEntityOfPage": url},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["question"],
                                                 "acceptedAnswer": {"@type": "Answer", "text": answer}}]},
        ],
    }, ensure_ascii=False)


def write_sitemap(urls):
    L = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        L.append(f"  <url><loc>{site['url']}{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>")
    L.append("</urlset>")
    write("sitemap.xml", "\n".join(L) + "\n")


def write_rss(items):
    L = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
         f"<title>{escape(site['name'])}</title><link>{site['url']}/</link><description>{escape(site['tagline'])}</description><language>ko</language>"]
    for t, u, d in items[:30]:
        L.append(f"<item><title>{escape(t)}</title><link>{site['url']}{u}</link><guid>{site['url']}{u}</guid><description>{escape(d)}</description></item>")
    L.append("</channel></rss>")
    write("rss.xml", "\n".join(L) + "\n")


def md_page(name: str):
    """pages/<name>.md : 'title: ..\\ndescription: ..\\n---\\n<html>' 형식 (마음체크와 동일)."""
    raw = (ROOT / "pages" / f"{name}.md").read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = dict(line.split(":", 1) for line in head.splitlines() if ":" in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    body = body.replace("{{ contact_email }}", site.get("contact_email", "")).replace("{{ author }}", site.get("author", ""))
    return meta, body


# ---------- 메인 ----------
def main():
    if DIST.exists():
        # 폴더 자체가 다른 프로세스에 잡혀 있어도 되도록 안의 내용만 비운다
        for child in DIST.iterdir():
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "static", DIST / "static")
    js = DIST / "static" / "site.js"
    js.write_text(with_base(js.read_text(encoding="utf-8")), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: Jekyll 처리 끄기
    if site.get("adsense_client"):  # 애드센스 ads.txt (루트 도메인 배포 시 유효)
        (DIST / "ads.txt").write_text("google.com, " + site["adsense_client"].replace("ca-", "") + ", DIRECT, f08c47fec0942fa0" + chr(10), encoding="utf-8")
    for fname in site.get("google_verification_files", []):  # 서치콘솔 HTML 파일 인증
        (DIST / fname).write_text(f"google-site-verification: {fname}", encoding="utf-8")

    common = load_common()
    majors = load(ROOT / "content" / "majors.json")
    profiles = load_profiles()
    unis = load(ROOT / "content" / "universities.json")
    actual_by = load_actual()
    seed = load_univ_seed()
    univ_names = {c: seed[c]["name"] for c in seed}
    with_data = [c for c in actual_by if c in seed]
    urls, rss = [], []

    # 카테고리별 질문 묶음
    by_cat = {k: [q for q in common["questions"] if q["category"] == k] for k in common["categories"]}
    for k in common["categories"]:
        common["categories"][k]["url"] = f"/category/{k}/"
        common["categories"][k]["n"] = len(by_cat[k])

    # 대학 요약 (기출 있는 대학)
    univ_cards = []
    for code in with_data:
        recs = actual_by[code]
        years = sorted({r["year"] for r in recs}, reverse=True)
        univ_cards.append({"code": code, "name": univ_names[code], "n": len(recs), "years": years,
                           "actual": sum(1 for r in recs if r["kind"] == "actual"), "url": f"/univ/{code}/"})
    univ_cards.sort(key=lambda u: -u["n"])
    for m in majors["majors"]:
        m["url"] = f"/major/{m['code']}/"

    # 학과별 + 대학 프로필
    depts = load_departments()
    major_by = {m["code"]: m for m in majors["majors"]}
    for m in majors["majors"]:
        m["depts"] = [d for d in depts if d["group"] == m["code"]]
    for d in depts:
        assert d["group"] in major_by, f"unknown group {d['group']} in {d['slug']}"
    uprof = load_profiles_univ()
    prof_by = {u["code"]: u for u in uprof["universities"]}
    for cq in uprof["common_questions"]:
        cq["answer_html"] = ph(cq["answer"])
    for u in uprof["universities"]:
        for q in u["questions"]:
            q["answer_html"] = ph(q["answer"])
    prepped = {c for c in prof_by if c not in with_data}
    # 분교·캠퍼스 코드(also) 는 본교 프로필 페이지로 연결
    prep_link = {c: f"/univ/{c}/" for c in prof_by}
    for u in uprof["universities"]:
        for a in u.get("also", []):
            prep_link.setdefault(a, u["url"])

    newd = load_new_departments()
    dept_by = {d["slug"]: d for d in depts}

    # rich 데이터 (학과·대학 2027 보강, 완성 예시)
    rich_dept, rich_univ, examples = load_rich("dept"), load_rich("univ"), load_examples()
    all_dept_url = {d["slug"]: (d["url"], d["label"]) for d in depts}
    all_dept_url.update({d["slug"]: (d["url"], d["label"]) for d in newd["departments"]})
    for d in depts + newd["departments"]:
        r = rich_dept.get(d["slug"])
        if r:
            for row in ((r.get("y2027") or {}).get("rows") or []):
                row["url"] = prep_link.get(row.get("code") or "", "")
            d["rich"] = r
    for code, r in rich_univ.items():
        if code in prof_by:
            r["dept_links"] = [{"url": all_dept_url[x["slug"]][0], "label": all_dept_url[x["slug"]][1]}
                               for x in r.get("depts", []) if x.get("slug") in all_dept_url]
            prof_by[code]["rich"] = r
    # 면접 일정: 트랙별 면접일·1단계 발표일을 뽑아 '같은 날 면접 대학'·내 면접 일정표에 쓴다
    WD = "월화수목금토일"
    dlabel = lambda iso: f"{int(iso[5:7])}/{int(iso[8:])}({WD[datetime.date.fromisoformat(iso).weekday()]})"
    SHORT = {"한국외국어대학교": "한국외대", "서울과학기술대학교": "서울과기대", "한국기술교육대학교": "한국기술교육대"}
    short = lambda n: SHORT.get(n) or re.sub("대학교", "대", re.sub("교육대학교", "교대", re.sub("여자대학교", "여대", n)))
    planner, by_day = [], {}
    for code, r in sorted(rich_univ.items(), key=lambda kv: kv[1].get("name", "")):
        if code not in prof_by:
            continue
        tr = []
        for i, t in enumerate(r.get("tracks", [])):
            days = [x for x in datesparse.parse(t.get("date")) if x >= TODAY.isoformat()]
            if not days:
                continue
            f = datesparse.first(t.get("first"))
            tr.append({"id": f"{code}:{i}", "n": t["name"], "d": days, "dt": t.get("date", ""), "f": f, "ft": t.get("first", "")})
            for x in days:
                by_day.setdefault(x, {}).setdefault(code, []).append(t["name"])
        if tr:
            planner.append({"c": code, "u": prof_by[code]["url"], "n": short(r.get("name") or prof_by[code]["name"]), "t": tr})
    for code, r in rich_univ.items():
        if code not in prof_by:
            continue
        mine = sorted({x for t in r.get("tracks", []) for x in datesparse.parse(t.get("date")) if x >= TODAY.isoformat()})
        r["same_day"] = [{"label": dlabel(x), "univs": [{"name": short(rich_univ[c].get("name") or prof_by[c]["name"]), "url": prof_by[c]["url"]}
                                                       for c in sorted(by_day[x], key=lambda c: rich_univ[c].get("name", "")) if c != code]}
                         for x in mine]
        r["same_day"] = [g for g in r["same_day"] if g["univs"]]
        pr = []
        if r.get("published_questions") and code not in RESTRICTED:
            pr.append({"set": f"univ:{code}", "label": f"{short(r.get('name', code))} 공개 질문"})
        pr += [{"set": f"dept:{x['slug']}", "label": all_dept_url[x["slug"]][1]} for x in r.get("depts", []) if x.get("slug") in all_dept_url][:5]
        pr.append({"set": "common", "label": "자주 나오는 공통"})
        r["practice"] = pr
    rich_common = load_rich("common")
    for q in common["questions"]:
        q["example"] = examples.get("common", {}).get(q["slug"])
        rc = rich_common.get(q["slug"])
        if rc:
            for ex in rc.get("univ_examples", []):
                ex["url"] = prof_by[ex["code"]]["url"] if ex.get("code") in prof_by else ""
        q["rich"] = rc
    for m in majors["majors"]:
        exs = examples.get("majors", {}).get(m["code"], [])
        for i, q in enumerate(m["questions"]):
            q["example"] = exs[i] if i < len(exs) else None
    for p_ in profiles:
        for q in p_["seed_questions"]:
            q["example"] = examples.get("types", {}).get(q["id"])

    # 홈
    n_videos = sum(len(d.get("videos", [])) for d in depts) + sum(len(d.get("videos", [])) for d in newd["departments"]) + sum(len(u.get("videos", [])) for u in uprof["universities"])
    stats = {"questions": len(common["questions"]), "depts": len(depts) + len(newd["departments"]), "univs": sum(1 for p in prof_by.values() if p.get("rich")), "actual": sum(len(v) for c, v in actual_by.items() if c not in RESTRICTED),
             "videos": n_videos, "updated": TODAY.strftime("%Y.%m.%d")}
    page("", "home.html", common=common, by_cat=by_cat, majors=majors["majors"], profiles=profiles, univ_cards=univ_cards, stats=stats,
         depts=depts, newd=newd["departments"], prep_n=len(prof_by), top=common["questions"][:8], description=site["description"])
    urls.append("/")

    # 신설학과
    tag_order = []
    for d in newd["departments"]:
        if d["tag"] not in tag_order:
            tag_order.append(d["tag"])
    tags = [{"label": tg, "list": [d for d in newd["departments"] if d["tag"] == tg]} for tg in tag_order]
    page("new", "new_index.html", intro=newd["intro"], notice=newd["notice"], tags=tags,
         title=f"신설학과 면접 질문과 답변 {len(newd['departments'])}개 학과", description="반도체·배터리·양자·AI·K-POP·e스포츠·웹툰·반려동물·자유전공 등 새로 생긴 학과의 소개, 개설 대학, 선발 방식, 면접 질문 6개와 답변 예시.")
    urls.append("/new/")
    for d in newd["departments"]:
        for q in d["questions"]:
            q["answer_html"] = ph(q["answer"])
        qa = d["rich"]["questions"] if d.get("rich") else d["questions"]
        page(f"new/{d['slug']}", "new_dept.html", d=d, siblings=newd["departments"], notice=newd["notice"], og_custom=True,
             related=[dept_by[s] for s in d.get("related", []) if s in dept_by],
             jsonld=jsonld_faq(f"{d['label']} 면접 질문과 답변", d["summary"], d["url"], qa),
             title=f"{d['label']} 면접 질문 {len(d['questions'])}개와 답변 · 개설 대학", description=f"{d['summary']} 왜 생겼는지, 어디서 뽑는지, 어떻게 뽑는지와 면접 질문·답변 예시.")
        urls.append(d["url"])
        rss.append((f"{d['label']} 면접 질문과 답변 (신설학과)", d["url"], d["summary"]))

    # 학과별
    page("dept", "dept_index.html", groups=[m for m in majors["majors"] if m["depts"]], total=sum(len(d["questions"]) for d in depts),
         title=f"학과별 면접 질문과 답변 {len(depts)}개 학과", description="국문·영문·심리·경영·컴퓨터·기계·의예·간호·교육·디자인 등 학과별로 반복되는 면접 질문과 표준 답변.")
    urls.append("/dept/")
    for d in depts:
        for q in d["questions"]:
            q["answer_html"] = ph(q["answer"])
        g = major_by[d["group"]]
        r = d.get("rich")
        qa = r["questions"] if r else d["questions"]
        y_univs = [re.sub("대학교$", "대", re.sub("교육대학교$", "교대", re.sub("여자대학교$", "여대", x["univ"]))) for x in ((r or {}).get("y2027") or {}).get("rows", [])][:4] if r else []
        title = (f"{d['label']} 면접 질문 {len(qa)}개와 답변 예시 · 2027 " + "·".join(dict.fromkeys(y_univs)) + " 면접 방식") if y_univs \
            else (f"{d['label']} 면접 질문 {len(qa)}개와 답변 예시" if r else f"{d['label']} 면접 질문 {len(qa)}개와 답변")
        desc = (r["hook"][:110] + " 2027 대학별 면접 방식과 완성 답변 예시.") if r else f"{d['desc']} 자주 나오는 질문과 표준 답변, 준비 팁."
        page(f"dept/{d['slug']}", "dept.html", d=d, group=g, siblings=g["depts"], notice=majors["notice"],
             related=related_by_keywords(tokens(d["label"] + " " + d["desc"]), actual_by, univ_names),
             jsonld=jsonld_faq(f"{d['label']} 면접 질문과 답변", d["desc"], d["url"], qa),
             title=title, description=desc)
        urls.append(d["url"])
        rss.append((f"{d['label']} 면접 질문과 답변", d["url"], d["desc"]))

    # 공통 질문 상세
    qs = common["questions"]
    for i, q in enumerate(qs):
        prev_q = qs[i - 1] if i > 0 else None
        next_q = qs[i + 1] if i + 1 < len(qs) else None
        same_cat = [r for r in by_cat[q["category"]] if r["slug"] != q["slug"]][:6]
        page(f"q/{q['slug']}", "question.html", q=q, cat=common["categories"][q["category"]], notice=common["notice"],
             answer_html=ph(q["answer"]), related=related_actual(q, actual_by, univ_names), same_cat=same_cat,
             prev_q=prev_q, next_q=next_q, jsonld=jsonld_question(q), profiles=profiles,
             title=q["question"], description=f"{q['why']} 표준 답변과 답변 구조, 피해야 할 표현을 정리했습니다.")
        urls.append(q["url"])
        rss.append((q["question"], q["url"], q["why"]))

    # 카테고리
    cat_guide = load(RICH / "category.json") if (RICH / "category.json").exists() else {}
    q_by_slug = {q["slug"]: q for q in common["questions"]}
    for k, meta in common["categories"].items():
        g = cat_guide.get(k) or {}
        page(f"category/{k}", "category.html", cat=meta, key=k, questions=by_cat[k], categories=common["categories"],
             guide=g.get("guide", []), first=[q_by_slug[x] for x in g.get("first", []) if x in q_by_slug],
             title=f"{meta['label']} 면접 질문 {len(by_cat[k])}개", description=meta["desc"])
        urls.append(meta["url"])

    # 계열
    for m in majors["majors"]:
        for q in m["questions"]:
            q["answer_html"] = ph(q["answer"])
        page(f"major/{m['code']}", "major.html", m=m, majors=majors["majors"], notice=majors["notice"],
             title=f"{m['label']} 계열 면접 질문과 답변", description=f"{m['desc']} 자주 나오는 질문 {len(m['questions'])}개와 표준 답변.")
        urls.append(m["url"])

    # 유형
    for p in profiles:
        for q in p["seed_questions"]:
            q["answer_html"] = ph(q["answer"]) if q.get("answer") else None
        page(f"type/{p['code'].lower()}", "type.html", p=p, profiles=profiles,
             title=f"{p['label']} 면접 질문 {len(p['seed_questions'])}개와 답변 전략",
             description=p["description"])
        urls.append(p["url"])

    # 대학 목록: content/universities.json(지역별 수동 목록) + seed 에만 있는 대학 합치기, 보고서 링크 붙이기
    REGION_MAP = {"서울": "서울", "경기": "경기·인천", "인천": "경기·인천", "대전": "대전·충청·강원", "충남": "대전·충청·강원", "충북": "대전·충청·강원",
                  "강원": "대전·충청·강원", "세종": "대전·충청·강원", "대구": "대구·경북", "경북": "대구·경북", "부산": "부산·울산·경남", "울산": "부산·울산·경남",
                  "경남": "부산·울산·경남", "광주": "광주·전라·제주", "전북": "광주·전라·제주", "전남": "광주·전라·제주", "제주": "광주·전라·제주"}
    listed = {u["code"] for r in unis["regions"] for u in r["universities"]}
    for code, su in seed.items():
        reports = [s_ for s_ in su.get("sources", []) if s_.get("kind") == "report"]
        if code not in listed and reports:
            rname = REGION_MAP.get(su.get("region", ""), "기타")
            reg = next((r for r in unis["regions"] if r["name"] == rname), None)
            if reg is None:
                reg = {"name": rname, "universities": []}
                unis["regions"].append(reg)
            reg["universities"].append({"code": code, "name": su["name"], "url": su["admission_url"]})
    for r in unis["regions"]:
        for u in r["universities"]:
            su = seed.get(u["code"])
            reports = sorted([s_ for s_ in (su or {}).get("sources", []) if s_.get("kind") == "report"], key=lambda x: -x["year"])
            if reports:
                u["report_url"] = reports[0]["url"]
                u["report_year"] = reports[0]["year"]
        r["universities"].sort(key=lambda u: (u["code"] not in with_data, u["code"] not in prep_link, u["name"]))
    prep_cards = [{"code": u["code"], "name": u["name"], "blurb": u["blurb"], "url": u["url"], "has_data": u["code"] in with_data} for u in uprof["universities"]]
    page("univ", "univ_index.html", regions=unis["regions"], notice=unis["notice"], colleges=unis.get("colleges", []), college_notice=unis.get("college_notice", ""), with_data=set(with_data), prep_link=prep_link, prep_cards=prep_cards, univ_cards=univ_cards, n_univ=sum(len(r["universities"]) for r in unis["regions"]), n_college=sum(len(r["universities"]) for r in unis.get("colleges", [])),
         title="전국 대학·전문대 면접 안내·준비 가이드·기출 공개 대학", description=f"주요 대학 {len(prep_cards)}곳의 특성·면접 방식·맞춤 예상 질문, 전국 4년제·전문대 홈페이지·보고서 링크, 실제 면접 문항을 공개한 대학의 기출 정리.")
    urls.append("/univ/")

    # 기출 없는 대학의 준비 가이드 페이지
    for code in sorted(prepped):
        p = prof_by[code]
        s = seed.get(code, {})
        reports = sorted([s_ for s_ in s.get("sources", []) if s_.get("kind") == "report"], key=lambda x: -x["year"])
        page(f"univ/{code}", "univ_prep.html", p=p, home=p.get("home") or s.get("admission_url", "#"),
             report_url=reports[0]["url"] if reports else None, report_year=reports[0]["year"] if reports else None,
             common_questions=uprof["common_questions"], notice=uprof["notice"],
             robots=None if p.get("rich") else "noindex,follow",  # 2027 정보 없는 템플릿 페이지는 색인 제외 (얇은 콘텐츠)
             title=(f"{p['name']} 면접 2027 — 전형별 면접 방식·일정·공개 질문" if p.get("rich") else f"{p['name']} 면접 준비 가이드 — 특징·면접 방식·예상 질문"),
             description=(p["rich"]["summary"][:150] if p.get("rich") else f"{p['blurb']} 면접 방식과 준비 포인트, 맞춤 예상 질문 {len(p['questions'])}개."))
        if p.get("rich"):
            urls.append(p["url"])
            rss.append((f"{p['name']} 면접 2027", p["url"], p["rich"]["summary"][:120]))
    for u in univ_cards:
        recs = actual_by[u["code"]]
        s = seed[u["code"]]
        # 전형 요약
        adm: dict[str, dict] = {}
        for r in recs:
            a = adm.setdefault(r["admission_name"], {"name": r["admission_name"], "category": CATEGORY_LABEL.get(r["category"], r["category"]), "n": 0, "years": set()})
            a["n"] += 1
            a["years"].add(r["year"])
        for a in adm.values():
            a["years"] = sorted(a["years"], reverse=True)
        years = u["years"]
        restricted = RESTRICTED.get(u["code"])
        year_src = {}
        for r in recs:
            year_src.setdefault(r["year"], {})
            year_src[r["year"]].setdefault(r["admission_name"], r.get("source_url") or "")
        rich_p = (prof_by.get(u["code"]) or {}).get("rich")
        if restricted:
            title_u = (f"{u['name']} 면접 2027 — 전형별 면접 방식·일정 · 기출 공개 현황" if rich_p else f"{u['name']} 면접 기출 공개 현황 {years[-1]}~{years[0]}학년도")
            desc_u = f"{u['name']} 입학처가 공개한 면접·구술고사 문항의 학년도·전형별 현황과 원문 링크. 대학의 이용 조건에 따라 문항 원문은 이 사이트에 싣지 않습니다."
        else:
            title_u = (f"{u['name']} 면접 2027 — 전형별 면접 방식·일정 · 기출문항 {years[0]}학년도" if rich_p else f"{u['name']} 면접 기출문항 {years[-1]}~{years[0]}학년도")
            desc_u = f"{u['name']} 입학처가 공개한 면접·구술고사 문항 {u['n']}개를 연도·전형별로 정리했습니다. 출제 의도와 출처 링크 포함."
        page(f"univ/{u['code']}", "univ.html", u=u, seed=s, years=years, admissions=list(adm.values()), sample=([] if restricted else [r for r in recs if r["year"] == years[0]][:6]),
             restricted=restricted, year_src=year_src,
             robots=("noindex,follow" if (restricted and not rich_p) else None),
             p=prof_by.get(u["code"]), kind_label=KIND_LABEL,
             title=title_u, description=desc_u)
        if not (restricted and not rich_p):
            urls.append(u["url"])
        for y in ([] if restricted else years):
            yr = [r for r in recs if r["year"] == y]
            by_adm: dict[str, list] = {}
            for r in yr:
                by_adm.setdefault(r["admission_name"], []).append(r)
            page(f"univ/{u['code']}/{y}", "univ_year.html", u=u, seed=s, y=y, years=years, by_adm=by_adm, kind_label=KIND_LABEL,
                 title=f"{u['name']} {y}학년도 면접 기출문항 {len(yr)}개",
                 description=f"{u['name']} {y}학년도 면접·구술고사 공개 문항 {len(yr)}개. 제시문·출제 의도 요약과 입학처 출처 링크.")
            urls.append(f"/univ/{u['code']}/{y}/")

    # 모의 면접
    sets = [{"id": "common", "label": "자주 나오는 공통 질문",
             "items": [{"q": q["question"], "ex": q.get("example") or "", "tip": q.get("tips", ""), "u": q["url"]} for q in common["questions"]]}]
    for d in depts + newd["departments"]:
        r = d.get("rich")
        qa = r["questions"] if r else d["questions"]
        sets.append({"id": f"dept:{d['slug']}", "label": f"학과 · {d['label']}",
                     "items": [{"q": q["question"], "ex": q.get("example") or "", "tip": q.get("caution") or q.get("tips", ""), "u": d["url"]} for q in qa]})
    for code, r in sorted(rich_univ.items(), key=lambda kv: kv[1].get("name", "")):
        if r.get("published_questions") and code in prof_by:
            sets.append({"id": f"univ:{code}", "label": f"대학 공개 질문 · {r.get('name', code)}",
                         "items": [{"q": q["q"], "ex": "", "tip": q.get("area", ""), "u": prof_by[code]["url"]} for q in r["published_questions"]]})
    write("practice/questions.json", json.dumps({"sets": sets}, ensure_ascii=False))
    page("practice", "practice.html", title="모의 면접 연습 — 무작위 질문·60초 타이머·녹음",
         description="학과별·공통·대학 공개 면접 질문을 무작위로 뽑아 생각 15초, 답변 60초로 연습합니다. 녹음은 내 기기 안에서만 재생되고 서버로 보내지 않습니다.")
    urls.append("/practice/")

    # 수능최저 모아보기: 면접 있는 전형 중 수능최저학력기준이 있는 것만
    minrows = []
    for code, r in sorted(rich_univ.items(), key=lambda kv: kv[1].get("name", "")):
        if code not in prof_by:
            continue
        for t in r.get("tracks", []):
            v = (t.get("min") or "").strip()
            if not v or v.startswith("없음") or v in ("미적용", "-"):
                continue
            minrows.append({"code": code, "name": short(r.get("name") or prof_by[code]["name"]), "url": prof_by[code]["url"],
                            "track": t["name"], "min": v, "date": t.get("date", ""), "first": t.get("first", ""), "source": t.get("source", "")})
    page("minimum", "minimum.html", rows=minrows, n_univ=len({x["code"] for x in minrows}), checked_n=len(prof_by),
         title=f"2027 수시 수능최저 모아보기 — 면접 전형 {len(minrows)}개",
         description=f"면접이 있는 2027학년도 수시 전형 중 수능최저학력기준이 있는 {len(minrows)}개 전형을 대학별로 모았습니다. 수능 가채점 뒤 최저 충족 여부를 확인하고, 면접 준비 순서를 정하는 데 쓰세요.")
    urls.append("/minimum/")

    # 수능 정보 페이지: 수능 뒤 날짜별 면접 대학(내 면접 일정표와 같은 데이터)
    after = []
    for x in sorted(by_day):
        if "2026-11-20" <= x <= "2026-12-17":  # 수능 다음 날 ~ 수시 전형기간 끝
            us = [short(rich_univ[c].get("name") or prof_by[c]["name"]) for c in sorted(by_day[x], key=lambda c: rich_univ[c].get("name", ""))]
            after.append({"label": dlabel(x), "univs": us})
    page("suneung", "suneung.html", after=after,
         title="2027 수능 D-day와 꼭 알아야 할 것 — 시간표·준비물·가채점·성적 통지·대입 일정",
         description="2027학년도 수능(2026년 11월 19일) 시간표, 반입 금지 물품과 준비물, 4교시 탐구 주의사항, 수험표 뒷면 가채점표, 정답 확정·성적 통지일, 수능 뒤 면접 대학과 정시 일정을 평가원·교육부·대교협 공식 자료로 정리했습니다.")
    urls.append("/suneung/")

    # 내 면접 일정표
    write("planner/data.json", json.dumps({"today": TODAY.isoformat(), "csat": "2026-11-19", "events": [m for m in site.get("milestones", []) if m["date"] != "2026-11-19"], "univs": planner}, ensure_ascii=False))
    page("planner", "planner.html", n_univ=len(planner), n_track=sum(len(u["t"]) for u in planner),
         title="내 면접 일정표 — 지원한 대학의 1단계 발표일·면접일 한눈에",
         description=f"지원한 대학과 전형을 고르면 1단계 발표일과 면접일을 날짜순으로 보여 주고, 같은 날 겹치는 면접을 표시합니다. {len(planner)}개 대학 2027학년도 수시모집요강 기준.")
    urls.append("/planner/")

    # 고정 페이지
    for name in ("guide", "schedule", "about", "privacy", "contact"):
        meta, body = md_page(name)
        page(name, "page.html", body=body, title=meta["title"], description=meta.get("description", ""))
        urls.append(f"/{name}/")

    # 404, robots, sitemap, rss, search
    write("404.html", env.get_template("404.html").render(site=site, year=TODAY.year, title="페이지를 찾을 수 없습니다", description="", path="/404"))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {site['url']}/sitemap.xml\n")
    write_sitemap(urls)
    write_rss(rss)
    search = [{"t": q["question"], "u": q["url"], "c": q["cat_label"]} for q in common["questions"]]
    search += [{"t": f"{m['label']} · {q['question']}", "u": m["url"], "c": "계열별"} for m in majors["majors"] for q in m["questions"]]
    search += [{"t": f"{p['label']} · {q['text']}", "u": p["url"], "c": "유형별"} for p in profiles for q in p["seed_questions"]]
    search += [{"t": f"{d['label']} · {q['question']}", "u": d["url"], "c": "학과별"} for d in depts for q in (d["rich"]["questions"] if d.get("rich") else d["questions"])]
    search += [{"t": "모의 면접 연습 (무작위 질문·타이머·녹음)", "u": "/practice/", "c": "도구", "p": 1}]
    search += [{"t": "내 면접 일정표 (1단계 발표일·면접일·겹침 확인)", "u": "/planner/", "c": "도구", "p": 1}]
    search += [{"t": "수능최저 모아보기 (면접 있는 전형)", "u": "/minimum/", "c": "도구", "p": 1}]
    search += [{"t": "2027 수능 D-day·시간표·준비물·성적 통지일", "u": "/suneung/", "c": "수능", "p": 1}]
    search += [{"t": f"{d['label']} · {q['question']}", "u": d["url"], "c": "신설학과"} for d in newd["departments"] for q in d["questions"]]
    search += [{"t": f"{d['label']} (신설학과)", "u": d["url"], "c": "신설학과"} for d in newd["departments"]]
    search += [{"t": f"{u['name']} · {q['question']}", "u": u["url"], "c": "대학별"} for u in uprof["universities"] for q in u["questions"]]
    search += [{"t": f"{u['name']} 면접 준비 가이드", "u": u["url"], "c": "대학별"} for u in uprof["universities"]]
    # 전국 4년제·전문대 전체 (가이드·기출이 있으면 그 페이지로, 없으면 대학 목록의 해당 줄로)
    for r in unis["regions"]:
        for u in r["universities"]:
            if u["code"] in with_data:
                link, lab = f"/univ/{u['code']}/", "대학 · 면접 기출 + 가이드"
            elif u["code"] in prep_link:
                link, lab = prep_link[u["code"]], "대학 · 면접 준비 가이드"
            else:
                link, lab = f"/univ/#u-{u['code']}", f"대학 · {r['name']} · 홈페이지 링크"
            search.append({"t": u["name"], "u": link, "c": lab, "p": 1, "a": univ_aliases(u["name"])})
    for r in unis.get("colleges", []):
        for u in r["universities"]:
            search.append({"t": u["name"], "u": f"/univ/#c-{u['code']}", "c": f"전문대 · {r['name']} · 홈페이지 링크", "p": 1, "a": univ_aliases(u["name"])})
    search += [{"t": d["label"], "u": d["url"], "c": "학과 · 면접 질문과 답변", "p": 1} for d in depts]
    search += [{"t": d["label"], "u": d["url"], "c": "신설학과 · 소개와 면접 질문", "p": 1} for d in newd["departments"]]
    search += [{"t": f"{m['label']} 계열", "u": m["url"], "c": "계열별 질문", "p": 1} for m in majors["majors"]]
    search += [{"t": f"{c['label']} 질문 {c['n']}개", "u": c["url"], "c": "자주 나오는 질문", "p": 1} for c in common["categories"].values()]
    search += [{"t": f"{pf['label']} 지원자", "u": pf["url"], "c": "유형별 질문", "p": 1} for pf in profiles]
    write("search.json", json.dumps(search, ensure_ascii=False))
    print(f"pages: {len(urls)}  questions: {len(common['questions'])}  depts: {len(depts)}  new: {len(newd['departments'])}  univ profiles: {len(prof_by)}  actual: {sum(len(v) for v in actual_by.values())}  -> {DIST}")


if __name__ == "__main__":
    main()
