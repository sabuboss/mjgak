"""GA4·서치콘솔 숫자를 브라우저 로그인 없이 API 로 읽어 유입 리포트를 만든다(둘 다 무료 API).

준비(한 번만): docs/promo/analytics/SETUP.md
  python report.py                 # 지난 7일 vs 그 전 7일 → 화면 출력 + ../weekly/<오늘>-api.md
  python report.py --days 2        # 최근 2일
  python report.py --check         # 열쇠·권한만 확인

열쇠 파일: docs/promo/.secrets/ga-reader.json (서비스 계정, git 에 안 올라감). 읽기 전용 권한만 준다.
"""
import argparse, datetime, os, ssl, sys, tempfile, warnings
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
        req.dimension_filter = FilterExpression(filter=Filter(field_name=name, string_filter=Filter.StringFilter(
            value=val, match_type=Filter.StringFilter.MatchType.CONTAINS)))
    res = cl.run_report(req)
    return [[v.value for v in r.dimension_values] + [v.value for v in r.metric_values] for r in res.rows]


def sc(c, start, end, dims, limit=25):
    from googleapiclient.discovery import build
    s = build("searchconsole", "v1", credentials=c, cache_discovery=False)
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit}
    return s.searchanalytics().query(siteUrl=SC_SITE, body=body).execute().get("rows", [])


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
    L += ["## 1. 어디서 왔나", f"세션 {tot} (전 기간 {ptot})", ""]
    L.append(table(["출처/매체", "세션", "전", "참여 세션", "평균 체류"],
                   [[k, r[1], prev.get(k, [0, 0])[1], r[2], sec(r[3])] for k, r in now.items()]))
    L += ["", "## 2. ChatGPT 로 온 사람의 도착 페이지(무슨 질문을 하다 왔나)", ""]
    L.append(table(["도착 페이지", "세션", "평균 체류"], [[r[0], r[1], sec(r[2])] for r in
                   ga(c, S, E, ["landingPagePlusQueryString"], ["sessions", "averageSessionDuration"], 20, ("sessionSource", "chatgpt"))]))
    L += ["", "## 3. 많이 본 페이지", ""]
    L.append(table(["페이지", "조회", "사용자", "사용자당 참여"], [[r[0], r[1], r[2], sec(float(r[3]) / max(int(r[2]), 1))] for r in
                   ga(c, S, E, ["pagePath"], ["screenPageViews", "activeUsers", "userEngagementDuration"], 15)]))
    L += ["", "## 4. 도구 사용(이벤트)", ""]
    ev = ga(c, S, E, ["eventName"], ["eventCount", "totalUsers"], 40)
    L.append(table(["이벤트", "횟수", "사용자"], [r for r in ev if r[0].startswith(("practice_", "fixreq", "click", "file_download"))] or [["(없음)", 0, 0]]))
    try:  # search_term 맞춤 측정기준을 GA 에 등록해야 읽힌다(없으면 건너뜀)
        nf = ga(c, S, E, ["customEvent:search_term"], ["eventCount"], 15, ("eventName", "practice_nofind")) if any(r[0] == "practice_nofind" for r in ev) else []
    except Exception:
        nf = []
    if nf:
        L += ["", "모의면접에서 못 찾은 검색어(묶음 추가 후보): " + ", ".join(f"{r[0]}({r[1]})" for r in nf)]
    L += ["", "## 5. 블로그 글별(utm_campaign)", ""]
    L.append(table(["글", "세션", "평균 체류"], [[r[0], r[1], sec(r[2])] for r in
                   ga(c, S, E, ["sessionCampaignName"], ["sessions", "averageSessionDuration"], 20, ("sessionCampaignName", "post-"))]))
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
