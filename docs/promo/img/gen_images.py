"""블로그 원고의 제미나이 프롬프트로 본문 이미지를 자동 생성 (Vertex AI, 구독 월 크레딧 안에서만).

원고 작업 메모의 "[제미나이 프롬프트 N — 장면 (4:3)]" 다음 영문 프롬프트를 읽어
img/gem-<slug>-<N>.png 로 저장한다. slug 는 원고의 "썸네일: img/thumb-<slug>.png" 에서 딴다.

  python gen_images.py ../naver-98-동물보건학과-v2.md            # 생성
  python gen_images.py ../naver-98-동물보건학과-v2.md --dry-run  # 프롬프트·예상 비용만
  python gen_images.py --status                                   # 이번 달 사용액

돈을 더 쓰지 않는다: 월 장부(../gen-ledger.json)에 장당 비용을 넉넉히 잡아 쌓고,
MONTHLY_CAP_KRW(../.env)에 닿으면 생성하지 않고 멈춘다. 콘솔의 Vertex AI 지출 한도(₩10,000)가 두 번째 안전장치.
"""
import base64, datetime, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
LEDGER = PROMO / "gen-ledger.json"
PROJECT = "mjgak-images"
MODEL = "gemini-2.5-flash-image"
# 장당 약 $0.039(출력 이미지 1290토큰) — 환율·프롬프트 토큰까지 넉넉히 잡아 ₩70
COST_PER_IMAGE_KRW = 70
URL = f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/global/publishers/google/models/{MODEL}:generateContent"


def env():
    out = {}
    for ln in (PROMO / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in ln and not ln.lstrip().startswith("#"):
            k, v = ln.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}


def month():
    return datetime.date.today().strftime("%Y-%m")


def spent(lg):
    return lg.get(month(), {}).get("krw", 0)


def record(lg, name):
    m = lg.setdefault(month(), {"krw": 0, "count": 0, "items": []})
    m["krw"] += COST_PER_IMAGE_KRW
    m["count"] += 1
    m["items"].append(name)
    LEDGER.write_text(json.dumps(lg, ensure_ascii=False, indent=1), encoding="utf-8")


def prompts(md: Path):
    full = md.read_text(encoding="utf-8")
    memo = full.split("=" * 20, 1)[1] if "=" * 20 in full else ""
    gem = re.findall(r"^\[(제미나이 프롬프트[^\]]*)\]\s*\n(.+?)(?=\n\s*\n|\n\[|\Z)", memo, flags=re.M | re.S)
    m = re.search(r"img/thumb-([\w-]+)\.png", full)
    slug = m.group(1) if m else md.stem.split("-")[1]
    out = []
    for lbl, txt in gem:
        n = re.search(r"프롬프트\s*(\d+)", lbl)
        ratio = re.search(r"\((\d+:\d+)\)\s*$", lbl)
        out.append((int(n.group(1)) if n else len(out) + 1, txt.strip(), ratio.group(1) if ratio else "4:3"))
    return slug, out


def link_in_post(md: Path, n: int, fname: str):
    """본문 이미지 자리 줄 끝에 파일 이름을 붙인다 → 오토포스트 등록 때 그 그림이 자동으로 들어간다(engine/mjgak.py 가 자리 줄의 .png 를 찾음)."""
    full = md.read_text(encoding="utf-8")
    pat = re.compile(rf"^(\[이미지 {n}\b[^\]\n]*제미나이 프롬프트 {n}\b[^\]\n]*?)\]", re.M)
    new, k = pat.subn(lambda m: m.group(0) if ".png" in m.group(1) else f"{m.group(1)} · {fname}]", full, count=1)
    if k and new != full:
        md.write_text(new, encoding="utf-8")


def generate(key, text, ratio):
    body = {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ratio}}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for i in range(6):  # 연결 단계 끊김(SSLEOF 등)만 다시 시도 — HTTP 오류는 그대로 올린다
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                res = json.load(r)
            break
        except urllib.error.HTTPError:
            raise
        except urllib.error.URLError:
            if i == 5:
                raise
            time.sleep(15 * (i + 1))
    for c in res.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("이미지가 오지 않았습니다: " + json.dumps(res, ensure_ascii=False)[:300])


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # 윈도 콘솔(cp949)에서 ₩·✔ 출력
    args = sys.argv[1:]
    cfg = env()
    cap = int(cfg.get("MONTHLY_CAP_KRW") or 10000)
    lg = ledger()
    if "--status" in args:
        print(f"{month()} 사용 ₩{spent(lg):,} / 상한 ₩{cap:,} · {lg.get(month(), {}).get('count', 0)}장")
        return 0
    md = Path(next(a for a in args if not a.startswith("--")))
    slug, items = prompts(md)
    if not items:
        print("제미나이 프롬프트가 없습니다:", md.name)
        return 1
    dry, force = "--dry-run" in args, "--force" in args
    todo = [(n, t, r, HERE / f"gem-{slug}-{n}.png") for n, t, r in items]
    for n, _, _, f in todo:
        if f.exists():
            link_in_post(md, n, f.name)
    todo = [x for x in todo if force or not x[3].exists()]
    print(f"{md.name}: 프롬프트 {len(items)}개, 새로 만들 것 {len(todo)}장 · 예상 ₩{len(todo) * COST_PER_IMAGE_KRW:,} · "
          f"이번 달 사용 ₩{spent(lg):,} / 상한 ₩{cap:,}")
    if dry:
        for n, t, r, f in todo:
            print(f"  {f.name} ({r}) {t[:80]}…")
        return 0
    key = cfg.get("VERTEX_API_KEY", "")
    if not key:
        print("docs/promo/.env 의 VERTEX_API_KEY 가 비어 있습니다.")
        return 2
    for n, t, r, f in todo:
        if spent(lg) + COST_PER_IMAGE_KRW > cap:
            print(f"■ 이번 달 크레딧 상한(₩{cap:,})에 닿아 생성을 멈춥니다. 남은 이미지는 제미나이 프롬프트로 직접 만들어 주세요.")
            return 3
        try:
            data = generate(key, t, r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:400]
            print(f"■ {f.name} 실패 HTTP {e.code}: {msg}")
            if e.code in (403, 429):
                print("■ 권한·한도 문제(지출 한도 도달로 서비스가 멈췄을 수 있음) — 생성을 멈춥니다.")
                return 3
            continue
        f.write_bytes(data)
        record(lg, f.name)
        link_in_post(md, n, f.name)
        print(f"  ✔ {f.name} ({len(data) // 1024}KB) · 누적 ₩{spent(lg):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
