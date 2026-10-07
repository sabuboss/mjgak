# 그룹 C(예체능·K): 체육학과·디자인학과·K-POP실용음악과·뷰티학과 블로그 이미지. python jobs_b5_C.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw
import pymupdf
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure, font, NAVY, NAVY_D, ACCENT, BG, LINE, GRAY

KHU = pdf("경희대학교"); INHA = pdf("인하대학교"); KMU = pdf("국민대학교"); EWHA = pdf("이화여자대학교"); MJU = pdf("명지대학교")
SKU = pdf("성결대학교"); BS = pdf("백석대학교"); SH = pdf("신한대학교")
NAMBU = str(SRC / "nambu.pdf"); SS = pdf("성신여자대학교"); EU = pdf("을지대학교")


def cap_x(out, pdf_path, page, start, end, univ, doc_label, note, x0f=0.0, x1f=1.0, dpi=200, start_pad=14, end_pad=6, start_idx=0, end_idx=0):
    """promo_style.make_capture 와 같은 틀. 다만 좌우 범위를 쪽 너비 비율(x0f~x1f)로 잘라 2단 표의 한쪽만 담는다."""
    pg = pymupdf.open(pdf_path)[page - 1]
    y0 = pg.search_for(start)[start_idx].y0 - start_pad
    if isinstance(end, tuple) and end[0] == "after":
        y1 = pg.search_for(end[1])[end_idx].y1 + end_pad
    elif isinstance(end, str):
        y1 = pg.search_for(end)[0].y0 - end_pad
    else:
        y1 = end
    r = pg.rect
    pix = pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.x0 + r.width * x0f, y0, r.x0 + r.width * x1f, y1))
    shot = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    W = max(shot.width + 80, 1400)
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
    d.text((40, fy + 10), f"출처: {univ} {doc_label}", font=font(26), fill=GRAY)
    d.text((40, fy + 48), note, font=font(26, True), fill=NAVY)
    fb = font(26, True)
    d.text((W - 40 - d.textlength("면접각 mjgak.com", font=fb), fy + 48), "면접각 mjgak.com", font=fb, fill=GRAY)
    img.save(out)
    print("capture", out, img.size)


# ---------------------------------------------------------------- 공통 헬퍼
def khu_count(out, note):
    cap_x(out, KHU, 39, "산업디자인학과", ("after", "1,076"), "경희대학교", "2027학년도 수시모집요강 37쪽(PDF 39쪽)", note,
          x0f=0.5, x1f=0.96, start_pad=1.2, end_pad=10)


def khu_method(out, note):
    make_capture(out, KHU, 40, "3. 전형 방법", "※ 서류평가 및 면접평가 안내는", "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", note, start_pad=10, end_pad=8)


def khu_schedule42(out, note):
    make_capture(out, KHU, 42, "[면접평가 상세일정]", "<인문계열·자율전공학부>", "경희대학교", "2027학년도 수시모집요강 40쪽(PDF 42쪽)", note, start_pad=10, end_pad=8)


def khu_interview(out):
    make_capture(out, KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적", "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)",
                 "공통질문 + 서류확인 면접 · 출제문항 없음 · 2:1 개인면접 10분 · 인성 50% + 전공적합성 50%", start_pad=10, end_pad=8)


def kmu_method(out, note):
    make_capture(out, KMU, 19, "4. 전형방법 및 전형요소별 반영비율", ("after", "나. 면접고사에서 ‘F’ 판정"),
                 "국민대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", note, end_pad=6)


def kmu_interview(out):
    make_capture(out, KMU, 17, "나. 면접평가", ("after", "협업과 소통 능력"), "국민대학교", "2027학년도 수시모집요강 15쪽(PDF 17쪽)",
                 "국민프런티어 · 10분 이내 개별 블라인드 · 진로역량 40 · 학업역량 30 · 공동체역량 30", start_pad=10, end_pad=10)


def ewha_method(out, note):
    cap_x(out, EWHA, 34, "학생부종합[예체능서류전형]", ("after", "제2외국어/한문은 탐구영역의 한 과목으로 인정하지 않음"),
          "이화여자대학교", "2027학년도 수시모집요강 35쪽(PDF 34쪽)", note, x0f=0.065, x1f=0.925, start_pad=12, end_pad=10)


def ewha_interview(out, note):
    make_capture(out, EWHA, 39, "나. 예체능서류전형(디자인학부/체육과학부)", ("after", "질적으로 더 높은 단계로 향상될 가능성"),
                 "이화여자대학교", "2027학년도 수시모집요강 40쪽(PDF 39쪽)", note, start_pad=2.5, end_pad=10, end_idx=-1)


def ewha_schedule(out, note):
    make_capture(out, EWHA, 8, "2. 전형별 고사 및 합격자 발표 일정", ("after", "체육과학부"),
                 "이화여자대학교", "2027학년도 수시모집요강 9쪽(PDF 8쪽)", note, start_pad=4, end_pad=10, lr=36)


def inha_method(out, note):
    make_capture(out, INHA, 14, "3. 전형 방법", ("after", "스포츠과학과, 의류디자인학과(일반)"),
                 "인하대학교", "2027학년도 수시모집요강 11쪽(PDF 14쪽)", note, start_pad=10, end_pad=4.5)


def inha_interview(out, note):
    make_capture(out, INHA, 15, "평가방식 및 진행 방식", "5. 제출서류", "인하대학교", "2027학년도 수시모집요강 12쪽(PDF 15쪽)", note, start_pad=18, end_pad=14)


def mju_track(out, note):
    make_capture(out, MJU, 49, "학생부종합(명지인재면접전형)", ("after", "면접고사는 서울(인문캠퍼스)에서 진행"),
                 "명지대학교", "2027학년도 수시모집요강 47쪽(PDF 49쪽)", note, start_pad=10, end_pad=2)


def mju_interview(out, note):
    make_capture(out, MJU, 50, "4. 전형방법", ("after", "자기주도성, 도전정신"), "명지대학교", "2027학년도 수시모집요강 48쪽(PDF 50쪽)", note, start_pad=10, end_pad=8)


# ---------------------------------------------------------------- 30 체육학과
def jobs_pe():
    make_thumb(HERE / "thumb-pe.png", "체육학과")
    khu_count(HERE / "khu-2027-pe-count.png", "네오르네상스 체육학과 16·스포츠의학과 11·골프산업학과 4·태권도학과 12명")
    khu_method(HERE / "khu-2027-pe-method.png", "1단계 서류 100% 3배수 · 2단계 70% + 면접 30% · 체육대학 수능 최저 없음")
    khu_schedule42(HERE / "khu-2027-pe-schedule.png", "1단계 발표 11월 25일 · 체육대학 면접 12월 5일(토) 09:00~13:00 국제캠퍼스")
    inha_method(HERE / "inha-2027-pe-method.png", "인하미래인재(면접형) 스포츠과학과 23명 · 3.5배수 · 70% + 면접 30% · 11월 21일")
    inha_interview(HERE / "inha-2027-pe-interview.png", "2:1 개별 · 서류 기반 블라인드 · 8~10분 · 기초학업·진로탐구·의사소통역량")
    kmu_method(HERE / "kookmin-2027-pe-method.png", "국민프런티어 스포츠건강재활학과 19명 · 3배수 · 70% + 면접 30% · F면 불합격")
    kmu_interview(HERE / "kookmin-2027-pe-interview.png")
    ewha_method(HERE / "ewha-2027-pe-method.png", "예체능서류 체육과학부 15명 · 4배수 · 80% + 면접 20% · 최저 3개 합 9")
    ewha_interview(HERE / "ewha-2027-pe-interview.png", "면접 평가요소 자기주도성 · 전공 잠재력 · 발전가능성 · 면접 11월 21일(토)")
    make_structure(HERE / "structure-pe.png", [
        "체육학과는 운동을 잘하는 법만이 아니라, 몸이 왜 그렇게 움직이는지를 운동생리학·역학·심리학으로 설명하는 곳이라 지원했습니다.",
        "고2 때 축구부 친구들의 체력 기록을 6주 동안 정리했는데, 같은 훈련을 해도 회복 속도가 사람마다 달라서 수면 시간과 함께 비교해 봤습니다.",
        "훈련은 많이 하는 것보다 몸의 반응을 재고 조절하는 것이 중요하고, 그 근거가 과학이라는 것을 배웠습니다.",
        "체육학과에서 운동생리학과 측정평가를 제대로 배워, 데이터로 훈련을 설계하는 트레이너가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 31 디자인학과
def jobs_design():
    make_thumb(HERE / "thumb-design.png", "디자인학과")
    khu_count(HERE / "khu-2027-design-count.png", "네오르네상스 산업디자인 3·시각디자인 8·환경조경 10·의류디자인 6·디지털콘텐츠 3")
    khu_schedule42(HERE / "khu-2027-design-schedule.png", "1단계 발표 11월 25일 · 예술·디자인대학 면접 12월 5일(토) 09:00 국제캠퍼스")
    khu_interview(HERE / "khu-2027-design-interview.png")
    kmu_method(HERE / "kookmin-2027-design-method.png", "국민프런티어 시각디자인 10·AI디자인 15명 · 3배수 · 70% + 면접 30%")
    kmu_interview(HERE / "kookmin-2027-design-interview.png")
    ewha_method(HERE / "ewha-2027-design-method.png", "예체능서류 디자인학부 24명 · 4배수 · 80% + 면접 20% · 최저 2개 합 7")
    ewha_schedule(HERE / "ewha-2027-design-schedule.png", "디자인학부 1단계 발표 11월 12일 · 면접 11월 21일(토) · 최종 12월 17일")
    mju_track(HERE / "mju-2027-design-track.png", "명지인재면접 디지털콘텐츠디자인 6·공간디자인 6명 · 면접 11월 28~29일")
    mju_interview(HERE / "mju-2027-design-interview.png", "4배수 · 70% + 면접 30% · 심층면접 약 10분 · 진로역량 40% · 최저 없음")
    make_structure(HERE / "structure-design.png", [
        "제 대표작은 학교 분리수거장 안내판인데, 예쁘게 만드는 것보다 1학년이 3초 안에 알아보게 만드는 것이 목표였습니다.",
        "처음엔 글씨로 품목을 적었더니 아무도 안 읽어서, 친구 20명에게 보여 주고 헷갈린 곳을 표시하게 한 뒤 색과 그림 위주로 세 번 고쳤습니다.",
        "디자인은 내 취향을 보여 주는 것이 아니라 쓰는 사람의 행동을 바꾸는 것이고, 그 답은 관찰과 수정에서 나온다는 것을 배웠습니다.",
        "디자인학과에서 사용자 조사와 시각 커뮤니케이션을 제대로 배워, 사람이 헤매지 않게 만드는 디자이너가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 38 K-POP·실용음악과
def jobs_kpop():
    make_thumb(HERE / "thumb-kpop.png", "실용음악과")
    make_capture(HERE / "sungkyul-2027-kpop-method.png", SKU, 40, "모집단위", ("after", "성적 반영방법은 p.50"),
                 "성결대학교", "2027학년도 수시모집요강 40쪽", "실기우수자 실용음악예술학과 25명 · 학생부교과 20% + 실기 80% · 최저 없음", start_pad=12, end_pad=10, lr=60)
    make_capture(HERE / "sungkyul-2027-kpop-qa.png", SKU, 43, "가. 실기 방법", "※ MR 사용 안내",
                 "성결대학교", "2027학년도 수시모집요강 43쪽", "보컬·작곡·기악·뮤직테크놀로지 실기에 질의응답 포함 · 실기 10월 9일(금)", start_pad=12, end_pad=8, lr=60)
    make_capture(HERE / "baekseok-2027-kpop-method.png", BS, 51, "실기위주 : 문화예술학부(실용음악)", ("after", "환산점수(점)"),
                 "백석대학교", "2027학년도 수시모집요강 49쪽(PDF 51쪽)", "실용음악 일반실기 77명 · 학생부교과 20% + 실기 80% · 수능 최저 없음", start_pad=12, end_pad=14)
    make_capture(HERE / "baekseok-2027-kpop-qa.png", BS, 52, "라. 실기고사", ("after", "기초적 뮤직비즈니스 관련 지식에 대한 문답"),
                 "백석대학교", "2027학년도 수시모집요강 50쪽(PDF 52쪽)", "실기 10월 15~20일 · 음향엔지니어링·프로페셔널뮤직은 지식 문답 포함", start_pad=12, end_pad=10)
    make_capture(HERE / "shinhan-2027-kpop-method.png", SH, 44, "실기우수자전형(실기위주)", ("after", "※ 학교생활기록부 반영방법 P.74 참고"),
                 "신한대학교", "2027학년도 수시모집요강 42쪽(PDF 44쪽)", "실기우수자 K-POP학과 15명 · 실기 80% + 학생부교과 20% · 실기 10월 26~30일", start_pad=12, end_pad=10)
    make_capture(HERE / "shinhan-2027-kpop-qa.png", SH, 48, "다. K-POP학과", "라. 태권도학부",
                 "신한대학교", "2027학년도 수시모집요강 46쪽(PDF 48쪽)", "보컬·댄스·기악·뮤직프로듀싱 각 2분 이내 · 뮤직프로듀싱은 질의응답 포함", start_pad=12, end_pad=10)
    make_structure(HERE / "structure-kpop.png", [
        "실용음악과는 보컬 한 분야를 깊게 파는 곳이고, 저는 노래와 춤과 무대 표현을 한 몸으로 하는 아티스트가 되고 싶어 K-POP 전공을 택했습니다.",
        "고1부터 커버댄스 팀에서 3년 활동하며 보컬 레슨을 병행했는데, 공연 영상을 다시 보면 춤이 격해지는 부분에서 음정이 늘 흔들렸습니다.",
        "노래와 춤을 따로 연습해서는 무대가 완성되지 않고, 호흡까지 같이 설계해야 한다는 것을 배웠습니다.",
        "이 학과에서 보컬과 퍼포먼스를 함께 훈련해, 라이브에서도 흔들리지 않는 무대를 만드는 아티스트가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 39 뷰티학과
def jobs_beauty():
    make_thumb(HERE / "thumb-beauty.png", "뷰티학과")
    make_capture(HERE / "nambu-2027-beauty-method.png", NAMBU, 8, "1. 학생부교과(일반학생)", ("after", "무도경호학과"),
                 "남부대학교", "2027학년도 수시모집요강 8쪽", "일반학생 향장미용학과 25명 · 학생부 70% + 면접 30% · 수능 최저 없음", start_pad=12, end_pad=10)
    make_capture(HERE / "nambu-2027-beauty-interview.png", NAMBU, 18, "2. 면접고사안내", "3. 학교폭력 조치 반영 방법",
                 "남부대학교", "2027학년도 수시모집요강 18쪽", "면접 10월 14일(수) · 다대다 면접 · 지원동기·학과 관심도·인성·진로·태도", start_pad=12, end_pad=10)
    make_capture(HERE / "baekseok-2027-beauty-track.png", BS, 19, "학생부위주(정원 내) : 학생부교과 60% + 면접 40%", ("after", "환산점수(점)"),
                 "백석대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", "백석인재 문화예술학부 글로벌뷰티아트 3명 · 교과 60% + 면접 40% · 최저 없음", start_pad=12, end_pad=14)
    make_capture(HERE / "baekseok-2027-beauty-interview.png", BS, 20, "라. 면접고사", "4) 유의사항",
                 "백석대학교", "2027학년도 수시모집요강 18쪽(PDF 20쪽)", "글로벌뷰티아트 면접 10월 16일(금) · 2:1 5분 내외 · 인·적성 문제로 출제", start_pad=12, end_pad=10)
    make_capture(HERE / "sungshin-2027-beauty-method.png", SS, 17, "학생부종합(자기주도인재전형)", ("after", "면접평가 안내(p.40) 참조"),
                 "성신여자대학교", "2027학년도 수시모집요강 16쪽(PDF 17쪽)", "자기주도인재 뷰티산업학과 5명 · 3배수 · 서류 60% + 면접 40% · 최저 없음", start_pad=12, end_pad=10)
    make_capture(HERE / "sungshin-2027-beauty-interview.png", SS, 41, "면접평가 안내", "2. 전형별 평가항목 및 반영비율",
                 "성신여자대학교", "2027학년도 수시모집요강 40쪽(PDF 41쪽)", "2:1 약 10분 · 학생부 사실 확인 후 추가 질문 · 자기소개 질문 없음", start_pad=12, end_pad=10)
    make_capture(HERE / "eulji-2027-beauty-interview.png", EU, 17, "1. EU면접형", ("after", "면접태도 및 자세, 제출서류 진위여부"),
                 "을지대학교", "2027학년도 수시모집요강 17쪽", "EU면접형 · 4배수 · 70% + 면접 30% · 11월 21일(토) 성남캠퍼스 · 최저 없음", start_pad=12, end_pad=10)
    make_capture(HERE / "eulji-2027-beauty-questions.png", EU, 18, "미생물 유전자 조작을 통한 콜라겐", ("after", "활동은 무엇인지 이야기해 주세요."),
                 "을지대학교", "2027학년도 수시모집요강 18쪽", "2026학년도 실제 면접 문항 공개 · 화장품·뷰티 관련 문항 포함 부분", start_pad=3, end_pad=3)
    make_structure(HERE / "structure-beauty.png", [
        "미용이 머리와 피부를 다루는 기술이라면, 뷰티학과는 그 기술에 화장품과 콘텐츠, 고객 응대를 붙여 산업으로 배우는 곳이라 지원했습니다.",
        "고2 때 친구 졸업사진 메이크업을 맡았는데, 사진관 조명에서는 제가 한 베이스가 들떠 보여서 다음 날 조명 아래에서 두 번 다시 해 봤습니다.",
        "뷰티는 내 눈에 예쁜 것이 아니라 그 사람이 서는 환경과 피부에 맞추는 일이고, 실패를 기록해야 실력이 는다는 것을 배웠습니다.",
        "뷰티학과에서 피부과학과 메이크업을 제대로 배워, 고객의 상황을 먼저 묻고 맞추는 아티스트가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    names = sys.argv[1:] or ["jobs_pe", "jobs_design", "jobs_kpop", "jobs_beauty"]
    for name in names:
        try:
            globals()[name]()
            print("OK", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
