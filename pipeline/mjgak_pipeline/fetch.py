"""수집기: universities.json 의 sources 에 적힌 PDF URL 을 raw/{code}/{year}/ 에 내려받는다.

- 원문 PDF 는 git 제외(raw/). 앱에서 서빙하지 않는다.
- 크롤링이 막힌 사이트는 수동 다운로드 후 같은 경로에 두면 이후 단계가 동일하게 동작한다.
- 사내망처럼 TLS 검사 프록시가 있는 환경을 위해 OS 인증서 저장소(truststore)를 쓴다.
- 대학 게시판은 보통 게시글을 먼저 열어 세션 쿠키를 받고 Referer 를 붙여야 파일을 준다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import requests
import truststore

truststore.inject_into_ssl()

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "data" / "seed" / "universities.json"
RAW = ROOT / "pipeline" / "raw"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) mjgak-pipeline/0.1"


def load_universities() -> list[dict]:
    return json.loads(SEED.read_text(encoding="utf-8"))["universities"]


def get_university(code: str) -> dict:
    return next(u for u in load_universities() if u["code"] == code)


def safe_name(s: str) -> str:
    return re.sub(r"[^\w.-]+", "_", s)[:120]


def download(url: str, dest: Path, page_url: str | None = None, timeout: int = 120) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    s = requests.Session()
    s.headers["User-Agent"] = UA
    headers = {}
    if page_url:
        s.get(page_url, timeout=timeout)  # 세션 쿠키
        headers["Referer"] = page_url
    r = s.get(url, headers=headers, timeout=timeout, stream=True)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "")
    if "pdf" not in ctype and "octet-stream" not in ctype:
        raise RuntimeError(f"PDF 가 아닙니다 (content-type={ctype}). 게시글 URL 을 확인하세요.")
    with dest.open("wb") as f:
        for chunk in r.iter_content(1 << 16):
            f.write(chunk)
    return dest


def source_dest(code: str, src: dict) -> Path:
    fname = src.get("filename") or safe_name(src["url"].rsplit("/", 1)[-1] or "report")
    if not fname.lower().endswith(".pdf"):
        fname += ".pdf"
    return RAW / code / str(src["year"]) / fname


def fetch_university(code: str, year: int | None = None) -> list[Path]:
    univ = get_university(code)
    got: list[Path] = []
    for src in univ.get("sources", []):
        if year and src["year"] != year:
            continue
        dest = source_dest(code, src)
        try:
            got.append(download(src["url"], dest, page_url=src.get("page_url")))
            print(f"[fetch] {code} {src['year']} {dest.stat().st_size//1024}KB -> {dest.relative_to(ROOT)}")
        except Exception as e:  # noqa: BLE001
            print(f"[fetch] FAILED {src['url']}: {e}\n        수동 다운로드 후 {dest.relative_to(ROOT)} 에 저장하세요.")
    return got
