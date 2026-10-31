# 경찰대학 2027학년도 신입생 2차 시험 면접 블로그 글(naver-117) 이미지. python jobs_police.py
# src/m_경찰대학.pdf = 경찰대학 입학 홈페이지 신입학 모집 > 모집요강 게시물(2026-04-15)
#   「★(최종)2027학년도 경찰대학 신입생 모집요강.pdf」(https://www.police.ac.kr/pds/1776229824677.pdf, 48쪽).
#   인쇄 쪽수 = PDF 쪽수 - 10 (인쇄 1쪽 = PDF 11쪽). PDF 9쪽 「신입생 입학전형」 개요는 인쇄 쪽수 없음.
# src/m_경찰대학_2차시험안내.pdf = 신입학 모집 > 공지사항 「2027학년도 경찰대학 신입생 입학전형 2차 시험 일정 안내」(2026-08-18)
#   첨부 「★(최종)2027학년도 경찰대학 신입생 입학전형 2차 시험 일정 안내.pdf」(https://www.police.ac.kr/pds/1787029539774.pdf, 9쪽).
# 경찰대학 휘장(홀수 쪽 머리)은 캡처 범위에 넣지 않는다.
# 기존 경찰행정학과 글(naver-12)이 thumb-police.png · structure-police.png 를 쓰므로 여기서는 police-univ 를 쓴다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, SRC, make_thumb, make_capture, make_structure, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

P = str(SRC / "m_경찰대학.pdf")
P2 = str(SRC / "m_경찰대학_2차시험안내.pdf")
U, LBL = "경찰대학", "2027학년도 신입생 모집요강"


def cap_notice(out, pdf, page, start, end, doc_label, note, chip="2027학년도 입학 공지", dpi=200,
               start_pad=14, end_pad=6, lr=28):
    """promo_style.make_capture 와 같은 틀에 머리 칩 글자만 바꾼 것(모집요강이 아닌 공지 첨부용)."""
    pg = pymupdf.open(pdf)[page - 1]
    y0 = pg.search_for(start)[0].y0 - start_pad
    y1 = pg.search_for(end[1])[0].y1 + end_pad if isinstance(end, tuple) else pg.search_for(end)[0].y0 - end_pad
    r = pg.rect
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.x0 + lr, y0, r.x1 - lr, y1))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    W = shot.width + 80
    HEAD, FOOT = 104, 92
    img = Image.new("RGB", (W, HEAD + shot.height + 40 + FOOT), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, HEAD], fill=NAVY)
    fc = font(30, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([40, 26, 40 + cw + 44, 26 + 52], radius=26, fill=ACCENT)
    d.text((40 + 22, 31), chip, font=fc, fill=NAVY_D)
    d.text((40 + cw + 70, 30), U, font=font(38, True), fill="white")
    d.rectangle([38, HEAD + 18, 42 + shot.width, HEAD + 22 + shot.height], fill="white", outline=LINE, width=2)
    img.paste(shot, (40, HEAD + 20))
    fy = HEAD + shot.height + 40
    text_fixed(d, (40, fy + 10), f"출처: {U} {doc_label}", font(26), GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


def jobs_police():
    make_thumb(HERE / "thumb-police-univ.png", "경찰대학 면접", line2="2차 시험 총정리", line3="예상 질문 7개 답변법",
               chip="2027학년도 입시")
    make_capture(HERE / "police-2027-overview.png", P, 9, "원서접수", ("after", "(500점)"),
                 U, f"{LBL} 입학전형 개요(PDF 9쪽)", "1차 필기 → 2차 신체·체력·적성 · 면접 → 최종 1,000점",
                 start_pad=12, end_pad=14, lr=46)
    make_capture(HERE / "police-2027-units.png", P, 11, "입학 정원 및 학과 진학", ("after", "2학년 진학 시 결정"),
                 U, f"{LBL} 1쪽(PDF 11쪽)", "일반 44 · 농어촌 3 · 한마음 무궁화 3 · 총 50명",
                 start_pad=12, end_pad=10, lr=24)
    make_capture(HERE / "police-2027-second.png", P, 17, "다. 2차 시험", ("after", "조를 나누어 진행"),
                 U, f"{LBL} 7쪽(PDF 17쪽)", "신체·체력·적성 9/3~9/30 · 면접시험 12/2(수)~12/9(수)",
                 start_pad=10, end_pad=10, lr=24)
    make_capture(HERE / "police-2027-interview.png", P, 22, "다. 면접 시험 성적", ("after", "감점 사유는 면접시험 안내 시"),
                 U, f"{LBL} 12쪽(PDF 22쪽)", "개별 면접 70 · 집단토론 30 · 생활 태도 감점제 · 60점 미만 불합격",
                 start_pad=12, end_pad=12, lr=24)
    cap_notice(HERE / "police-2027-presurvey.png", P2, 3, "사전조사서 및 적성검사 안내", ("after", "면접 시험의 보조자료로 활용"),
               "2차 시험 일정 및 유의사항 안내 3쪽(2026-08-18 공지)", "사전조사서 2문항 · 적성검사 450문항 → 면접 보조자료",
               start_pad=12, end_pad=10, lr=30)
    make_capture(HERE / "police-2027-fitness.png", P, 21, "나. 순환식 체력검사 기준", ("after", "(4.2kg 조끼 미착용)"),
                 U, f"{LBL} 11쪽(PDF 21쪽)", "순환식 체력검사 5분 10초 이하 합격 · 1회만 실시",
                 start_pad=10, end_pad=10, lr=24)
    make_capture(HERE / "police-2027-min.png", P, 25, "2) 수능 및 한국사 최저학력 기준", ("after", "한국사 : 3등급 이내"),
                 U, f"{LBL} 15쪽(PDF 25쪽)", "2개 영역 이상 2등급 이내 + 한국사 3등급 이내",
                 start_pad=10, end_pad=10, lr=24)
    make_structure(HERE / "structure-police-univ.png", [
        "경찰대학에 지원한 이유는 갈등이 커지기 전에 먼저 듣고 정리하는 일이 제게 맞는다는 것을 학교에서 확인했기 때문입니다.",
        "2학년 때 학급 반장으로 청소 구역 다툼을 맡았는데, 두 모둠의 말을 따로 듣고 불만을 표로 적어 보니 쓰레기 버리는 시간 하나가 겹친 것이 원인이었습니다.",
        "시간표를 10분 엇갈리게 바꾸자 다툼이 멈췄고, 누가 옳은지보다 사실을 먼저 확인해야 갈등이 풀린다는 것을 배웠습니다.",
        "경찰대학에서 법과 행정을 체계적으로 배워, 사실을 확인하고 공정하게 판단하는 경찰관이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_police()
