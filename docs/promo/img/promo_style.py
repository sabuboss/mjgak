"""면접각 블로그 이미지 통일 디자인 (썸네일 · 모집요강 캡처 · 답변 구조 도식).

모든 이미지가 같은 색·글꼴·틀을 쓰도록 여기서만 정의한다.
  python promo_style.py            # 아래 JOBS 전부 생성
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pymupdf

HERE = Path(__file__).parent
SRC = HERE / "src"
F = "C:/Windows/Fonts/malgun.ttf"
FB = "C:/Windows/Fonts/malgunbd.ttf"

# ---- 팔레트 (모든 이미지 공통) ----
NAVY = "#23406e"      # 메인
NAVY_D = "#172c4d"    # 진한 배경
BLUE = "#3b6db3"
PALE = "#e8eef8"      # 연한 파랑
BG = "#f3f5f8"        # 바탕 회색
LINE = "#cfd6de"
TEXT = "#1c2430"
GRAY = "#66717f"
ACCENT = "#ffd166"    # 강조 노랑
CORAL = "#e8795a"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else F, size)


def wrap_chars(d, text, fnt, maxw):
    out, cur = [], ""
    for ch in text:
        t = cur + ch
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            out.append(cur); cur = ch
    if cur:
        out.append(cur)
    return out


def brand(d, x, y, size=26, color=GRAY):
    d.text((x, y), "면접각", font=font(size, True), fill=color)
    w = d.textlength("면접각", font=font(size, True))
    d.text((x + w + 10, y + size * 0.18), "mjgak.com", font=font(int(size * 0.8)), fill=color)


# ---------------------------------------------------------------- 썸네일
def make_thumb(out, dept, line2="면접 질문 6가지", line3="답변 예시 총정리", chip="2027 수시 면접", size=1080):
    """정사각 썸네일. 네이버 검색 결과에서 가운데가 잘려도 제목이 보이도록 중앙 정렬."""
    W = H = size
    img = Image.new("RGB", (W, H), NAVY_D)
    d = ImageDraw.Draw(img)
    # 배경 장식: 큰 원 두 개 + 말풍선 Q/A
    d.ellipse([W - 420, -180, W + 160, 400], fill=NAVY)
    d.ellipse([-220, H - 360, 300, H + 160], fill=NAVY)
    def bubble(x, y, w, h, fill, letter, lc):
        d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=fill)
        d.polygon([(x + 40, y + h - 2), (x + 90, y + h - 2), (x + 38, y + h + 42)], fill=fill)
        f = font(int(h * 0.62), True)
        d.text((x + w / 2 - d.textlength(letter, font=f) / 2, y + h * 0.12), letter, font=f, fill=lc)
    bubble(W - 300, 150, 150, 120, PALE, "Q", NAVY)
    bubble(W - 210, 300, 150, 120, ACCENT, "A", NAVY_D)
    # 칩
    fc = font(34, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([90, 150, 90 + cw + 56, 150 + 64], radius=32, fill=ACCENT)
    d.text((90 + 28, 158), chip, font=fc, fill=NAVY_D)
    # 제목
    y = 330
    f1 = font(118, True)
    for ln in wrap_chars(d, dept, f1, W - 180):
        d.text((88, y), ln, font=f1, fill="white"); y += 140
    f2 = font(84, True)
    d.text((88, y + 6), line2, font=f2, fill="white"); y += 130
    f3 = font(60, True)
    tw = d.textlength(line3, font=f3)
    d.rounded_rectangle([88, y, 88 + tw + 48, y + 92], radius=18, fill=CORAL)
    d.text((88 + 24, y + 6), line3, font=f3, fill="white")
    # 하단 브랜드
    d.line([90, H - 150, W - 90, H - 150], fill=BLUE, width=2)
    brand(d, 90, H - 118, size=40, color="white")
    fs = font(28)
    s = "학과별 · 대학별 면접 무료 정리"
    d.text((W - 90 - d.textlength(s, font=fs), H - 108), s, font=fs, fill=PALE)
    img.save(out)
    print("thumb", out, img.size)


# ---------------------------------------------------------------- 모집요강 캡처
def make_capture(out, pdf, page, start, end, univ, doc_label, note, dpi=200, start_pad=14, end_pad=6, lr=28, start_idx=0, end_idx=0):
    """PDF 한 쪽에서 start 문구 ~ end(문구 또는 y좌표 또는 ('after', 문구)) 구간을 잘라 공통 틀에 넣는다.
    같은 문구가 여러 번 나오면 start_idx / end_idx 로 몇 번째인지 고른다(-1 은 마지막)."""
    pg = pymupdf.open(pdf)[page - 1]
    y0 = pg.search_for(start)[start_idx].y0 - start_pad
    if isinstance(end, tuple) and end[0] == "after":
        y1 = pg.search_for(end[1])[end_idx].y1 + end_pad
    elif isinstance(end, str):
        y1 = pg.search_for(end)[0].y0 - end_pad
    else:
        y1 = end
    r = pg.rect
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.x0 + lr, y0, r.x1 - lr, y1))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    W = shot.width + 80
    HEAD, FOOT = 104, 92
    img = Image.new("RGB", (W, HEAD + shot.height + 40 + FOOT), BG)
    d = ImageDraw.Draw(img)
    # 헤더: 네이비 띠 + 칩
    d.rectangle([0, 0, W, HEAD], fill=NAVY)
    fc = font(30, True)
    chip = "2027학년도 모집요강"
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 44, 26 + 52], radius=26, fill=ACCENT)
    d.text((40 + 22, 31), chip, font=fc, fill=NAVY_D)
    d.text((40 + cw + 70, 30), univ, font=font(38, True), fill="white")
    # 본문 캡처
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    # 푸터
    fy = HEAD + shot.height + 40
    d.text((40, fy + 10), f"출처: {univ} {doc_label}", font=font(26), fill=GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


# ---------------------------------------------------------------- 답변 구조 도식
def make_structure(out, examples, W=1200):
    labels = [("1", "결론", "질문에 대한 답을 한 문장으로 먼저"),
              ("2", "경험", "그렇게 생각하게 된 경험 하나 (언제·무엇·숫자)"),
              ("3", "배운 점", "그 경험 전후로 무엇이 달라졌나"),
              ("4", "연결", "그래서 이 학과에서 무엇을 하고 싶은가")]
    tmp = Image.new("RGB", (W, 10)); td = ImageDraw.Draw(tmp)
    f_ex = font(22)
    PAD = 60; bx0, bx1 = PAD, W - PAD; tx = bx0 + 170
    rows = []
    for (n, lab, desc), ex in zip(labels, examples):
        lines = wrap_chars(td, f"\"{ex}\"", f_ex, (bx1 - 16) - (tx + 46) - 16)
        rows.append((n, lab, desc, lines, 100 + 30 * len(lines)))
    HEAD = 150
    H = HEAD + sum(r[4] for r in rows) + 34 * 3 + 190
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD - 30], fill=NAVY)
    d.text((PAD, 26), "면접 답변 구조 4단계", font=font(42, True), fill="white")
    d.text((PAD, 82), "어떤 질문이든 이 순서로 40~60초. 외우는 게 아니라 구조를 익히는 것입니다.", font=font(22), fill=PALE)
    y = HEAD
    for i, (n, lab, desc, lines, h) in enumerate(rows):
        d.rounded_rectangle([bx0, y, bx1, y + h], radius=14, fill="white", outline=LINE, width=2)
        d.rounded_rectangle([bx0, y, bx0 + 150, y + h], radius=14, fill=PALE)
        d.rectangle([bx0 + 120, y, bx0 + 150, y + h], fill=PALE)
        d.ellipse([bx0 + 22, y + 18, bx0 + 68, y + 64], fill=NAVY)
        fn = font(30, True)
        d.text((bx0 + 45 - d.textlength(n, font=fn) / 2, y + 22), n, font=fn, fill="white")
        d.text((bx0 + 22, y + h - 52), lab, font=font(30, True), fill=NAVY)
        d.text((tx, y + 18), desc, font=font(23, True), fill=TEXT)
        d.rounded_rectangle([tx, y + 58, bx1 - 16, y + 58 + 30 * len(lines) + 14], radius=8, fill="#f7f9fc")
        d.text((tx + 12, y + 63), "예)", font=font(20, True), fill=CORAL)
        for j, ln in enumerate(lines):
            d.text((tx + 46, y + 64 + 30 * j), ln, font=f_ex, fill=TEXT)
        y += h
        if i < 3:
            cx = bx0 + 75
            d.polygon([(cx - 12, y + 6), (cx + 12, y + 6), (cx, y + 26)], fill=NAVY)
            y += 34
    y += 28
    d.text((PAD, y), "이렇게 쓰세요", font=font(23, True), fill=CORAL); y += 36
    for t in ["숫자와 고유명사를 넣으면 진짜 경험으로 들립니다.",
              "예시는 본인 경험으로 바꾸세요. 그대로 외우면 면접관이 알아봅니다.",
              "한 답변이 60초를 넘기면 잘라내세요. 녹음해서 확인."]:
        d.ellipse([PAD + 4, y + 10, PAD + 12, y + 18], fill=NAVY)
        d.text((PAD + 24, y), t, font=font(20), fill=TEXT); y += 30
    brand(d, W - PAD - 190, H - 52, size=24)
    img.save(out)
    print("structure", out, img.size)


# ================================================================ 작업 목록
def pdf(name):
    return str(SRC / f"m_{name}.pdf")


def jobs_business():
    make_thumb(HERE / "thumb-business.png", "경영학과")
    make_capture(HERE / "kw-2027-biz-track.png", pdf("광운대학교"), 19, "학생부종합【광운참빛인재전형", ("after", "600점/0점"),
                 "광운대학교", "2027학년도 수시모집요강 19쪽", "광운참빛인재전형Ⅰ(면접형) · 경영학부 34명 · 서류 60% + 면접 40%", end_pad=14)
    make_capture(HERE / "kw-2027-biz-interview.png", pdf("광운대학교"), 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】",
                 "광운대학교", "2027학년도 수시모집요강 46쪽", "면접 10분 · 블라인드 · 발전가능성 45% · 종합적사고력 30% · 인성 25%", end_pad=10)
    make_capture(HERE / "sejong-2027-biz-track.png", pdf("세종대학교"), 13, "세종인재", 770,
                 "세종대학교", "2027학년도 수시모집요강 13쪽", "세종인재(면접형) · 경영학부 12명 · 서류 60% + 면접 40% · 면접 9분", end_pad=18)
    make_capture(HERE / "sejong-2027-biz-schedule.png", pdf("세종대학교"), 14, "전형일정", "제출서류",
                 "세종대학교", "2027학년도 수시모집요강 14쪽", "1단계 발표 11월 13일 · 인문계열(경영학부) 면접 11월 22일(일)", start_pad=18, end_pad=14)
    make_structure(HERE / "structure-business.png", [
        "경영학은 한정된 사람과 돈과 시간으로 조직이 목표를 이루게 하는 학문이라고 생각해서 지원했습니다.",
        "학교 축제 부스를 운영하며 재료비 예산 12만 원, 역할 분담 6명, 홍보를 동시에 챙겨야 했습니다.",
        "감으로 하면 재료가 남고 사람이 지친다는 걸 알았고, 원가와 인원을 표로 관리하자 이익률이 18%가 됐습니다.",
        "이 학과에서 마케팅과 조직관리를 체계적으로 배워, 숫자와 사람을 함께 보는 기획자가 되고 싶습니다.",
    ])


def jobs_cs():
    make_thumb(HERE / "thumb-cs.png", "컴퓨터공학과")
    make_capture(HERE / "kw-2027-sw-track.png", pdf("광운대학교"), 24, "학생부종합【소프트웨어우수인재전형】", ("after", "400점/0점"),
                 "광운대학교", "2027학년도 수시모집요강 24쪽", "소프트웨어우수인재전형 · 컴퓨터정보공학부·소프트웨어학부 등 72명 · 서류 60% + 면접 40%", end_pad=14)
    make_capture(HERE / "kw-2027-sw-interview.png", pdf("광운대학교"), 46, "평가방법", ("after", "면접 태도"),
                 "광운대학교", "2027학년도 수시모집요강 46쪽", "면접 10분 · 블라인드 · 발전가능성 45%(소프트웨어 경험의 진정성 포함)", end_idx=-1, end_pad=14, start_pad=2)
    make_capture(HERE / "sm-2027-sw-track.png", pdf("숙명여자대학교"), 20, "가. 모집단위 및 모집인원", "마. 전형요소별 평가방법",
                 "숙명여자대학교", "2027학년도 수시모집요강 16쪽(PDF 20쪽)", "소프트웨어인재전형 · 컴퓨터과학·데이터사이언스 35명 · 면접 11월 28일(토) · 면접 30%", start_pad=16, end_pad=12)
    make_capture(HERE / "sm-2027-sw-interview.png", pdf("숙명여자대학교"), 21, "2) 면접평가", "바. 제출서류",
                 "숙명여자대학교", "2027학년도 수시모집요강 17쪽(PDF 21쪽)", "소프트웨어인재전형 면접 · 평가위원 2인 · 12분 내외 · 블라인드", end_pad=14)
    make_structure(HERE / "structure-cs.png", [
        "직접 만들어 보면서 문제를 쪼개고 해결하는 과정이 가장 재미있어서 컴퓨터공학과에 지원했습니다.",
        "급식 메뉴 알림 봇을 파이썬으로 만들었는데, 학교 홈페이지 구조가 바뀌면 멈추는 문제가 생겼습니다.",
        "위치가 아니라 표의 규칙을 읽도록 바꿔 해결했고, 원인을 찾는 습관이 코드 실력보다 중요하다는 걸 알았습니다.",
        "이 학과에서 자료구조와 운영체제를 제대로 배워, 30명이 아니라 3만 명이 써도 멈추지 않는 서비스를 만들고 싶습니다.",
    ])


def jobs_med():
    make_thumb(HERE / "thumb-med.png", "의예과")
    make_capture(HERE / "ulsan-2027-med-mmi.png", str(SRC / "ulsan.pdf"), 42, "학생부종합형 면접고사", ("after", "면접고사에 참여할 수 없음"),
                 "울산대학교", "2027학년도 수시모집 신입생 모집요강 42쪽", "잠재역량(의예과) · 면접 12월 5일(토) · 다대일 다면평가 · 상황 제시 · 30분 내외 · 500점", end_pad=12)
    make_capture(HERE / "inha-2027-med-interview.png", pdf("인하대학교"), 15, "평가방식 및 진행 방식", "5. 제출서류",
                 "인하대학교", "2027학년도 수시모집요강 12쪽(PDF 15쪽)", "인하미래인재(면접형) 의예과 · 면접실 2개 이동 · 15분 내외 · 서류 기반 블라인드", start_pad=18, end_pad=14)
    make_capture(HERE / "khu-2027-med-schedule.png", pdf("경희대학교"), 41, "5. 전형일정 및 면접평가 상세일정", ("after", "2026. 12. 18(금) 18:00"),
                 "경희대학교", "2027학년도 수시모집요강 39쪽(PDF 41쪽)", "네오르네상스전형 의예과 · 1단계 발표 11월 25일 · 면접 12월 5~6일 · 수능 최저 적용", end_pad=14)
    make_capture(HERE / "khu-2027-med-note.png", pdf("경희대학교"), 42, "[의과대학]", ("after", "“서류확인 면접”만 진행합니다"),
                 "경희대학교", "2027학년도 수시모집요강 40쪽(PDF 42쪽)", "의예과·한의예과·치의예과 면접 12월 6일(일) 14:00 · 출제문항 면접 없이 서류확인 면접만", start_pad=20, end_pad=14)
    make_structure(HERE / "structure-med.png", [
        "환자의 결정을 존중하되, 그 결정이 정확한 정보 위에서 내려졌는지 확인하는 것이 제 책임이라고 생각합니다.",
        "아버지가 응급실에 실려 가셨을 때 의사 선생님이 검사 결과를 하나씩 설명하며 가족을 안심시키던 모습을 봤습니다.",
        "의사의 말 한마디가 환자 가족의 결정을 바꾼다는 것, 그래서 설명도 치료의 일부라는 것을 알았습니다.",
        "이 학과에서 의료 윤리와 소통을 함께 배워, 환자가 이해한 뒤 결정하게 돕는 의사가 되고 싶습니다.",
    ])


def jobs_restyle_previous():
    """이전 편도 같은 디자인으로 다시 뽑기 (썸네일 + 캡처)."""
    make_thumb(HERE / "thumb-nursing.png", "간호학과")
    make_thumb(HERE / "thumb-ece.png", "유아교육과")
    make_capture(HERE / "ulsan-2027-nursing-interview.png", str(SRC / "ulsan.pdf"), 42, "학생부종합형 면접고사", ("after", "면접고사에 참여할 수 없음"),
                 "울산대학교", "2027학년도 수시모집신입생 모집요강 42쪽", "잠재역량(간호학과) · 면접 11월 28일(토) · 다대일 개인면접 10분 이내", end_pad=12)
    make_capture(HERE / "nambu-2027-nursing-interview.png", str(SRC / "nambu.pdf"), 18, "2. 면접고사안내", "3. 학교폭력",
                 "남부대학교", "2027학년도 수시모집 신입생 모집요강 18쪽", "지역인재(간호학과) · 면접 10월 14일(수) · 면접 30% · 다대다 면접", end_pad=10)
    make_capture(HERE / "kangnam-2027-ece-interview.png", pdf("강남대학교"), 26, "학생부종합[학교생활우수자전형2]", ("after", "종합적 사고력 및 의사소통능력"),
                 "강남대학교", "2027학년도 수시모집요강 26쪽", "학교생활우수자전형2 · 유아교육과 20명 · 서류 70% + 면접 30%", start_pad=30, end_pad=16)
    make_capture(HERE / "duksung-2027-ece-interview-criteria.png", pdf("덕성여자대학교"), 73, "모집단위별 평가 방안", ("after", "자기효능감을 판단할 수 있는가"),
                 "덕성여자대학교", "2027학년도 수시모집요강 73쪽", "덕성인재전형Ⅱ · 유아교육과 평가 역량과 면접평가 항목", end_pad=12)
    make_capture(HERE / "duksung-2027-ece-schedule.png", pdf("덕성여자대학교"), 30, "5. 전형일정", "6. 제출서류",
                 "덕성여자대학교", "2027학년도 수시모집요강 30쪽", "덕성인재전형Ⅱ · 유아교육과 면접 2026년 11월 21일(토)")


if __name__ == "__main__":
    jobs_business()
    jobs_restyle_previous()


def jobs_edu():
    make_thumb(HERE / "thumb-edu.png", "교대")
    make_capture(HERE / "snue-2027-edu-interview.png", pdf("서울교육대학교"), 12, "면접평가", "사정원칙",
                 "서울교육대학교", "2027학년도 수시모집 신입생 모집요강 10쪽(PDF 12쪽)", "학교장추천 · 복수 면접위원 심층 문답 · 교직 이해와 태도 / 리더십·자기주도성·문제해결 · 수능 최저", end_pad=10)
    make_capture(HERE / "snue-2027-edu-schedule.png", pdf("서울교육대학교"), 7, "전형일정", "최초 합격자",
                 "서울교육대학교", "2027학년도 수시모집 신입생 모집요강 5쪽(PDF 7쪽)", "1단계 발표 11월 13일(금) · 면접 11월 21일(토) · 최초 합격자 발표 12월 18일(금)")
    make_capture(HERE / "ginue-2027-edu-video.png", pdf("경인교육대학교"), 26, "평가 방법 및 점수", "합격자 사정 및 동점자",
                 "경인교육대학교", "2027학년도 수시모집 신입생 모집요강 24쪽(PDF 26쪽)", "학교장추천 · 비대면 동영상 업로드 면접 · 공개 문항 · Pass/Fail 300점 · 영상 제출 9월 21~23일", end_pad=12)
    make_capture(HERE / "jeju-2027-edu-interview.png", pdf("제주대학교"), 36, "4) 면접평가 방법", ("after", "면접평가 성적이 150점"),
                 "제주대학교", "2027학년도 수시모집요강 31쪽(PDF 36쪽)", "초등교육학부 학생부종합(일반학생) · 면접 12월 4일(금) · 15분 내외 · 150점 미만 과락", start_pad=6, end_pad=10)
    make_structure(HERE / "structure-edu.png", [
        "먼저 그 학생이 왜 그러는지 이유를 찾고, 수업을 방해하지 않는 방식으로 역할을 주겠습니다.",
        "초등학생 방과후 교실 봉사 때, 계속 돌아다니던 아이에게 자료 나눠 주는 역할을 맡기자 집중하기 시작하는 것을 봤습니다.",
        "문제 행동은 혼낼 대상이 아니라 그 아이가 보내는 신호이고, 역할이 생기면 태도가 바뀐다는 것을 배웠습니다.",
        "교대에서 아동 발달과 생활지도를 배워, 아이의 신호를 먼저 읽는 교사가 되고 싶습니다.",
    ])


def jobs_psy():
    make_thumb(HERE / "thumb-psy.png", "심리학과")
    make_capture(HERE / "cau-2027-psy-schedule.png", str(SRC / "cau.pdf"), 27, "다. 전형일정", "경영경제대학",
                 "중앙대학교", "2027학년도 수시모집요강 27쪽", "학생부종합 탐구형인재 · 1단계 발표 11월 26일 · 면접 12월 5~6일 · 심리학과는 4배수, 12월 6일(일)", end_pad=8)
    make_capture(HERE / "cau-2027-psy-interview.png", str(SRC / "cau.pdf"), 95, "2. 면접평가", "나. 평가요소별 세부 내용",
                 "중앙대학교", "2027학년도 수시모집요강 95쪽", "탐구형인재 · 학생부 기반 면접 · 1인당 10분 이내 · 입학사정관 2인 · 수업·탐구활동 중심 개인별 질문", end_pad=10)
    make_capture(HERE / "ajou-2027-psy-ace.png", pdf("아주대학교"), 11, "3. 전형방법", ("after", "면접평가 30%"),
                 "아주대학교", "2027학년도 수시모집요강 9쪽(PDF 11쪽)", "ACE전형 심리학과 14명 · 1단계 서류 3배수 · 2단계 1단계 70% + 면접 30% · 수능 최저 없음", start_pad=16, end_pad=5)
    make_capture(HERE / "kw-2027-psy-interview.png", pdf("광운대학교"), 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】",
                 "광운대학교", "2027학년도 수시모집요강 46쪽", "광운참빛인재Ⅰ 면접형 산업심리학과 8명 · 면접 40% · 10분 이내 · 문제 제시형 없음", start_pad=10, end_pad=6)
    make_structure(HERE / "structure-psy.png", [
        "재미로 쓰는 건 괜찮지만, 사람을 16가지로 나눠 판단하는 도구로 쓰면 위험하다고 생각합니다.",
        "2학년 때 반 친구 30명에게 MBTI를 두 달 간격으로 두 번 검사했는데, 12명의 유형이 바뀌는 것을 봤습니다.",
        "검사가 믿을 만하려면 다시 재도 같은 결과가 나와야 한다는 것(신뢰도), 그래서 심리학이 통계를 배우는 이유를 알았습니다.",
        "심리학과에서 심리측정과 통계를 제대로 배워, 유행하는 검사가 과학적인지 가려낼 수 있는 사람이 되고 싶습니다.",
    ])


def jobs_sw():
    make_thumb(HERE / "thumb-sw.png", "사회복지학과")
    make_capture(HERE / "hansei-2027-sw-interview.png", pdf("한세대학교"), 25, "11. 면접우수자 전형", "┃ 제출서류 ┃",
                 "한세대학교", "2027학년도 수시모집요강 25쪽", "면접우수자(학생부교과) 인문사회학부 30명 · 교과 60% + 면접 40% · 예시 질문 사전 공개 · 수능 최저 없음", end_pad=8)
    make_capture(HERE / "hansei-2027-sw-schedule.png", pdf("한세대학교"), 7, "3. 전형일정", ("after", "※ 개별 통보하지 않음"),
                 "한세대학교", "2027학년도 수시모집요강 7쪽", "면접고사 10월 24~25일(토·일) · 최초 합격자 발표 11월 10일(화) · 수능 전 면접", end_pad=14)
    make_capture(HERE / "dongguk-2027-sw-method.png", pdf("동국대학교"), 19, "1단계 선발배수", "선발원칙 및 동점자 처리기준",
                 "동국대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", "Do Dream 사회복지학과 5명 · 3.5배수 · 면접 30% · 면접위원 2인 10분 내외 · 전공적합성 30%", start_pad=14, end_pad=22)
    make_capture(HERE / "ssu-2027-sw-interview.png", pdf("숭실대학교"), 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"),
                 "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", "SSU미래인재(면접형) 사회복지학부 8명 · 면접 50% · 12분 내외 · 면접 질문 예시 공개", end_pad=12)
    make_capture(HERE / "cau-2027-sw-schedule.png", str(SRC / "cau.pdf"), 27, "다. 전형일정", "경영경제대학",
                 "중앙대학교", "2027학년도 수시모집요강 27쪽", "탐구형인재 사회복지학부 8명 · 1단계 발표 11월 26일 · 4배수 · 면접 12월 5일(토)", end_pad=8)
    make_structure(HERE / "structure-sw.png", [
        "도움을 강요하지 않고, 왜 거부하는지부터 듣겠습니다. 거부도 그분의 권리이기 때문입니다.",
        "독거 어르신 도시락 봉사 때 문을 안 열어 주시던 할아버지가 계셨는데, 3주 동안 문 앞에 두고 인사만 드리자 넷째 주에 문을 열어 주셨습니다.",
        "거부는 도움이 싫어서가 아니라 낯선 사람에게 약한 모습을 보이기 싫어서라는 것, 신뢰가 먼저고 서비스는 그다음이라는 것을 배웠습니다.",
        "사회복지학과에서 사례관리와 상담 기법을 배워, 거부하는 분에게도 끝까지 문을 두드리는 복지사가 되고 싶습니다.",
    ])


def jobs_pt():
    make_thumb(HERE / "thumb-pt.png", "물리치료학과")
    make_capture(HERE / "sunmoon-2027-pt-interview.png", pdf("선문대학교"), 27, "5. 학생부교과(정원내)", ("after", "(입학처 홈페이지)"),
                 "선문대학교", "2027학년도 수시모집요강 27쪽", "학생부교과 면접전형 물리치료학과 14명 · 교과 60% + 면접 40% · 비대면 녹화영상 면접 10월 31일", start_pad=10, end_pad=12, lr=40)
    make_capture(HERE / "sunmoon-2027-pt-video.png", pdf("선문대학교"), 20, "학생부교과 면접전형 평가 및 유의사항", ("after", "불합격 처리함"),
                 "선문대학교", "2027학년도 수시모집요강 20쪽", "비대면 녹화면접 · 사전 공개 문항 중 당일 3개 · 총 3분 · 원본 업로드 · 부적격 시 불합격", start_pad=10, end_pad=10, lr=40)
    make_capture(HERE / "baekseok-2027-pt-interview.png", pdf("백석대학교"), 20, "라. 면접고사", "4) 유의사항",
                 "백석대학교", "2027학년도 수시모집요강 18쪽(PDF 20쪽)", "백석인재(교과 60% + 면접 40%) 물리치료학과 15명 · 10월 15~16일 · 인·적성 구술 · 다대일 5분 내외", end_pad=8)
    make_capture(HERE / "kyungnam-2027-pt-interview.png", str(SRC / "kyungnam.pdf"), 14, "학생부교과(일반면접전형)", 780,
                 "경남대학교", "2027학년도 수시모집요강 14쪽", "일반면접전형 물리치료학과 5명 · 1단계 4배수 · 2단계 60% + 면접 40% · 블라인드 · 평가영역 5개", start_pad=12)
    make_capture(HERE / "eulji-2027-pt-questions.png", pdf("을지대학교"), 18, "라. 전년도(2026학년도) 면접문항 예시", ("after", "마그누스 효과"),
                 "을지대학교", "2027학년도 수시모집요강 18쪽", "EU면접형(학종) 전년도 실제 면접 문항 공개 · '물리치료학과 커리큘럼에서 가장 배우고 싶은 과목은?'", start_pad=10, end_pad=2)
    make_structure(HERE / "structure-pt.png", [
        "포기하려는 환자에게는 '열심히 하세요'가 아니라 어제보다 나아진 것을 숫자로 보여 주겠습니다.",
        "할머니 무릎 수술 후 재활을 따라다녔는데, 한 달째 '안 낫는다'며 운동을 거부하시다 치료사 선생님이 보행 거리를 매일 적어 보여 주자 다시 시작하셨습니다.",
        "환자가 포기하는 이유는 통증보다 '변화가 안 보여서'라는 것, 치료사의 일은 운동을 시키는 것만이 아니라 변화를 보이게 만드는 것임을 배웠습니다.",
        "물리치료학과에서 평가와 측정을 제대로 배워, 환자가 자기 회복을 눈으로 확인하며 끝까지 가게 하는 치료사가 되고 싶습니다.",
    ])


def jobs_mech():
    make_thumb(HERE / "thumb-mech.png", "기계공학과")
    make_capture(HERE / "inha-2027-mech-interview.png", pdf("인하대학교"), 15, "평가방식 및 진행 방식", "5. 제출서류",
                 "인하대학교", "2027학년도 수시모집요강 12쪽(PDF 15쪽)", "인하미래인재(면접형) 기계공학과 · 3.5배수 · 면접 30% · 1개 면접실 8~10분 · 11월 22일(일)", start_pad=18, end_pad=14)
    make_capture(HERE / "kookmin-2027-mech-interview.png", pdf("국민대학교"), 17, "평가방법", 745,
                 "국민대학교", "2027학년도 수시모집요강 15쪽(PDF 17쪽)", "국민프런티어 · 10분 이내 개별 블라인드 · 진로역량 40 · 학업역량 30 · 공동체역량 30", start_pad=30, start_idx=0)
    make_capture(HERE / "kookmin-2027-mech-method.png", pdf("국민대학교"), 19, "4. 전형방법 및 전형요소별 반영비율", ("after", "나. 면접고사에서 ‘F’ 판정"),
                 "국민대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", "국민프런티어 · 1단계 3배수 · 2단계 1단계 70% + 면접 30% · F 판정 시 불합격 · 자연계 면접 11월 21일(토)", end_pad=6)
    make_capture(HERE / "dongguk-2027-mech-method.png", pdf("동국대학교"), 19, "1단계 선발배수", "선발원칙 및 동점자 처리기준",
                 "동국대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", "Do Dream 기계로봇에너지공학과 27명 · 3배수 · 면접 30% · 2인 10분 내외 · 면접 12월 12일(토)", start_pad=14, end_pad=22)
    make_capture(HERE / "cau-2027-mech-schedule.png", str(SRC / "cau.pdf"), 27, "다. 전형일정", "소프트웨어대학",
                 "중앙대학교", "2027학년도 수시모집요강 27쪽", "탐구형인재 기계공학부 15명 · 공과대학 5배수 · 1단계 발표 11월 26일 · 면접 12월 6일(일)", end_pad=6)
    make_structure(HERE / "structure-mech.png", [
        "투석기를 설계해 교내 대회에 나갔는데, 처음 설계는 실패했고 원인을 계산해서 고쳤습니다.",
        "팔 길이를 길게 하면 멀리 갈 줄 알았는데 회전이 느려져 사거리가 줄었고, 팔을 30cm에서 22cm로 줄이자 4m에서 7m로 늘었습니다.",
        "머릿속 설계와 실제 물리는 다르다는 것, 토크와 각속도의 관계를 계산하고 측정해야 한다는 것을 배웠습니다.",
        "기계공학과에서 동역학과 설계를 제대로 배워, 계산으로 먼저 검증하고 만드는 엔지니어가 되고 싶습니다.",
    ])


def jobs_vet():
    make_thumb(HERE / "thumb-vet.png", "수의예과")
    make_capture(HERE / "konkuk-2027-vet-interview.png", pdf("건국대학교"), 30, "나. 면접", ("after", "학교폭력 조치사항 기재 항목에 따른 감점표"),
                 "건국대학교", "2027학년도 수시모집요강 30쪽", "KU자기추천 수의예과 24명 · 3배수 · 면접 30% · 개별면접 10분 · 진로역량 40% · 수능 최저 없음", start_pad=12, end_pad=6)
    make_capture(HERE / "konkuk-2027-vet-schedule.png", pdf("건국대학교"), 31, "7. 전형일정", "8. 제출서류",
                 "건국대학교", "2027학년도 수시모집요강 31쪽", "1단계 발표 11월 20일(금) · 수의과대학 면접 12월 6일(일) · 오전/오후 4타임", end_pad=8)
    make_capture(HERE / "jnu-2027-vet-method.png", pdf("전남대학교"), 40, "다. 전형 방법", "라. 제출 서류",
                 "전남대학교", "2027학년도 수시모집요강 40쪽", "고교생활우수자Ⅰ 수의예과 · 1단계 6배수 · 면접 30% · 수능 최저 3개 합 7 · 기하/미적분·과탐 2과목 필수", start_pad=6, end_pad=8)
    make_capture(HERE / "jnu-2027-vet-interview.png", pdf("전남대학교"), 53, "1. 평가 요소 및 반영 점수", "3. 면접 응시자 유의사항",
                 "전남대학교", "2027학년도 수시모집요강 53쪽", "학생부종합 면접 15분 이내 · 진로·학업역량 180점 + 공동체역량 120점 · F 2인 이상 시 불합격", end_pad=8)
    make_capture(HERE / "cnu-2027-vet-schedule.png", pdf("충남대학교"), 34, "다. 수능최저학력기준", ("after", "동점자 모두 면접대상자로 선발함"),
                 "충남대학교", "2027학년도 수시모집요강 32쪽(PDF 34쪽)", "학생부종합Ⅰ(면접전형) 수의과대학 · 최저 상위 2개 + 수학 합 7 · 과탐 2과목 평균 · 면접 12월 2일(수)", end_pad=8)
    make_capture(HERE / "jeju-2027-vet-interview.png", pdf("제주대학교"), 36, "4) 면접평가 방법", ("after", "면접평가 성적이 150점"),
                 "제주대학교", "2027학년도 수시모집요강 31쪽(PDF 36쪽)", "학생부종합(일반학생) 수의예과 · 3배수 · 면접 30% · 15분 내외 · 150점 미만 과락 · 12월 4일(금)", start_pad=6, end_pad=10)
    make_structure(HERE / "structure-vet.png", [
        "동물을 치료하는 사람이자, 말 못 하는 환자 대신 보호자와 소통하는 사람이 되고 싶어서 지원했습니다.",
        "키우던 고양이가 신부전으로 2년간 투병할 때, 수의사 선생님이 치료보다 저희 가족에게 설명하는 시간이 더 길다는 것을 봤습니다.",
        "수의사는 좋아하는 마음만으로는 부족하고, 살릴 수 없는 결정과 화난 보호자까지 감당해야 하는 직업이라는 것을 배웠습니다.",
        "수의예과에서 내과와 소통을 함께 배워, 그때 저희 가족이 받은 설명과 위로를 다른 가족에게 주는 수의사가 되고 싶습니다.",
    ])
