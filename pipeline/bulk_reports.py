"""전국 대학 선행학습 영향평가 보고서 일괄 수집 (서울진로진학정보센터 CDN 미러).

  python bulk_reports.py fetch [--year 2026]   # raw/<code>/<year>/<code>_<year>_report.pdf
  python bulk_reports.py scan                   # 각 PDF 에 면접 문항카드가 있는지 훑어 out/_bulk_scan.json
  python bulk_reports.py seed                    # data/seed/universities.json 에 대학·출처 추가

CDN 경로: https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info{year}/{대학명}/{대학명}_{year}학년도_선행학습영향평가.pdf
원문은 각 대학 입학처가 공개한 보고서이며 미러는 서울특별시교육청 진로진학정보센터(jinhak.or.kr)가 제공한다.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

import pymupdf
import requests
import truststore

truststore.inject_into_ssl()

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
RAW = ROOT / "raw"
CDN = "https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info{year}/"
BOARD = "https://www.jinhak.or.kr/subList/20000000267"

# code, 대학명(CDN 표기), 지역, 홈페이지
UNIVS = [
    # 서울
    ("hanyang", "한양대학교", "서울", "https://www.hanyang.ac.kr"),
    ("cau", "중앙대학교", "서울", "https://www.cau.ac.kr"),
    ("khu", "경희대학교", "서울", "https://www.khu.ac.kr"),
    ("hufs", "한국외국어대학교", "서울", "https://www.hufs.ac.kr"),
    ("uos", "서울시립대학교", "서울", "https://www.uos.ac.kr"),
    ("ewha", "이화여자대학교", "서울", "https://www.ewha.ac.kr"),
    ("sogang", "서강대학교", "서울", "https://www.sogang.ac.kr"),
    ("konkuk", "건국대학교", "서울", "https://www.konkuk.ac.kr"),
    ("dongguk", "동국대학교", "서울", "https://www.dongguk.edu"),
    ("hongik", "홍익대학교", "서울", "https://www.hongik.ac.kr"),
    ("kookmin", "국민대학교", "서울", "https://www.kookmin.ac.kr"),
    ("sookmyung", "숙명여자대학교", "서울", "https://www.sookmyung.ac.kr"),
    ("soongsil", "숭실대학교", "서울", "https://www.ssu.ac.kr"),
    ("sejong", "세종대학교", "서울", "https://www.sejong.ac.kr"),
    ("dankook", "단국대학교", "경기", "https://www.dankook.ac.kr"),
    ("kwangwoon", "광운대학교", "서울", "https://www.kw.ac.kr"),
    ("sangmyung", "상명대학교", "서울", "https://www.smu.ac.kr"),
    ("seoultech", "서울과학기술대학교", "서울", "https://www.seoultech.ac.kr"),
    ("sungshin", "성신여자대학교", "서울", "https://www.sungshin.ac.kr"),
    ("duksung", "덕성여자대학교", "서울", "https://www.duksung.ac.kr"),
    ("dongduk", "동덕여자대학교", "서울", "https://www.dongduk.ac.kr"),
    ("catholic", "가톨릭대학교", "경기", "https://www.catholic.ac.kr"),
    ("myongji", "명지대학교", "서울", "https://www.mju.ac.kr"),
    ("snue", "서울교육대학교", "서울", "https://www.snue.ac.kr"),
    ("swu", "서울여자대학교", "서울", "https://www.swu.ac.kr"),
    ("hansung", "한성대학교", "서울", "https://www.hansung.ac.kr"),
    ("skuniv", "서경대학교", "서울", "https://www.skuniv.ac.kr"),
    ("syu", "삼육대학교", "서울", "https://www.syu.ac.kr"),
    ("knsu", "한국체육대학교", "서울", "https://www.knsu.ac.kr"),
    ("skhu", "성공회대학교", "서울", "https://www.skhu.ac.kr"),
    ("chongshin", "총신대학교", "서울", "https://www.chongshin.ac.kr"),
    ("kaywon", "계원예술대학교", "경기", "https://www.kaywon.ac.kr"),
    # 경기·인천
    ("inha", "인하대학교", "인천", "https://www.inha.ac.kr"),
    ("ajou", "아주대학교", "경기", "https://www.ajou.ac.kr"),
    ("kyonggi", "경기대학교", "경기", "https://www.kyonggi.ac.kr"),
    ("gachon", "가천대학교", "경기", "https://www.gachon.ac.kr"),
    ("inu", "인천대학교", "인천", "https://www.inu.ac.kr"),
    ("hanyang-erica", "한양대학교(ERICA)", "경기", "https://www.hanyang.ac.kr/web/erica"),
    ("ginue", "경인교육대학교", "인천", "https://www.ginue.ac.kr"),
    ("cha", "차의과학대학교", "경기", "https://www.cha.ac.kr"),
    ("kau", "한국항공대학교", "경기", "https://www.kau.ac.kr"),
    ("sungkyul", "성결대학교", "경기", "https://www.sungkyul.ac.kr"),
    ("anyang", "안양대학교", "경기", "https://www.anyang.ac.kr"),
    ("ptu", "평택대학교", "경기", "https://www.ptu.ac.kr"),
    ("hs", "한신대학교", "경기", "https://www.hs.ac.kr"),
    ("uhs", "협성대학교", "경기", "https://www.uhs.ac.kr"),
    ("suwon", "수원대학교", "경기", "https://www.suwon.ac.kr"),
    ("tukorea", "한국공학대학교", "경기", "https://www.tukorea.ac.kr"),
    ("kangnam", "강남대학교", "경기", "https://www.kangnam.ac.kr"),
    ("yongin", "용인대학교", "경기", "https://www.yongin.ac.kr"),
    ("eulji", "을지대학교", "경기", "https://www.eulji.ac.kr"),
    ("daejin", "대진대학교", "경기", "https://www.daejin.ac.kr"),
    ("shinhan", "신한대학교", "경기", "https://www.shinhan.ac.kr"),
    ("stu", "서울신학대학교", "경기", "https://www.stu.ac.kr"),
    ("hknu", "한경국립대학교", "경기", "https://www.hknu.ac.kr"),
    ("hufs-global", "한국외국어대학교(글로벌)", "경기", "https://www.hufs.ac.kr"),
    ("dankook-cheonan", "단국대학교(천안)", "충남", "https://www.dankook.ac.kr"),
    # 대전·충청·강원
    ("kaist", "한국과학기술원", "대전", "https://www.kaist.ac.kr"),
    ("cnu", "충남대학교", "대전", "https://www.cnu.ac.kr"),
    ("cbnu", "충북대학교", "충북", "https://www.cbnu.ac.kr"),
    ("kangwon", "강원대학교", "강원", "https://www.kangwon.ac.kr"),
    ("hanbat", "한밭대학교", "대전", "https://www.hanbat.ac.kr"),
    ("gjue", "공주교육대학교", "충남", "https://www.gjue.ac.kr"),
    ("cje", "청주교육대학교", "충북", "https://www.cje.ac.kr"),
    ("cnue", "춘천교육대학교", "강원", "https://www.cnue.ac.kr"),
    ("koreatech", "한국기술교육대학교", "충남", "https://www.koreatech.ac.kr"),
    ("hallym", "한림대학교", "강원", "https://www.hallym.ac.kr"),
    ("sunmoon", "선문대학교", "충남", "https://www.sunmoon.ac.kr"),
    ("kongju", "공주대학교", "충남", "https://www.kongju.ac.kr"),
    ("knue", "한국교원대학교", "충북", "https://www.knue.ac.kr"),
    ("ut", "한국교통대학교", "충북", "https://www.ut.ac.kr"),
    ("sch", "순천향대학교", "충남", "https://www.sch.ac.kr"),
    ("nsu", "남서울대학교", "충남", "https://www.nsu.ac.kr"),
    ("bu", "백석대학교", "충남", "https://www.bu.ac.kr"),
    ("hoseo", "호서대학교", "충남", "https://www.hoseo.ac.kr"),
    ("kornu", "나사렛대학교", "충남", "https://www.kornu.ac.kr"),
    ("konyang", "건양대학교", "충남", "https://www.konyang.ac.kr"),
    ("pcu", "배재대학교", "대전", "https://www.pcu.ac.kr"),
    ("mokwon", "목원대학교", "대전", "https://www.mokwon.ac.kr"),
    ("hannam", "한남대학교", "대전", "https://www.hannam.ac.kr"),
    ("wsu", "우송대학교", "대전", "https://www.wsu.ac.kr"),
    ("dju", "대전대학교", "대전", "https://www.dju.ac.kr"),
    ("cju", "청주대학교", "충북", "https://www.cju.ac.kr"),
    ("semyung", "세명대학교", "충북", "https://www.semyung.ac.kr"),
    ("seowon", "서원대학교", "충북", "https://www.seowon.ac.kr"),
    ("gwnu", "강릉원주대학교", "강원", "https://www.gwnu.ac.kr"),
    ("yonsei-mirae", "연세대학교(미래)", "강원", "https://www.yonsei.ac.kr/wj"),
    ("sangji", "상지대학교", "강원", "https://www.sangji.ac.kr"),
    ("cku", "가톨릭관동대학교", "강원", "https://www.cku.ac.kr"),
    ("korea-sejong", "고려대학교(세종)", "세종", "https://sejong.korea.ac.kr"),
    ("hongik-sejong", "홍익대학교(세종)", "세종", "https://www.hongik.ac.kr"),
    # 대구·경북
    ("knu", "경북대학교", "대구", "https://www.knu.ac.kr"),
    ("postech", "포항공과대학교", "경북", "https://www.postech.ac.kr"),
    ("dgist", "대구경북과학기술원", "대구", "https://www.dgist.ac.kr"),
    ("yu", "영남대학교", "경북", "https://www.yu.ac.kr"),
    ("kmu", "계명대학교", "대구", "https://www.kmu.ac.kr"),
    ("daegu", "대구대학교", "경북", "https://www.daegu.ac.kr"),
    ("cu", "대구가톨릭대학교", "경북", "https://www.cu.ac.kr"),
    ("dhu", "대구한의대학교", "경북", "https://www.dhu.ac.kr"),
    ("kumoh", "금오공과대학교", "경북", "https://www.kumoh.ac.kr"),
    ("andong", "안동대학교", "경북", "https://www.andong.ac.kr"),
    ("kiu", "경일대학교", "경북", "https://www.kiu.ac.kr"),
    ("dongguk-wise", "동국대학교(WISE)", "경북", "https://www.dongguk.ac.kr"),
    ("handong", "한동대학교", "경북", "https://www.handong.edu"),
    ("dnue", "대구교육대학교", "대구", "https://www.dnue.ac.kr"),
    ("kyungpook-natl", "국립경국대학교", "경북", "https://www.andong.ac.kr"),
    # 부산·울산·경남
    ("pnu", "부산대학교", "부산", "https://www.pusan.ac.kr"),
    ("unist", "울산과학기술원", "울산", "https://www.unist.ac.kr"),
    ("gnu", "경상국립대학교", "경남", "https://www.gnu.ac.kr"),
    ("dau", "동아대학교", "부산", "https://www.donga.ac.kr"),
    ("pknu", "부경대학교", "부산", "https://www.pknu.ac.kr"),
    ("ulsan", "울산대학교", "울산", "https://www.ulsan.ac.kr"),
    ("bnue", "부산교육대학교", "부산", "https://www.bnue.ac.kr"),
    ("cue", "진주교육대학교", "경남", "https://www.cue.ac.kr"),
    ("changwon", "창원대학교", "경남", "https://www.changwon.ac.kr"),
    ("inje", "인제대학교", "경남", "https://www.inje.ac.kr"),
    ("deu", "동의대학교", "부산", "https://www.deu.ac.kr"),
    ("ks", "경성대학교", "부산", "https://www.ks.ac.kr"),
    ("silla", "신라대학교", "부산", "https://www.silla.ac.kr"),
    ("bufs", "부산외국어대학교", "부산", "https://www.bufs.ac.kr"),
    ("kmou", "한국해양대학교", "부산", "https://www.kmou.ac.kr"),
    ("ysu", "영산대학교", "경남", "https://www.ysu.ac.kr"),
    ("kosin", "고신대학교", "부산", "https://www.kosin.ac.kr"),
    ("dongseo", "동서대학교", "부산", "https://www.dongseo.ac.kr"),
    ("tu", "동명대학교", "부산", "https://www.tu.ac.kr"),
    # 광주·전라·제주
    ("jnu", "전남대학교", "광주", "https://www.jnu.ac.kr"),
    ("jbnu", "전북대학교", "전북", "https://www.jbnu.ac.kr"),
    ("gist", "광주과학기술원", "광주", "https://www.gist.ac.kr"),
    ("kentech", "한국에너지공과대학교", "전남", "https://www.kentech.ac.kr"),
    ("chosun", "조선대학교", "광주", "https://www.chosun.ac.kr"),
    ("wku", "원광대학교", "전북", "https://www.wku.ac.kr"),
    ("gnue", "광주교육대학교", "광주", "https://www.gnue.ac.kr"),
    ("jnue", "전주교육대학교", "전북", "https://www.jnue.ac.kr"),
    ("jejunu", "제주대학교", "제주", "https://www.jejunu.ac.kr"),
    ("mokpo", "목포대학교", "전남", "https://www.mokpo.ac.kr"),
    ("gwangju", "광주대학교", "광주", "https://www.gwangju.ac.kr"),
    ("honam", "호남대학교", "광주", "https://www.honam.ac.kr"),
    ("woosuk", "우석대학교", "전북", "https://www.woosuk.ac.kr"),
    ("jj", "전주대학교", "전북", "https://www.jj.ac.kr"),
    ("kunsan", "군산대학교", "전북", "https://www.kunsan.ac.kr"),
    ("scnu", "순천대학교", "전남", "https://www.scnu.ac.kr"),
    ("dsu", "동신대학교", "전남", "https://www.dsu.ac.kr"),
    ("nambu", "남부대학교", "광주", "https://www.nambu.ac.kr"),
    ("sehan", "세한대학교", "전남", "https://www.sehan.ac.kr"),
    # 특수
    ("police", "경찰대학", "충남", "https://www.police.ac.kr"),
    ("kma", "육군사관학교", "서울", "https://www.kma.ac.kr"),
    ("navy", "해군사관학교", "경남", "https://www.navy.ac.kr"),
    ("afa", "공군사관학교", "충북", "https://www.afa.ac.kr"),
    ("kafna", "국군간호사관학교", "대전", "https://www.kafna.ac.kr"),
]

# 서울대·연세대·고려대·성균관대는 입학처 원본으로 이미 수집 → 여기서 제외
SKIP = {"snu", "yonsei", "korea", "skku"}


def cdn_url(name: str, year: int) -> str:
    return CDN.format(year=year) + urllib.parse.quote(f"{name}/{name}_{year}학년도_선행학습영향평가.pdf")


def fetch(year: int):
    ok, miss = [], []
    for code, name, region, home in UNIVS:
        if code in SKIP:
            continue
        dest = RAW / code / str(year) / f"{code}_{year}_report.pdf"
        if dest.exists() and dest.stat().st_size > 1000:
            ok.append(code)
            continue
        url = cdn_url(name, year)
        try:
            r = requests.get(url, timeout=120, stream=True, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                miss.append((code, name, r.status_code))
                continue
            it = r.iter_content(1 << 16)
            first = next(it, b"")
            if not first.startswith(b"%PDF"):
                miss.append((code, name, "not-pdf"))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("wb") as f:
                f.write(first)
                for c in it:
                    f.write(c)
            ok.append(code)
            print(f"[fetch] {code} {name} {dest.stat().st_size // 1024}KB", flush=True)
        except Exception as e:  # noqa: BLE001
            miss.append((code, name, str(e)[:60]))
    print(f"\nok {len(ok)}  missing {len(miss)}")
    for m in miss:
        print("  MISS", m)


def scan(year: int):
    """면접 문항카드 존재 여부 훑기: '문항 정보' 헤더 수, '면접' 카드 수, '문항 미작성' 문구."""
    import re
    out = {}
    for code, name, region, home in UNIVS:
        pdf = RAW / code / str(year) / f"{code}_{year}_report.pdf"
        if not pdf.exists():
            continue
        try:
            doc = pymupdf.open(pdf)
            text = "\n".join(p.get_text("text", sort=True) for p in doc)
        except Exception as e:  # noqa: BLE001
            out[code] = {"error": str(e)[:80]}
            continue
        cards = len(re.findall(r"문항\s*정보\s*\]|\[\s*[가-힣]+대학교?\s*문항\s*정보|문항\s*카드\s*$", text, re.M))
        interview_cards = len(re.findall(r"■\s*면접|▣\s*면접|☑\s*면접|✔\s*면접|\[■\]\s*면접", text))
        not_written = len(re.findall(r"문항\s*미작성|문항카드\s*미작성|해당\s*없음", text))
        qmarks = len(re.findall(r"^\s*(?:\[문제\s*\d|문제\s*\d|문항\s*\d|\d+\.\s+[가-힣].{10,}(?:시오|나요|까요)\s*$)", text, re.M))
        out[code] = {"name": name, "pages": len(doc), "cards": cards, "interview_cards": interview_cards, "not_written": not_written, "question_lines": qmarks}
        print(f"{code:16s} {name:14s} p={len(doc):3d} cards={cards:3d} interview={interview_cards:3d} notwritten={not_written:2d} qlines={qmarks:3d}", flush=True)
    (ROOT / "out" / "_bulk_scan.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def seed(year: int):
    p = REPO / "data" / "seed" / "universities.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    have = {u["code"]: u for u in d["universities"]}
    added = 0
    for code, name, region, home in UNIVS:
        if code in SKIP:
            continue
        pdf = RAW / code / str(year) / f"{code}_{year}_report.pdf"
        if not pdf.exists():
            continue
        src = {"year": year, "kind": "report", "title": f"{year}학년도 {name} 선행학습 영향평가 보고서 (서울진로진학정보센터 미러)",
               "page_url": BOARD, "url": cdn_url(name, year), "filename": f"{code}_{year}_report.pdf", "verified": False}
        if code in have:
            u = have[code]
            if not any(s.get("url") == src["url"] for s in u.get("sources", [])):
                u.setdefault("sources", []).append(src)
        else:
            t = "teachers" if name.endswith("교육대학교") else "military" if "사관학교" in name else "police" if "경찰" in name else "special" if name.endswith("과학기술원") or "공과대학교" in name and "에너지" in name else "general"
            d["universities"].append({"code": code, "name": name, "region": region, "type": t, "admission_url": home, "report_board_url": BOARD, "priority": 5, "sources": [src]})
            added += 1
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"seed: total {len(d['universities'])} (+{added})")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    year = int(sys.argv[sys.argv.index("--year") + 1]) if "--year" in sys.argv else 2026
    {"fetch": fetch, "scan": scan, "seed": seed}[cmd](year)
