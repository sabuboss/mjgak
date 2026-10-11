# 고려대 학생부종합 계열적합전형(제시문 기반 면접) 블로그 글 이미지. python jobs_ku.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, pdf, make_thumb, make_capture, font, wrap_chars, text_fixed, brand,
                         NAVY, PALE, BG, LINE, TEXT, CORAL)

KU = pdf("고려대학교")
U, LBL = "고려대학교", "2027학년도 수시모집요강"


def make_structure_ku(out, examples, W=1200):
    """promo_style.make_structure 를 복사해 제시문 면접용 라벨(결론·근거·적용·종합)로 바꾼 것."""
    labels = [("1", "결론", "문항이 묻는 것에 대한 답을 한 문장으로 먼저"),
              ("2", "근거", "제시문 어디에서 — (가)·㉠ 같은 기호와 단어를 짚어서"),
              ("3", "적용", "그 근거를 문항이 가리키는 대상에 대입해 설명"),
              ("4", "종합", "한계·조건까지 묶어 한 문장으로 마무리")]
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
    d.text((PAD, 26), "제시문 면접 답변 구조 4단계", font=font(42, True), fill="white")
    d.text((PAD, 82), "문항마다 이 순서로 1분 30초 안팎. 준비 21분 동안 문항별로 이 네 칸을 채웁니다.", font=font(22), fill=PALE)
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
            text_fixed(d, (tx + 46, y + 64 + 30 * j), ln, f_ex, TEXT)
        y += h
        if i < 3:
            cx = bx0 + 75
            d.polygon([(cx - 12, y + 6), (cx + 12, y + 6), (cx, y + 26)], fill=NAVY)
            y += 34
    y += 28
    d.text((PAD, y), "이렇게 쓰세요", font=font(23, True), fill=CORAL); y += 36
    for t in ["배경지식보다 제시문 속 단어로 말하세요. 근거는 기호로 짚으면 분명해집니다.",
              "예시는 2026학년도 인문계열(오후) 기출 문항 1을 이 구조로 쪼갠 것입니다.",
              "말하다가 틀린 걸 알면 바로 고쳐 말하세요. 고치는 것도 사고력입니다."]:
        d.ellipse([PAD + 4, y + 10, PAD + 12, y + 18], fill=NAVY)
        text_fixed(d, (PAD + 24, y), t, font(20), TEXT); y += 30
    brand(d, W - PAD - 190, H - 52, size=24)
    img.save(out)
    print("structure", out, img.size)


def jobs_ku():
    make_thumb(HERE / "thumb-ku.png", "고려대 면접", line2="계열적합전형", line3="제시문 기출 유형 총정리")
    make_capture(HERE / "ku-2027-fit-units.png", KU, 4, "전형별 모집단위 및 모집인원", 543,
                 U, f"{LBL} 4쪽", "계열적합 523명(합계 5쪽) · 경영학과 48 · 경제학과 15 · 영어영문학과 12", start_pad=10)
    make_capture(HERE / "ku-2027-fit-method.png", KU, 15, "2. 대학수학능력시험", ("after", "(1단계 성적이 동일한 경우 모두 선발)"),
                 U, f"{LBL} 15쪽", "수능최저 없음 · 1단계 서류 100%로 5배수 · 2단계 1단계 60% + 면접 40%", start_pad=10, end_pad=12)
    make_capture(HERE / "ku-2027-fit-schedule.png", KU, 9, "전형별 일정", ("after", "(자세한 내용은 입학처 홈페이지 참고)"),
                 U, f"{LBL} 9쪽", "계열적합 1단계 10/30(금) 17:00 · 면접 11/7(토) 인문, 11/8(일) 자연", start_pad=10, end_pad=10)
    make_capture(HERE / "ku-2027-fit-dates.png", KU, 15, "4. 면접 안내", ("after", "변경될 수 있음"),
                 U, f"{LBL} 15쪽", "인문 11/7(토) · 자연 11/8(일) · 모집단위별 08:00 또는 13:20까지 입실", start_pad=10, end_pad=10)
    make_capture(HERE / "ku-2027-fit-time.png", KU, 29, "2. 전형별 면접평가 진행방식", ("after", "지구과학"),
                 U, f"{LBL} 29쪽", "준비 21분 · 면접 7분 제시문 기반 · 의학과는 MMI Ⅰ·Ⅱ 각 8분 추가", start_pad=10, end_pad=12, end_idx=-1)
    make_capture(HERE / "ku-2027-fit-criteria.png", KU, 30, "4. 전형별 면접평가 내용 및 요소", 293,
                 U, f"{LBL} 30쪽", "분석력 20% + 적용력 30% + 종합적 사고력 40% + 면접태도 10%", start_pad=10)
    make_capture(HERE / "ku-2027-fit-blind.png", KU, 27, "2. 면접, 논술고사 시 수험생 유의사항", ("after", "불합격 처리됨"),
                 U, f"{LBL} 27쪽", "교복·교표 등 출신고교가 드러나는 복장은 불합격 · 가번호 부여", start_pad=10, end_pad=10)
    make_structure_ku(HERE / "structure-ku.png", [
        "(나)의 ㉠ 주장은 (가)와 같은 오류, 즉 함께 변한 두 현상을 원인과 결과로 단정한 오류를 범하고 있습니다.",
        "(가)에서 아이스크림 판매량과 익사 사고가 함께 늘어난 것은 여름이라는 다른 요인 때문인데, 연구자 A는 이를 인과관계로 읽었습니다.",
        "(나)의 B국 정부도 C광역시의 정책 시행 전후 사망 건수만 비교했을 뿐, 같은 기간 다른 요인으로 사고가 줄었을 가능성은 따지지 않았습니다.",
        "따라서 ㉠만으로는 정책 효과를 단정할 수 없고, 정책을 시행하지 않은 지역의 변화와 비교해 봐야 효과를 말할 수 있습니다.",
    ])


if __name__ == "__main__":
    jobs_ku()
