# 가천대 학생부종합 가천바람개비전형 면접 블로그 글(naver-106) 이미지. python jobs_gachon.py
# PDF: src/m_가천대학교.pdf (가천대 입학처 수시 모집요강 게시물 첨부 "2027 가천대학교 수시모집요강(업로드).pdf",
#      admission.gachon.ac.kr/upload/BBS0021/20260901154909TB3M9B.PDF, 104쪽, 2026-08-28 작성).
# 인쇄 쪽수 = PDF 쪽수 (표지가 1쪽).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, make_thumb, make_capture, make_structure, pdf, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

GC = pdf("가천대학교")
U, LBL = "가천대학교", "2027학년도 수시모집요강"


def cap(out, pdf_path, page, box, univ, doc_label, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. box=(x0, y0, x1, y1) PDF 포인트 좌표.
    34쪽 전형일정 표는 오른쪽 '비고' 칸이 여러 행에 걸쳐 있어, 좌우를 따로 잘라야 해서 만든 함수."""
    pg = pymupdf.open(pdf_path)[page - 1]
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(*box))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    W = shot.width + 80
    HEAD, FOOT = 104, 92
    img = Image.new("RGB", (W, HEAD + shot.height + 40 + FOOT), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD], fill=NAVY)
    fc = font(30, True)
    chip = "2027학년도 모집요강"
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 44, 26 + 52], radius=26, fill=ACCENT)
    d.text((40 + 22, 31), chip, font=fc, fill=NAVY_D)
    d.text((40 + cw + 70, 30), univ, font=font(38, True), fill="white")
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    fy = HEAD + shot.height + 40
    text_fixed(d, (40, fy + 10), f"출처: {univ} {doc_label}", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_gachon():
    make_thumb(HERE / "thumb-gachon.png", "가천대 면접", line2="가천바람개비전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "gachon-2027-baram-units.png", GC, 58, "가천바람개비 전형", ("after", "총점 순으로 선발합니다"),
                 U, f"{LBL} 58쪽", "437명 · 1단계 서류 100% 4배수 · 1단계 50 + 면접 50 · 최저 없음",
                 start_pad=10, end_pad=10, lr=28)
    make_capture(HERE / "gachon-2027-baram-schedule.png", GC, 59, "전형일정", ("after", "3. 교과목 이수단위"),
                 U, f"{LBL} 59쪽", "1단계 10/29 · 면접 10/31~11/1, 11/7~11/8 학과별",
                 start_pad=10, end_pad=10, lr=28)
    make_capture(HERE / "gachon-2027-baram-eval.png", GC, 56, "면접평가", ("after", "답하는 학생이라면"),
                 U, f"{LBL} 56쪽", "인성 40 · 진학의지 40 · 의사소통역량 20 · 제시문 없음",
                 start_pad=10, end_pad=24, lr=28)
    make_capture(HERE / "gachon-2027-baram-faq.png", GC, 57, "면접평가 FAQ", ("after", "사전 지식을 평가하는"),
                 U, f"{LBL} 57쪽", "면접위원 3명 : 지원자 1명 · 학업성취도는 면접에 반영 안 함",
                 start_pad=10, end_pad=10, lr=28)
    make_capture(HERE / "gachon-2027-baram-blind.png", GC, 54, "서류평가 평가영역", ("after", "4. 학교폭력조치사항"),
                 U, f"{LBL} 54쪽", "일반면접 · 학생부 기반 질문 · 블라인드, 교복 착용 금지",
                 start_pad=12, end_pad=10, lr=28)
    cap(HERE / "gachon-2027-interview-dates.png", GC, 34, (28, 236, 466, 434),
        U, f"{LBL} 34쪽", "지역균형 12/5~7 · 의예 12/14 · 약학 12/15 · 바람개비 11/7~8")
    make_capture(HERE / "gachon-2027-yakmed.png", GC, 60, "가천의약학 전형", ("after", "총점 순으로 선발합니다"),
                 U, f"{LBL} 60쪽", "의예 16 · 약학 10 · 4배수 · 수능 최저 있음",
                 start_pad=10, end_pad=10, lr=28)
    make_structure(HERE / "structure-gachon.png", [
        "그 활동은 2학년 생명과학Ⅰ 시간에 배운 혈당 조절에서 시작했습니다.",
        "인슐린이 혈당을 낮춘다고 배운 뒤 아침을 거른 날 3교시에 집중이 떨어지는 이유가 궁금해, 친구 열 명과 일주일 동안 아침 식사와 오전 집중도를 기록했습니다.",
        "아침을 먹은 날 집중도 점수가 더 높았지만, 열 명의 기록만으로는 원인을 단정할 수 없다는 것도 함께 배웠습니다.",
        "간호학과에서 환자의 식사와 혈당 관리를 근거를 갖고 설명하는 방법을 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_gachon()
