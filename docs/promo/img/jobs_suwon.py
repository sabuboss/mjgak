# 수원대 학생부교과 고교추천전형 면접 블로그 글(naver-113) 이미지. python jobs_suwon.py
# PDF: src/m_수원대학교.pdf (2027 수원대학교 신입생 모집요강_수시모집, 88쪽, PDF 정보상 2026-04-10 작성·2026-05-06 수정).
# 인쇄 쪽수 = PDF 쪽수. 글자 층이 있어 문구 검색(make_capture)을 쓰고,
# 세로쓰기 머리글이 있는 표(16·18·25쪽)는 jobs_dau.py 의 cap() 을 복사해 좌표로 자른다(110dpi 픽셀).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import (HERE, make_thumb, make_capture, make_structure, pdf, font, text_fixed,
                         BG, NAVY, NAVY_D, ACCENT, LINE, GRAY)

SW = pdf("수원대학교")
U, LBL = "수원대학교", "2027학년도 수시모집요강"
PX = 72 / 110  # 110dpi 픽셀 -> PDF 포인트


def cap(out, page, box, doc_label, note, dpi=200):
    """promo_style.make_capture 와 같은 틀. box=(x0, y0, x1, y1) 110dpi 픽셀."""
    pg = pymupdf.open(SW)[page - 1]
    x0, y0, x1, y1 = (v * PX for v in box)
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
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


def jobs_suwon():
    make_thumb(HERE / "thumb-suwon.png", "수원대 면접", line2="고교추천전형", line3="질문 7개 총정리")
    make_capture(HERE / "suwon-2027-gochu-method.png", SW, 33, "지원자격", ("after", "지원자 전원 대학수학능력시험 이후 면접고사 실시"),
                 U, f"{LBL} 33쪽", "115명 · 학생부 51.7 + 면접 48.3(실질) · 최저 1개 영역 4등급",
                 start_pad=10, end_pad=8, lr=32)
    cap(HERE / "suwon-2027-gochu-units.png", 16, (106, 300, 684, 1213),
        f"{LBL} 16쪽", "고교추천 115명: 자유전공 15 · 인문사회융합 15 · 경영공학 10 등")
    make_capture(HERE / "suwon-2027-gochu-interview.png", SW, 34, "면접고사 방법", ("after", "예비소집은 따로 실시하지 않음"),
                 U, f"{LBL} 34쪽", "그룹면접(학생 3명 이내) · 1분 이내 자기소개로 시작",
                 start_pad=10, end_pad=8, lr=32)
    make_capture(HERE / "suwon-2027-gochu-schedule.png", SW, 34, "면접고사 전형일시", ("after", "본교 입학홈페이지 공고)"),
                 U, f"{LBL} 34쪽", "면접 11/27(금)~29(일) 중 지정 · 발표 12/18(금) 17시 이전",
                 start_pad=10, end_pad=8, lr=32)
    make_capture(HERE / "suwon-2027-rules.png", SW, 12, "1. 논술/면접/실기고사의 일정은", ("after", "차질이 없도록 하여야 한다"),
                 U, f"{LBL} 12쪽", "개별 통보 없음 · 지정일시 변경 불가 · 수험표 없으면 입실 불가",
                 start_pad=40, end_pad=8, lr=32)
    cap(HERE / "suwon-2027-tie.png", 25, (106, 588, 684, 793),
        f"{LBL} 25쪽", "동점자: 면접 총점 → 인성 → 전공적합성 등 6단계")
    cap(HERE / "suwon-2027-schedule-all.png", 18, (106, 590, 684, 716),
        f"{LBL} 18쪽", "면접위주교과 10/9~11 · 고교추천 11/27~29")
    make_structure(HERE / "structure-suwon.png", [
        "안녕하세요, 작은 변화도 기록해서 살피는 지원자입니다.",
        "2학년 보건 동아리에서 교실 이산화 탄소 농도를 쉬는 시간마다 재어 기록했는데, 창문을 닫고 수업한 4교시 뒤에 값이 가장 높았습니다.",
        "결과를 보여 드리고 쉬는 시간마다 창문을 여는 당번을 정했고, 기록이 있어야 사람들이 움직인다는 것을 배웠습니다.",
        "간호학과에서 환자의 상태를 꼼꼼히 관찰하고 기록하는 법을 배워 믿을 수 있는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_suwon()
