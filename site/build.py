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

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DIST = ROOT / "dist"
TODAY = datetime.date.today()

site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=False)

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
            by.setdefault(r["university_code"], []).append(r)
    return by


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
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\[([^\]]+)\]", r"(\1)", q["answer"])}} for q in qa]
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc,
         "author": {"@type": "Person", "name": site["author"], "url": f"{site['url']}/about/"},
         "publisher": {"@type": "Organization", "name": site["name"], "url": site["url"]},
         "datePublished": site["publish_date"], "dateModified": site["publish_date"], "mainEntityOfPage": url},
        {"@type": "FAQPage", "mainEntity": ents}]}, ensure_ascii=False)


def related_by_keywords(kw: set[str], actual_by, univ_names, limit=3):
    scored = []
    for code, recs in actual_by.items():
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
        L.append(f"  <url><loc>{site['url']}{u}</loc><lastmod>{site['publish_date']}</lastmod></url>")
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
        shutil.rmtree(DIST)
    DIST.mkdir()
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

    # 홈
    page("", "home.html", common=common, by_cat=by_cat, majors=majors["majors"], profiles=profiles, univ_cards=univ_cards,
         depts=depts, prep_n=len(prof_by), top=common["questions"][:8], description=site["description"])
    urls.append("/")

    # 학과별
    page("dept", "dept_index.html", groups=[m for m in majors["majors"] if m["depts"]], total=sum(len(d["questions"]) for d in depts),
         title=f"학과별 면접 질문과 답변 {len(depts)}개 학과", description="국문·영문·심리·경영·컴퓨터·기계·의예·간호·교육·디자인 등 학과별로 반복되는 면접 질문과 표준 답변.")
    urls.append("/dept/")
    for d in depts:
        for q in d["questions"]:
            q["answer_html"] = ph(q["answer"])
        g = major_by[d["group"]]
        page(f"dept/{d['slug']}", "dept.html", d=d, group=g, siblings=g["depts"], notice=majors["notice"],
             related=related_by_keywords(tokens(d["label"] + " " + d["desc"]), actual_by, univ_names),
             jsonld=jsonld_faq(f"{d['label']} 면접 질문과 답변", d["desc"], d["url"], d["questions"]),
             title=f"{d['label']} 면접 질문 {len(d['questions'])}개와 답변", description=f"{d['desc']} 자주 나오는 질문과 표준 답변, 준비 팁.")
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
    for k, meta in common["categories"].items():
        page(f"category/{k}", "category.html", cat=meta, key=k, questions=by_cat[k], categories=common["categories"],
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
    page("univ", "univ_index.html", regions=unis["regions"], notice=unis["notice"], with_data=set(with_data), prep_link=prep_link, prep_cards=prep_cards, univ_cards=univ_cards,
         title="전국 대학 면접 안내·준비 가이드·기출 공개 대학", description=f"주요 대학 {len(prep_cards)}곳의 특성·면접 방식·맞춤 예상 질문, 전국 대학 홈페이지·보고서 링크, 실제 면접 문항을 공개한 대학의 기출 정리.")
    urls.append("/univ/")

    # 기출 없는 대학의 준비 가이드 페이지
    for code in sorted(prepped):
        p = prof_by[code]
        s = seed.get(code, {})
        reports = sorted([s_ for s_ in s.get("sources", []) if s_.get("kind") == "report"], key=lambda x: -x["year"])
        page(f"univ/{code}", "univ_prep.html", p=p, home=p.get("home") or s.get("admission_url", "#"),
             report_url=reports[0]["url"] if reports else None, report_year=reports[0]["year"] if reports else None,
             common_questions=uprof["common_questions"], notice=uprof["notice"],
             title=f"{p['name']} 면접 준비 가이드 — 특징·면접 방식·예상 질문", description=f"{p['blurb']} 면접 방식과 준비 포인트, 맞춤 예상 질문 {len(p['questions'])}개.")
        urls.append(p["url"])
        rss.append((f"{p['name']} 면접 준비 가이드", p["url"], p["blurb"]))
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
        page(f"univ/{u['code']}", "univ.html", u=u, seed=s, years=years, admissions=list(adm.values()), sample=[r for r in recs if r["year"] == years[0]][:6],
             p=prof_by.get(u["code"]), kind_label=KIND_LABEL, title=f"{u['name']} 면접 기출문항 {years[-1]}~{years[0]}학년도",
             description=f"{u['name']} 입학처가 공개한 면접·구술고사 문항 {u['n']}개를 연도·전형별로 정리했습니다. 출제 의도와 출처 링크 포함.")
        urls.append(u["url"])
        for y in years:
            yr = [r for r in recs if r["year"] == y]
            by_adm: dict[str, list] = {}
            for r in yr:
                by_adm.setdefault(r["admission_name"], []).append(r)
            page(f"univ/{u['code']}/{y}", "univ_year.html", u=u, seed=s, y=y, years=years, by_adm=by_adm, kind_label=KIND_LABEL,
                 title=f"{u['name']} {y}학년도 면접 기출문항 {len(yr)}개",
                 description=f"{u['name']} {y}학년도 면접·구술고사 공개 문항 {len(yr)}개. 제시문·출제 의도 요약과 입학처 출처 링크.")
            urls.append(f"/univ/{u['code']}/{y}/")

    # 고정 페이지
    for name in ("guide", "about", "privacy", "contact"):
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
    search += [{"t": f"{d['label']} · {q['question']}", "u": d["url"], "c": "학과별"} for d in depts for q in d["questions"]]
    search += [{"t": f"{u['name']} · {q['question']}", "u": u["url"], "c": "대학별"} for u in uprof["universities"] for q in u["questions"]]
    search += [{"t": f"{u['name']} 면접 준비 가이드", "u": u["url"], "c": "대학별"} for u in uprof["universities"]]
    write("search.json", json.dumps(search, ensure_ascii=False))
    print(f"pages: {len(urls)}  questions: {len(common['questions'])}  depts: {len(depts)}  univ profiles: {len(prof_by)}  actual: {sum(len(v) for v in actual_by.values())}  -> {DIST}")


if __name__ == "__main__":
    main()
