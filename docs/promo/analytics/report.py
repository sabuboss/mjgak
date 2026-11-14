"""GA4·서치콘솔 숫자를 브라우저 로그인 없이 API 로 읽어 유입 리포트를 만든다(둘 다 무료 API).

준비(한 번만): docs/promo/analytics/SETUP.md
  python report.py                 # 지난 7일 vs 그 전 7일 → 화면 출력 + ../weekly/<오늘>-api.md
  python report.py --days 2        # 최근 2일
  python report.py --check         # 열쇠·권한만 확인

열쇠 파일: docs/promo/.secrets/ga-reader.json (서비스 계정, git 에 안 올라감). 읽기 전용 권한만 준다.
"""
import argparse, datetime, os, re, ssl, sys, tempfile, time, warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent


def trust_windows_roots():
    """회사망은 TLS 를 중간에서 다시 서명하므로, 검증은 그대로 두고 윈도우가 신뢰하는 루트 인증서를 기본 목록에 더한다."""
    if os.name != "nt":
        return
    import certifi
    pems = [Path(certifi.where()).read_text(encoding="ascii", errors="ignore")]
    for store in ("ROOT", "CA"):
        for der, enc, _ in ssl.enum_certificates(store):
            if enc == "x509_asn":
                pems.append(ssl.DER_cert_to_PEM_cert(der))
    f = Path(tempfile.gettempdir()) / "mjgak-ca-bundle.pem"
    f.write_text("\n".join(pems), encoding="ascii")
    for k in ("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH", "REQUESTS_CA_BUNDLE", "HTTPLIB2_CA_CERTS", "SSL_CERT_FILE"):
        os.environ.setdefault(k, str(f))


trust_windows_roots()
KEY = HERE.parent / ".secrets" / "ga-reader.json"
PROPERTY = "properties/556489763"
SC_SITE = "https://mjgak.com/"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly", "https://www.googleapis.com/auth/webmasters.readonly"]


def creds():
    from google.oauth2 import service_account
    if not KEY.exists():
        sys.exit(f"열쇠 파일이 없습니다: {KEY}\n→ docs/promo/analytics/SETUP.md 를 따라 한 번만 준비하세요.")
    return service_account.Credentials.from_service_account_file(str(KEY), scopes=SCOPES)


def ga(c, start, end, dims, mets, limit=25, filt=None, order=None):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (DateRange, Dimension, Filter, FilterExpression, Metric,
                                                    OrderBy, RunReportRequest)
    cl = BetaAnalyticsDataClient(credentials=c, transport="rest")  # 회사 프록시가 gRPC(HTTP/2)를 막아 REST 로
    req = RunReportRequest(property=PROPERTY, date_ranges=[DateRange(start_date=start, end_date=end)],
                           dimensions=[Dimension(name=d) for d in dims], metrics=[Metric(name=m) for m in mets], limit=limit,
                           order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order or mets[0]), desc=True)])
    if filt:
        name, val = filt
        if isinstance(val, (list, tuple)):  # 목록 중 하나와 정확히 일치(이벤트 여러 개를 한 사람 기준으로 셀 때)
            req.dimension_filter = FilterExpression(filter=Filter(field_name=name, in_list_filter=Filter.InListFilter(values=list(val))))
        else:
            req.dimension_filter = FilterExpression(filter=Filter(field_name=name, string_filter=Filter.StringFilter(
                value=val, match_type=Filter.StringFilter.MatchType.CONTAINS)))
    for k in range(4):  # 하루·시간 할당량(429)이나 회사망 연결 끊김은 잠깐 쉬고 다시
        try:
            res = cl.run_report(req)
            break
        except Exception:
            if k == 3:
                raise
            time.sleep(20 * (k + 1))
    return [[v.value for v in r.dimension_values] + [v.value for v in r.metric_values] for r in res.rows]


def sc(c, start, end, dims, limit=25):
    from googleapiclient.discovery import build
    s = build("searchconsole", "v1", credentials=c, cache_discovery=False)
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit}
    return s.searchanalytics().query(siteUrl=SC_SITE, body=body).execute().get("rows", [])


def post_titles():
    """utm_campaign 'post-118' → 블로그 글 제목(docs/promo/naver-118-*.md 의 '제목:' 줄). 글은 번호가 아니라 제목으로 부른다."""
    out = {}
    for f in sorted(HERE.parent.glob("naver-*.md")):
        m = re.match(r"naver-(\d+)-", f.name)
        if not m:
            continue
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines()[:15]:
            if line.startswith("제목:"):
                out["post-" + m.group(1)] = line[3:].strip().split(" (")[0][:60]
                break
    return out


def sec(x):
    x = float(x)
    return f"{int(x // 60)}분 {int(x % 60):02d}초" if x >= 60 else f"{int(x)}초"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    c = creds()
    today = datetime.date.today()
    end = today - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=a.days - 1)
    pstart, pend = start - datetime.timedelta(days=a.days), start - datetime.timedelta(days=1)
    S, E, PS, PE = (d.isoformat() for d in (start, end, pstart, pend))
    if a.check:
        print("GA4:", ga(c, S, E, [], ["sessions"])[0][0], "세션 OK")
        print("서치콘솔:", sum(r["clicks"] for r in sc(c, S, E, ["date"])), "클릭 OK")
        return
    L = [f"# 면접각 유입 리포트(API) — {today.isoformat()}", "", f"기간 {S}~{E} ({a.days}일), 비교 {PS}~{PE}. 서치콘솔은 2~3일 늦게 채워진다.", ""]
    now = {r[0]: r for r in ga(c, S, E, ["sessionSourceMedium"], ["sessions", "engagedSessions", "averageSessionDuration"], 15)}
    prev = {r[0]: r for r in ga(c, PS, PE, ["sessionSourceMedium"], ["sessions"], 30)}
    tot = sum(int(r[1]) for r in now.values()); ptot = sum(int(r[1]) for r in prev.values())
    L += ["## 0. 하루 세션", ""]
    L.append(table(["날짜", "세션", "참여 세션", "사용자"], [[f"{r[0][4:6]}/{r[0][6:]}", r[1], r[2], r[3]] for r in
                   sorted(ga(c, S, E, ["date"], ["sessions", "engagedSessions", "activeUsers"], 31), key=lambda r: r[0])]))
    L += ["", "## 1. 어디서 왔나", f"세션 {tot} (전 기간 {ptot})", ""]
    L.append(table(["출처/매체", "세션", "전", "참여 세션", "평균 체류"],
                   [[k, r[1], prev.get(k, [0, 0])[1], r[2], sec(r[3])] for k, r in now.items()]))
    L += ["", "## 1-2. 검색엔진별(자연 검색) — 구글·네이버 검색·Bing 비교", ""]
    se_now = {r[0]: r[1] for r in ga(c, S, E, ["sessionSource"], ["sessions"], 15, ("sessionMedium", "organic"))}
    se_prev = {r[0]: r[1] for r in ga(c, PS, PE, ["sessionSource"], ["sessions"], 15, ("sessionMedium", "organic"))}
    # 블로그 링크 일부가 utm_medium=organic 으로 잡혀 들어오는 것(naver_blog)은 검색엔진이 아니므로 뺀다
    L.append(table(["검색엔진", "세션", "전"], [[k, v, se_prev.get(k, 0)] for k, v in se_now.items() if "blog" not in k] or [["(없음)", 0, 0]]))
    L += ["", "## 1-3. 도착 페이지(모든 유입)", ""]
    L.append(table(["도착 페이지", "세션"], [[r[0] or "(없음)", r[1]] for r in ga(c, S, E, ["landingPage"], ["sessions"], 20)]))
    L += ["", "## 2. ChatGPT 로 온 사람의 도착 페이지(무슨 질문을 하다 왔나)", ""]
    L.append(table(["도착 페이지", "세션", "평균 체류"], [[r[0], r[1], sec(r[2])] for r in
                   ga(c, S, E, ["landingPagePlusQueryString"], ["sessions", "averageSessionDuration"], 20, ("sessionSource", "chatgpt"))]))
    L += ["", "## 3. 많이 본 페이지", ""]
    L.append(table(["페이지", "조회", "사용자", "사용자당 참여"], [[r[0], r[1], r[2], sec(float(r[3]) / max(int(r[2]), 1))] for r in
                   ga(c, S, E, ["pagePath"], ["screenPageViews", "activeUsers", "userEngagementDuration"], 15)]))
    L += ["", "## 4. 도구 사용(이벤트)", ""]
    ev = ga(c, S, E, ["eventName"], ["eventCount", "totalUsers"], 40)
    L.append(table(["이벤트", "횟수", "사용자"], [r for r in ev if r[0].startswith(("practice_", "fixreq", "click", "file_download", "planner_", "helpful_", "site_search", "try_"))] or [["(없음)", 0, 0]]))
    try:  # practice_nofind 의 search_term 파라미터는 GA 기본 측정기준 searchTerm 으로 읽힌다
        nf = ga(c, S, E, ["searchTerm"], ["eventCount"], 15, ("eventName", "practice_nofind")) if any(r[0] == "practice_nofind" for r in ev) else []
    except Exception:
        nf = []
    if nf:
        L += ["", "모의면접에서 못 찾은 검색어(묶음 추가 후보): " + ", ".join(f"{r[0]}({r[1]})" for r in nf)]
    L += ["", "## 5. 블로그 글별(utm_campaign, top = 글 위쪽 링크)", ""]
    pt = post_titles()
    agg = {}  # 같은 글·같은 링크 위치는 한 줄로(utm_content 가 '(not set)'·빈 값으로 갈려 나오는 것 합침), 체류는 세션 가중 평균
    for r in ga(c, S, E, ["sessionCampaignName", "sessionManualAdContent"], ["sessions", "averageSessionDuration"], 40, ("sessionCampaignName", "post-")):
        k = (pt.get(r[0], r[0]), r[1] if r[1] not in ("(not set)", "") else "본문")
        n, d = agg.get(k, (0, 0.0))
        agg[k] = (n + int(r[2]), d + int(r[2]) * float(r[3]))
    L.append(table(["글", "링크 위치", "세션", "평균 체류"], [[k[0], k[1], n, sec(d / max(n, 1))] for k, (n, d) in sorted(agg.items(), key=lambda kv: -kv[1][0])]))
    # 90일 로드맵 지표(신뢰 → 검색 → 이용자 검증): 방문자 수보다 '실제로 준비에 쓴 사람'을 본다
    users = int((ga(c, S, E, [], ["activeUsers"]) or [[0]])[0][0])
    evd = {r[0]: r for r in ev}
    nr = {r[0]: int(r[1]) for r in ga(c, S, E, ["newVsReturning"], ["activeUsers"], 5)}
    notice_v = sum(int(r[1]) for r in ga(c, S, E, ["pagePath"], ["screenPageViews"], 5, ("pagePath", "/notice")))
    pct = lambda n: f"{n} ({n * 100 // max(users, 1)}%)"
    L += ["", "## 5-2. 로드맵 지표", ""]
    L.append(table(["지표", "값"], [
        ["사용자", users],
        ["재방문 사용자", pct(nr.get("returning", 0))],
        ["모의면접 질문 뽑기 사용자", pct(int(evd.get("practice_draw", [0, 0, 0])[2]))],
        ["모의면접 끝까지 마친 사용자", pct(int(evd.get("practice_done", [0, 0, 0])[2]))],
        ["수정·요청 메일 버튼(fixreq_click)", evd.get("fixreq_click", [0, 0])[1]],
        ["틀린 곳 신고 바로가기(fixreq_jump)", evd.get("fixreq_jump", [0, 0])[1]],
        ["/notice/ 조회", notice_v]]))
    # 3단계(이용자 검증, 2026-11-14 부터 이벤트 수집): '방문자'보다 '실제로 준비에 쓴 사람'
    PREP = ["practice_done", "planner_add", "planner_copy", "planner_print", "planner_ics"]
    prep_u = int((ga(c, S, E, [], ["totalUsers"], 1, ("eventName", PREP)) or [[0]])[0][0])
    g = lambda n, i=1: int(evd.get(n, [0, 0, 0])[i])
    pl_u = int((ga(c, S, E, [], ["activeUsers"], 1, ("pagePath", "/planner/")) or [[0]])[0][0])
    L += ["", "## 5-3. 이용자 검증 지표(3단계)", ""]
    L.append(table(["지표", "값"], [
        ["준비 행동 사용자(모의면접 완주·일정표 담기·복사·인쇄·달력 넣기 중 하나)", pct(prep_u)],
        ["일정표 방문 → 전형 담기 → 링크 복사·인쇄(사용자)", f"{pl_u} → {g('planner_add', 2)} → {g('planner_copy', 2)}·{g('planner_print', 2)} · 달력 {g('planner_ics', 2)}"],
        ["모의면접 질문 뽑기 → 답변 → 끝까지(사용자)", f"{g('practice_draw', 2)} → {g('practice_answer', 2)} → {g('practice_done', 2)}"],
        ["「도움이 됐나요?」 예 / 아니오(횟수)", f"{g('helpful_yes')} / {g('helpful_no')}"],
        ["사이트 검색(횟수) / 결과 없음", f"{g('site_search')} / {g('site_search_nofind')}"],
        ["/try/ 사용해 보기 시작 → 답 복사(사용자)", f"{g('try_start', 2)} → {g('try_copy', 2)}"]]))
    for evn, label in (("helpful_no", "「아니오」가 나온 페이지"), ("helpful_yes", "「예」가 많은 페이지")):
        if g(evn):
            try:
                rows = ga(c, S, E, ["pagePath"], ["eventCount"], 10, ("eventName", [evn]))
                L += ["", f"{label}: " + ", ".join(f"{r[0]}({r[1]})" for r in rows)]
            except Exception:
                pass
    for evn, label in (("site_search", "많이 찾은 검색어"), ("site_search_nofind", "찾았지만 결과가 없던 검색어(보강 후보)")):
        if g(evn):
            try:
                rows = ga(c, S, E, ["searchTerm"], ["eventCount"], 15, ("eventName", [evn]))
                L += ["", f"{label}: " + ", ".join(f"{r[0]}({r[1]})" for r in rows)]
            except Exception:
                pass
    try:
        rows = sc(c, S, E, ["query"], 20)
        clicks = sum(r["clicks"] for r in sc(c, S, E, ["date"]))
        prow = sc(c, PS, PE, ["date"])
        L += ["", "## 6. 구글 검색(서치콘솔)", f"클릭 {clicks} (전 기간 {sum(r['clicks'] for r in prow)})", ""]
        L.append(table(["검색어", "클릭", "노출", "평균 순위"], [[r["keys"][0], r["clicks"], r["impressions"], round(r["position"], 1)] for r in rows]))
    except Exception as e:  # 서치콘솔 권한이 아직 없을 때
        L += ["", f"## 6. 구글 검색 — 읽기 실패: {str(e)[:120]}"]
    text = "\n".join(L) + "\n"
    print(text)
    out = HERE.parent / "weekly" / f"{today.isoformat()}-api.md"
    out.write_text(text, encoding="utf-8")
    print("저장:", out)


if __name__ == "__main__":
    main()
