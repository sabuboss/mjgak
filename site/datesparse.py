"""rich/univ 의 면접일·1단계 발표 문자열("11/21(토) … · 11/22(일) …")에서 날짜를 뽑는다."""
import datetime as dt
import re

# 면접일이 아닌 날짜(공지·서류·신체검사 등)가 들어 있는 조각은 버린다
SKIP = re.compile(r"유의사항|공고|발표|게재|출력|안내|공지|신체검사|실기고사|온라인 군 인성검사|업로드|제출|예비소집|예약")
DONE = re.compile(r"이미 끝남|이미 종료|\(종료\)|종료\b")
D = r"(\d{1,2})/(\d{1,2})(?:\([월화수목금토일]\))?"


def _year(m: int) -> int:
    return 2027 if m <= 2 else 2026


def _clean(s: str) -> str:
    # 괄호 안 공지 문구 제거: "(면접시간·장소는 11/18(수) 홈페이지 발표)"
    out, depth, buf = [], 0, ""
    for ch in s:
        if ch == "(":
            if depth == 0:
                out.append(buf); buf = ""
            depth += 1; buf += ch
        elif ch == ")" and depth:
            depth -= 1; buf += ch
            if depth == 0:
                out.append("" if SKIP.search(buf) else buf); buf = ""
        else:
            buf += ch
    out.append(buf)
    s = "".join(out)
    # " · " 로 나뉜 조각 중 공지 문구가 있는 조각 제거
    return " · ".join(p for p in re.split(r"\s·\s|,\s", s) if not SKIP.search(re.sub(D, "", p)) or not re.search(D, p))


def parse(s: str | None) -> list[str]:
    if not s or DONE.search(s):
        return []
    s = _clean(s)
    days: set[dt.date] = set()
    for m in re.finditer(D + r"((?:\s*[~·]\s*(?:\d{1,2}/)?\d{1,2}(?:\([월화수목금토일]\))?)*)", s):
        mo, d0 = int(m.group(1)), int(m.group(2))
        cur = dt.date(_year(mo), mo, d0)
        days.add(cur)
        for sep, mm, dd in re.findall(r"\s*([~·])\s*(?:(\d{1,2})/)?(\d{1,2})", m.group(3)):
            mo2 = int(mm) if mm else cur.month
            nxt = dt.date(_year(mo2), mo2, int(dd))
            if sep == "~":
                x = cur
                while x < nxt:
                    x += dt.timedelta(days=1); days.add(x)
            days.add(nxt)
            cur = nxt
    return sorted(x.isoformat() for x in days)


def first(s: str | None) -> str | None:
    if not s:
        return None
    m = re.search(D, s)
    return dt.date(_year(int(m.group(1))), int(m.group(1)), int(m.group(2))).isoformat() if m else None
