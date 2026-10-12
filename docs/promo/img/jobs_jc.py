# 전문대 면접 질문 6가지 블로그 글(naver-47) 이미지. python jobs_jc.py
# 전문대 모집요강은 CDN 에 없어 각 대학 입학 홈페이지에서 받은 PDF(src/m_<학교명>.pdf)를 쓴다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, pdf, make_thumb, make_capture, make_structure,
                         font, text_fixed, NAVY, NAVY_D, BG, LINE, GRAY, ACCENT)

YJU = pdf("영진전문대학교")
INHATC = pdf("인하공업전문대학")
DSU = pdf("동서울대학교")
DSU_AIR = pdf("동서울대학교_항공서비스학과_면접")
SHU = pdf("삼육보건대학교")


def cap_rect(out, pdf_path, page, y0, y1, univ, doc_label, note, dpi=200, lr=28):
    """글자 레이어가 없는(이미지로 된) PDF 쪽을 y 좌표로 잘라 make_capture 와 같은 틀에 넣는다.
    promo_style.make_capture 의 틀 그리기 부분을 그대로 옮긴 것(검색 대신 좌표만 다름)."""
    pg = pymupdf.open(pdf_path)[page - 1]
    r = pg.rect
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.x0 + lr, y0, r.x1 - lr, y1))
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
    print("capture(rect)", out, img.size)


def jobs_jc():
    make_thumb(HERE / "thumb-jc.png", "전문대 면접", line2="질문 6가지", line3="수시 2차 답변 예시", chip="2027 전문대 수시")

    # 영진전문대학교 2027학년도 수시모집 안내(인쇄 쪽수 = PDF 쪽수 - 2)
    U, L = "영진전문대학교", "2027학년도 신입생 수시모집 안내"
    make_capture(HERE / "yju-2027-jc-method.png", YJU, 17, "1. 성적반영 및 동점자 처리기준", ("after", "수능최저(2개 과목 합 10등급 이내)"),
                 U, f"{L} 15쪽(PDF 17쪽)", "면접전형 내신 200 + 면접 300 · 인성적·사회적·전문적역량 각 90점", start_pad=8, end_pad=8)
    make_capture(HERE / "yju-2027-jc-schedule.png", YJU, 12, "1. 전형일정", ("after", "합격조회에서 확인 가능"),
                 U, f"{L} 10쪽(PDF 12쪽)", "수시1차 면접 10/10~11 · 수시2차 면접 12/5(토) · 발표 12/10", start_pad=8, end_pad=3)
    make_capture(HERE / "yju-2027-jc-rule.png", YJU, 17, "2. 면접/실기 안내", "나. 실기전형 방법 안내",
                 U, f"{L} 15쪽(PDF 17쪽)", "1차 면접 응시 후 같은 학과 2차 지원 시 면접 면제, 1차 점수 반영", start_pad=8, end_pad=6)

    # 인하공업전문대학 2027학년도 입학전형 신입생 모집요강(수시·정시) (인쇄 쪽수 = PDF 쪽수 - 1)
    U, L = "인하공업전문대학", "2027학년도 신입생 모집요강"
    make_capture(HERE / "inhatc-2027-jc-schedule.png", INHATC, 5, "전형일정", 345,
                 U, f"{L} 4쪽(PDF 5쪽)", "수시1차 면접 10/16~18 · 수시2차 원서 11/11~25, 면접 12/11~13", start_pad=8, end_pad=10)
    make_capture(HERE / "inhatc-2027-jc-interview.png", INHATC, 5, "면접고사", 571,
                 U, f"{L} 4쪽(PDF 5쪽)", "수시 면접 4개 학과 · 항공 계열 흰색 반팔 티셔츠 · 예약은 선착순", start_pad=8, end_pad=8, start_idx=1)
    make_capture(HERE / "inhatc-2027-jc-score.png", INHATC, 12, "산출방법", 284,
                 U, f"{L} 11쪽(PDF 12쪽)", "학과 적성 · 발표 및 표현력 · 인성 및 태도, A~D 4등급", start_pad=8, end_pad=8)

    # 동서울대학교 — 항공서비스학과 수시1차 면접 유의사항(입학 홈페이지 공지 첨부) + 2027 신입생 입학안내(이미지 PDF)
    U = "동서울대학교"
    make_capture(HERE / "dongseoul-2027-jc-eval.png", DSU_AIR, 2, "5. 고사장 입장 시", ("after", "총점 600점"),
                 U, "2027 수시1차 항공서비스학과 면접 유의사항 2쪽", "5명 1조 10분 이내 · 학생부 320 + 출결 80 + 면접 600", start_pad=8, end_pad=10)
    make_capture(HERE / "dongseoul-2027-jc-questions.png", DSU_AIR, 3, "7. 면접 예상질문", "※ 항공서비스학과 학과 사무실",
                 U, "2027 수시1차 항공서비스학과 면접 유의사항 3쪽", "대학이 공개한 면접 예상질문 11개", start_pad=8, end_pad=4)
    cap_rect(HERE / "dongseoul-2027-jc-schedule.png", DSU, 15, 440, 800,
             U, "2027 신입생 입학안내 15쪽", "수시1차 면접 10/15~25 · 수시2차 원서 11/11~25, 면접 12/2~8")

    # 삼육보건대학교 2027학년도 수시·정시 모집요강 (인쇄 쪽수 = PDF 쪽수 - 2)
    U, L = "삼육보건대학교", "2027학년도 수시·정시 모집요강"
    make_capture(HERE / "shu-2027-jc-method.png", SHU, 32, "1. 전형 요약", ("after", "(대학자체/비교과)"),
                 U, f"{L} 30쪽(PDF 32쪽)", "수시1차 일반·일반고/특성화고특별은 학생부 100% · 면접은 일부 전형만", start_pad=8, end_pad=3)
    make_capture(HERE / "shu-2027-jc-schedule.png", SHU, 35, "구분", ("after", "면접 미응시자는 불합격"),
                 U, f"{L} 33쪽(PDF 35쪽)", "면접 10/16 · 12/4 · 지원자가 모집정원을 넘을 때만 면접", start_pad=10, end_pad=5)

    make_structure(HERE / "structure-jc.png", [
        "간호학과에 지원한 이유는 아픈 사람 곁에서 가장 오래 머무는 사람이 간호사라는 것을 직접 보았기 때문입니다.",
        "고2 겨울 할머니가 2주 입원하셨을 때 간호사 선생님이 밤마다 수액과 체온을 확인하고 할머니가 알아듣게 약 이름을 천천히 다시 설명해 주는 모습을 봤습니다.",
        "그때 간호는 주사를 놓는 기술만이 아니라 환자의 상태를 계속 살피고 설명하는 일이라는 것을 알았고, 그 뒤로 생명과학 시간에 배우는 내용을 몸의 변화와 연결해 보게 됐습니다.",
        "입학하면 기본간호학과 해부생리학을 먼저 단단히 익혀, 환자에게 설명을 잘하는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_jc()
