# 성균관대 학생부종합 과학인재(제시문 기반 수학/과학 교과형 면접)·성균인재 블로그 글 이미지. python jobs_skku.py
# 주의: 성균관대 기출 문항 원문은 상업적 이용·변형·발췌 금지 문서라 도식 예시에 기출 내용을 넣지 않는다(교과서 개념 일반 예시만).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import (HERE, pdf, make_thumb, make_capture, font, wrap_chars, text_fixed, brand,
                         NAVY, PALE, BG, LINE, TEXT, CORAL)

SKKU = pdf("성균관대학교")
U, LBL = "성균관대학교", "2027학년도 수시모집요강"


def make_structure_skku(out, examples, W=1200):
    """promo_style.make_structure 를 복사해 교과형 제시문 면접용 라벨(답·근거·풀이·검토)로 바꾼 것."""
    labels = [("1", "답", "문항이 묻는 값이나 선택을 한 문장으로 먼저"),
              ("2", "근거", "제시문의 어떤 개념·법칙을 쓰는지 이름으로"),
              ("3", "풀이", "식을 세우고 계산 과정을 말로 짚어 가며"),
              ("4", "검토", "다른 조건과 비교하거나 단위로 확인하고 한 줄로 마무리")]
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
    d.text((PAD, 26), "교과형 면접 답변 구조 4단계", font=font(42, True), fill="white")
    d.text((PAD, 82), "소문항마다 이 순서로. 답 하나를 말할 때마다 네 칸을 채웁니다.", font=font(22), fill=PALE)
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
    for t in ["근거는 공식 이름보다 제시문에 적힌 개념으로 대세요. <제시문 1>처럼 번호로 짚으면 분명해집니다.",
              "예시는 교과서 개념(빛의 전반사)으로 만든 연습용 질문입니다. 성균관대 기출 문항이 아닙니다.",
              "말하다가 계산이 틀린 걸 알면 바로 고쳐 말하세요. 고치는 과정도 풀이입니다."]:
        d.ellipse([PAD + 4, y + 10, PAD + 12, y + 18], fill=NAVY)
        text_fixed(d, (PAD + 24, y), t, font(20), TEXT); y += 30
    brand(d, W - PAD - 190, H - 52, size=24)
    img.save(out)
    print("structure", out, img.size)


def jobs_skku():
    make_thumb(HERE / "thumb-skku.png", "성균관대 면접", line2="과학인재·성균인재", line3="교과형 면접 답변법 총정리")
    make_capture(HERE / "skku-2027-science-units.png", SKKU, 34, "1. 모집단위", "2. 지원자격",
                 U, f"{LBL} 32쪽(PDF 34쪽)", "과학인재 155명 · 반도체시스템공학과·공학계열 각 25 · 자연과학계열 20",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "skku-2027-science-method.png", SKKU, 34, "3. 선발방법", ("after", "학교폭력"),
                 U, f"{LBL} 32쪽(PDF 34쪽)", "1단계 학생부 100% 7배수 내외 · 2단계 70 + 면접 30 · 동점 시 면접점수",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "skku-2027-schedule.png", SKKU, 10, "2. 전형별 고사", ("after", "2026. 11. 21."),
                 U, f"{LBL} 8쪽(PDF 10쪽)", "과학인재 1단계 10/27(화) · 면접 11/1(일) · 성균인재는 모집단위별",
                 start_pad=10, end_pad=4)
    make_capture(HERE / "skku-2027-science-interview.png", SKKU, 35, "4. 면접시험 안내", ("after", "admission.skku"),
                 U, f"{LBL} 33쪽(PDF 35쪽)", "11/1(일) 1교시 오전·2교시 오후 · 제시문 기반 수학/과학 교과형",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "skku-2027-talent-method.png", SKKU, 30, "3. 선발방법", ("after", "학교폭력"),
                 U, f"{LBL} 28쪽(PDF 30쪽)", "성균인재 1단계 3~7배수 내외 · 2단계 70 + 면접 30 · 수능최저 없음",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "skku-2027-talent-interview.png", SKKU, 31, "4. 면접시험 안내", ("after", "admission.skku"),
                 U, f"{LBL} 29쪽(PDF 31쪽)", "성균인재 인·적성 면접 · 10/25 · 11/8 · 12/6 모집단위별",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "skku-2027-doc-eval.png", SKKU, 72, "3. 평가 영역", "5. 평가요소",
                 U, f"{LBL} 70쪽(PDF 72쪽)", "학업역량 40 · 탐구역량 40 · 잠재역량 20 · 동점자 우선순위 영역",
                 start_pad=10, end_pad=10)
    make_structure_skku(HERE / "structure-skku.png", [
        "물에서 공기 쪽으로 비춘 빛은 입사각이 임계각보다 크면 전반사되어 공기로 못 나갑니다.",
        "굴절 법칙(n1 sinθ1 = n2 sinθ2)을 씁니다. 굴절률이 큰 물에서 작은 공기로 가는 빛이라 전반사가 일어날 수 있습니다.",
        "물의 굴절률이 공기보다 크니 굴절각이 입사각보다 큽니다. 입사각을 키우면 굴절각이 먼저 직각에 이르고, 이때의 입사각이 임계각입니다. 이보다 크면 굴절할 각이 없어 빛이 모두 반사됩니다.",
        "반대로 공기에서 물로 들어가는 빛은 굴절각이 입사각보다 작아 90°에 이르지 않으니 전반사가 없습니다. 조건을 바꿔 비교해도 결론이 맞습니다.",
    ])


if __name__ == "__main__":
    jobs_skku()
