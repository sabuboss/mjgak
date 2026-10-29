# 스포츠재활학과 학과 글(naver-97) 이미지. python jobs_sportsrehab.py
# 쪽수: 청주대 인쇄 쪽 = PDF 쪽 (PDF 18·19쪽 '- 18 -'·'- 19 -'),
#       광주여대 요강은 쪽번호 인쇄 없음 → PDF 쪽으로 표기 (src/m_광주여자대학교.pdf = dl_dept/speech-therapy/kwu_2027_susi.pdf 복사본),
#       신한대 인쇄 = PDF - 2 (캡처 없음, 본문 쪽수만).
# 새 다운로드 없음.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
from promo_style import HERE, SRC, pdf, make_capture, make_structure
from promo_style import font, wrap_chars, brand, NAVY, NAVY_D, BLUE, PALE, ACCENT, CORAL

LBL = "2027학년도 수시모집요강"


def make_thumb_fit(out, dept, line2="면접 질문 6가지", line3="답변 예시 총정리", chip="2027 수시 면접", size=1080, title_px=104):
    """promo_style.make_thumb 복사본. 학과 이름이 7글자라 118px 제목이 'A' 말풍선과 겹쳐 제목 글자 크기만 줄였다(나머지 동일)."""
    W = H = size
    img = Image.new("RGB", (W, H), NAVY_D)
    d = ImageDraw.Draw(img)
    d.ellipse([W - 420, -180, W + 160, 400], fill=NAVY)
    d.ellipse([-220, H - 360, 300, H + 160], fill=NAVY)

    def bubble(x, y, w, h, fill, letter, lc):
        d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=fill)
        d.polygon([(x + 40, y + h - 2), (x + 90, y + h - 2), (x + 38, y + h + 42)], fill=fill)
        f = font(int(h * 0.62), True)
        d.text((x + w / 2 - d.textlength(letter, font=f) / 2, y + h * 0.12), letter, font=f, fill=lc)
    bubble(W - 300, 150, 150, 120, PALE, "Q", NAVY)
    bubble(W - 210, 300, 150, 120, ACCENT, "A", NAVY_D)
    fc = font(34, True)
    cw = d.textlength(chip, font=fc)
    d.rounded_rectangle([90, 150, 90 + cw + 56, 150 + 64], radius=32, fill=ACCENT)
    d.text((90 + 28, 158), chip, font=fc, fill=NAVY_D)
    y = 330
    f1 = font(title_px, True)
    for ln in wrap_chars(d, dept, f1, W - 180):
        d.text((88, y + (118 - title_px) // 2), ln, font=f1, fill="white"); y += 140
    f2 = font(84, True)
    d.text((88, y + 6), line2, font=f2, fill="white"); y += 130
    f3 = font(60, True)
    tw = d.textlength(line3, font=f3)
    d.rounded_rectangle([88, y, 88 + tw + 48, y + 92], radius=18, fill=CORAL)
    d.text((88 + 24, y + 6), line3, font=f3, fill="white")
    d.line([90, H - 150, W - 90, H - 150], fill=BLUE, width=2)
    brand(d, 90, H - 118, size=40, color="white")
    fs = font(28)
    s = "학과별 · 대학별 면접 무료 정리"
    d.text((W - 90 - d.textlength(s, font=fs), H - 108), s, font=fs, fill=PALE)
    img.save(out)
    print("thumb", out, img.size, "title right edge", 88 + d.textlength(dept, font=f1))
CJU = pdf("청주대학교")
KWU = pdf("광주여자대학교")


def jobs_sportsrehab():
    make_thumb_fit(HERE / "thumb-sportsrehab.png", "스포츠재활학과")
    # 청주대 교과면접전형: 면접 평가영역 3개 · 30%(300/60)
    make_capture(HERE / "cheongju-2027-sportsrehab-interview.png", CJU, 18, "4) 면접고사 반영 및 평가내용", "5) 항공서비스학과",
                 "청주대학교", f"{LBL} 18쪽", "교과면접전형 · 교과 70 + 면접 30 · 면접 평가영역 3가지",
                 start_pad=4, end_pad=12)
    # 청주대 면접고사 일정: 보건의료과학대학 10/17~18 · 고사실 배정 10/2 게시
    make_capture(HERE / "cheongju-2027-sportsrehab-schedule.png", CJU, 19, "6) 면접고사 일정", "※ 주의사항",
                 "청주대학교", f"{LBL} 19쪽", "보건의료과학대학 면접 10월 17일~18일(종료)",
                 start_pad=10, end_pad=8)
    # 광주여대 일반학생전형Ⅰ 면접: 스포츠재활학과 비대면(온라인) · 10/14 · 2인 개별/집단 · 평가 기준 5개
    make_capture(HERE / "kwu-2027-sportsrehab-interview.png", KWU, 14, "2. 면접고사", ("after", "반드시 수험표와 신분증을 지참해야 함"),
                 "광주여자대학교", f"{LBL} PDF 14쪽(쪽번호 인쇄 없음)", "일반학생전형Ⅰ · 스포츠재활학과 비대면(온라인) · 10월 14일",
                 start_pad=4, end_pad=12)
    make_structure(HERE / "structure-sportsrehab.png", [
        "다친 사람이 운동으로 다시 일상과 운동에 돌아가도록 돕고 싶어 스포츠재활학과에 지원했습니다.",
        "체육 시간에 발목을 다친 뒤, 다시 뛰기 전에 균형 운동과 근력 운동을 단계별로 하면서 회복에도 운동 방법이 따로 있다는 것을 알았습니다.",
        "지원 학과 교육과정표를 찾아보니 몸의 구조와 운동의 원리를 배우는 과목부터 실습 과목까지 이어져 있었습니다.",
        "입학하면 그 기초가 되는 몸의 구조부터 정확하게 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_sportsrehab()
