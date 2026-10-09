# schedule_data.py → site/pages/schedule.md 의 대학별 면접 날짜 표 (마커 사이를 교체).
# python schedule_to_site.py
import sys, json, glob, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from schedule_data import SECTIONS

ROOT = Path(__file__).resolve().parents[3]
PAGE = ROOT / "site" / "pages" / "schedule.md"
START, END = "<!-- SCHEDULE-TABLE START -->", "<!-- SCHEDULE-TABLE END -->"

FULL = {"서울교대": "서울교육대학교", "덕성여대": "덕성여자대학교", "이화여대": "이화여자대학교",
        "성신여대": "성신여자대학교", "숙명여대": "숙명여자대학교"}


def code_map():
    m = {}
    for f in glob.glob(str(ROOT / "site" / "content" / "university_profiles*.json")):
        for u in json.load(open(f, encoding="utf-8"))["universities"]:
            m[u["name"]] = u["code"]
    return m


def link(short, codes):
    full = FULL.get(short, short.replace("대", "대학교", 1) if short.endswith("대") else short)
    code = codes.get(full)
    if code and (ROOT / "site" / "dist" / "univ" / code / "index.html").exists():
        return f'<a href="/univ/{code}/">{html.escape(short)}</a>'
    return html.escape(short)


def build():
    codes = code_map()
    out = [START, '<h2 id="dates">2027학년도 수시 대학별 면접 날짜</h2>',
           '<p>각 대학 <b>2027학년도 수시모집요강</b>에서 직접 확인한 면접일과 1단계 발표일입니다. '
           '같은 대학도 계열·단과대학에 따라 날짜가 다르니 내 모집단위를 확인하고, 시간·장소는 1단계 발표 때 입학처 공지를 보세요.</p>']
    for title, sub, rows in SECTIONS:
        out.append(f"<h3>{html.escape(title)} <small>{html.escape(sub)}</small></h3>")
        out.append('<table class="tbl"><tr><th>면접일</th><th>대학</th><th>전형 · 모집단위</th><th>1단계 발표</th></tr>')
        for date, univ, track, unit, first, memo in rows:
            extra = f"<br><small>{html.escape(unit)}" + (f" · {html.escape(memo)}" if memo else "") + "</small>"
            out.append(f"<tr><td><b>{html.escape(date)}</b></td><td>{link(univ, codes)}</td>"
                       f"<td>{html.escape(track)}{extra}</td><td>{html.escape(first)}</td></tr>")
        out.append("</table>")
    out.append('<p class="note">동국대 Do Dream은 2단계 전형료 납부 마감(11월 16일 16:00)을 놓치면 면접을 볼 수 없습니다. '
               '중앙대는 다른 대학과 시간이 겹칠 때 같은 날 안에서 면접 시간 조정을 신청할 수 있습니다(일자 변경 불가). '
               '빠진 대학이나 바뀐 날짜는 <a href="/contact/">문의</a>로 알려 주세요.</p>')
    out.append(END)
    return "\n".join(out)


def main():
    s = PAGE.read_text(encoding="utf-8")
    block = build()
    if START in s:
        a, rest = s.split(START, 1)
        _, b = rest.split(END, 1)
        s = a + block + b
    else:
        anchor = "<h2>지금 어느 시기인가요?</h2>"
        assert anchor in s
        s = s.replace(anchor, block + "\n\n" + anchor, 1)
    PAGE.write_text(s, encoding="utf-8")
    print("updated", PAGE, block.count("<tr>") - len(SECTIONS), "rows")


if __name__ == "__main__":
    main()
