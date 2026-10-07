# 식품영양학과·특수교육과·AI데이터사이언스학과·건축학과 블로그 이미지 (그룹 B). python jobs_b5_B.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

KW = pdf("광운대학교"); MJU = pdf("명지대학교"); SSU = pdf("숭실대학교"); KHU = pdf("경희대학교")
SYU = pdf("삼육대학교"); SM = pdf("숙명여자대학교"); DUK = pdf("덕성여자대학교")
BS = pdf("백석대학교"); KN = pdf("강남대학교"); PNU = pdf("부산대학교")


# ---------------------------------------------------------------- 공통 헬퍼 (jobs_batch4.py 에서 복사)
def kw_track(out, note):
    make_capture(out, KW, 19, "학생부종합【광운참빛인재전형", 748.5, "광운대학교", "2027학년도 수시모집요강 19쪽", note, start_pad=10, end_pad=3)


def kw_interview(out):
    make_capture(out, KW, 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】", "광운대학교", "2027학년도 수시모집요강 46쪽",
                 "2인 개별 대면 10분 이내 · 문제 제시형 없음 · 발전가능성 45% + 종합적사고력 30% + 인성 25%", start_pad=10, end_pad=8)


def kw_schedule(out, note, end=("after", "환경공학과")):
    make_capture(out, KW, 21, "6. 모집단위별 면접 일자", end, "광운대학교", "2027학년도 수시모집요강 21쪽", note, start_pad=10, end_pad=3)


def mju_interview(out, note):
    make_capture(out, MJU, 50, "4. 전형방법", ("after", "자기주도성, 도전정신"), "명지대학교", "2027학년도 수시모집요강 48쪽(PDF 50쪽)", note, start_pad=10, end_pad=8)


def mju_schedule(out, note):
    make_capture(out, MJU, 49, "3. 전형일정", ("after", "전형일정 상세내용은 p. 10 참조"), "명지대학교", "2027학년도 수시모집요강 47쪽(PDF 49쪽)", note, start_pad=10, end_pad=8)


def ssu_method(out, note):
    make_capture(out, SSU, 18, "전형요소 및 반영 비율", 293, "숭실대학교", "2027학년도 수시모집요강 13쪽(PDF 18쪽)", note, start_pad=36, end_pad=20)


def ssu_interview(out, note):
    make_capture(out, SSU, 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"), "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", note, start_pad=10, end_pad=8)


def khu_method(out, note):
    make_capture(out, KHU, 40, "3. 전형 방법", "※ 서류평가 및 면접평가 안내는", "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", note, start_pad=10, end_pad=8)


def khu_detail(out, note):
    make_capture(out, KHU, 42, "[면접평가 상세일정]", 545, "경희대학교", "2027학년도 수시모집요강 40쪽(PDF 42쪽)", note, start_pad=10)


def khu_interview(out):
    make_capture(out, KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적", "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)",
                 "공통질문 + 서류확인 면접 · 출제문항 없음 · 2:1 개인면접 10분 · 인성 50% + 전공적합성 50%", start_pad=10, end_pad=8)


# ---------------------------------------------------------------- 24 식품영양학과
def jobs_food():
    make_thumb(HERE / "thumb-food.png", "식품영양학과")
    make_capture(HERE / "syu-2027-food-track.png", SYU, 29, "단과대학", ("after", "순위까지 동점일"), "삼육대학교", "2027학년도 수시모집요강 27쪽(PDF 29쪽)",
                 "세움인재 식품영양학과 11명 · 4배수 · 60% + 면접 40% · 일반학과 최저 없음", start_pad=36, end_pad=8)
    make_capture(HERE / "syu-2027-food-interview.png", SYU, 56, "진행방법", 600, "삼육대학교", "2027학년도 수시모집요강 54쪽(PDF 56쪽)",
                 "서류 확인·개별질문 8분 이내 · 학업 30% + 진로 40% + 공동체 30%", start_pad=8)
    make_capture(HERE / "syu-2027-food-schedule.png", SYU, 18, "신학특별", 580, "삼육대학교", "2027학년도 수시모집요강 16쪽(PDF 18쪽)",
                 "세움인재 1단계 발표 10월 22일(목) · 면접 10월 25일(일) — 수능 전", start_pad=2)
    mju_interview(HERE / "mju-2027-food-interview.png", "명지인재면접 융합바이오학부 식품영양학전공 6명 · 4배수 · 70% + 면접 30%")
    mju_schedule(HERE / "mju-2027-food-schedule.png", "1단계 발표 11월 20일(금) · 자연캠퍼스 면접 11월 28일(토) · 장소는 서울 인문캠퍼스")
    make_capture(HERE / "sm-2027-food-method.png", SM, 18, "가. 모집단위 및 모집인원", "마. 전형요소별", "숙명여자대학교", "2027학년도 수시모집요강 14쪽(PDF 18쪽)",
                 "숙명인재(면접형) 식품영양학과 6명 · 4배수 · 70% + 면접 30% · 최저 없음", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-food-interview.png", SM, 19, "2) 면접평가", ("after", "(p.46~47)"), "숙명여자대학교", "2027학년도 수시모집요강 15쪽(PDF 19쪽)",
                 "평가위원 2인 개별면접 · 블라인드 · 12분 내외 제출서류 기반", start_pad=10, end_pad=8)
    khu_method(HERE / "khu-2027-food-method.png", "네오르네상스 식품영양학과 9명 · 3배수 · 70% + 면접 30% · 최저 없음")
    khu_detail(HERE / "khu-2027-food-schedule.png", "식품영양학과 면접 12월 6일(일) 09:00~13:00 서울캠퍼스")
    make_structure(HERE / "structure-food.png", [
        "식품영양학은 '무엇이 몸에 좋다'를 외우는 학문이 아니라, 먹는 것이 몸에서 어떻게 쓰이는지를 근거로 따지는 과학이라서 관심을 갖게 됐습니다.",
        "할아버지가 당뇨 진단을 받으신 뒤 가족이 흰쌀밥을 잡곡밥으로 바꿨는데, 혈당 기록을 2주간 같이 적어 보니 반찬 순서와 양에 따라 수치가 더 크게 달라졌습니다.",
        "'좋은 음식'보다 '언제, 얼마나, 누구에게'가 더 중요하고, 그걸 판단하는 기준이 생화학과 생리학이라는 것을 배웠습니다.",
        "식품영양학과에서 영양생화학과 임상영양을 제대로 배워, 환자 한 사람의 식단을 근거로 설계하는 임상영양사가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 26 특수교육과
def jobs_sped():
    make_thumb(HERE / "thumb-sped.png", "특수교육과")
    make_capture(HERE / "baekseok-2027-sped-track.png", BS, 19, "◈ 전형", ("after", "환산점수"), "백석대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)",
                 "백석인재 특수교육과 10명·유아특수교육과 3명 · 교과 60% + 면접 40% · 최저 없음", start_pad=8, end_pad=6)
    make_capture(HERE / "baekseok-2027-sped-interview.png", BS, 20, "라. 면접고사", "4) 유의사항", "백석대학교", "2027학년도 수시모집요강 18쪽(PDF 20쪽)",
                 "특수교육과 10월 16일(금) · 유아특수 10월 15일(목) · 2:1 5분 내외 · 인·적성 문제", start_pad=8, end_pad=8)
    make_capture(HERE / "kangnam-2027-sped-track.png", KN, 26, "학생부종합[학교생활우수자전형2]", ("after", "종합적 사고력 및 의사소통능력"), "강남대학교", "2027학년도 수시모집요강 26쪽",
                 "학교생활우수자전형2 초등특수·중등특수 각 8명 · 3배수 · 70% + 면접 30% · 최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "kangnam-2027-sped-schedule.png", KN, 27, "■ 전형일정", "■ 제출서류", "강남대학교", "2027학년도 수시모집요강 27쪽",
                 "1단계 발표 10월 30일(금) · 면접 11월 7일(토)~8일(일) 중 지정일 — 수능 전", start_pad=8, end_pad=10)
    make_capture(HERE / "kangnam-2027-sped-interview.png", KN, 49, "■ 면접평가", ("after", "개인별 면접일시 및 장소 확인"), "강남대학교", "2027학년도 수시모집요강 49쪽",
                 "면접관 3인 대 지원자 1인 · 학생부 확인 면접 · 15분 이내 · 블라인드", start_pad=8, end_pad=10)
    make_capture(HERE / "pusan-2027-sped-method.png", PNU, 37, "다. 전형방법", "미등록으로 인한", "부산대학교", "2027학년도 수시모집요강 35쪽(PDF 37쪽)",
                 "학생부종합전형 특수교육과 8명 · 3배수 · 1단계 80% + 면접 20%", start_pad=8, end_pad=10)
    make_capture(HERE / "pusan-2027-sped-schedule.png", PNU, 38, "전형일정", ("after", "등록 및 충원합격자"), "부산대학교", "2027학년도 수시모집요강 36쪽(PDF 38쪽)",
                 "1단계 발표 12월 1일(화) · 면접 12월 5일(토) · 최초 합격 12월 18일(금)", start_pad=10, end_pad=10)
    make_capture(HERE / "pusan-2027-sped-interview.png", PNU, 67, "2. 면접고사 일자", 489, "부산대학교", "2027학년도 수시모집요강 64쪽(PDF 67쪽)",
                 "학생부 기반 면접 10분 내외 · 탐구역량 + 사회역량 · 다수 평가자 대 1인", start_pad=8)
    make_structure(HERE / "structure-sped.png", [
        "특수교사는 장애 학생을 돌보는 사람이 아니라, 한 학생이 할 수 있는 것을 찾아 그 아이에게 맞는 수업을 설계하는 교사라고 생각해서 지원했습니다.",
        "고2 때 통합학급 짝꿍이 모둠 발표 때마다 자리를 피했는데, 발표 순서를 그림 카드로 미리 보여 주자 세 번째 시간부터 자기 파트를 끝까지 해냈습니다.",
        "그 친구가 못 한 게 아니라 수업이 그 친구에게 맞지 않았던 것이고, 바꿔야 할 쪽은 환경이라는 것을 배웠습니다.",
        "특수교육과에서 개별화교육과 행동지원을 제대로 배워, 통합학급 담임과 함께 한 아이의 하루를 설계하는 특수교사가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 27 AI·데이터사이언스학과
def jobs_aidata():
    # 학과명이 길어 글자 단위 줄바꿈이 어색하므로 이 썸네일만 'AI·데이터 / 사이언스학과'로 끊는다(promo_style.py 는 그대로).
    import promo_style
    orig = promo_style.wrap_chars
    promo_style.wrap_chars = lambda d, text, fnt, maxw: ["AI·데이터", "사이언스학과"] if text == "AI·데이터사이언스학과" else orig(d, text, fnt, maxw)
    try:
        make_thumb(HERE / "thumb-aidata.png", "AI·데이터사이언스학과")
    finally:
        promo_style.wrap_chars = orig
    make_capture(HERE / "duksung-2027-aidata-method.png", DUK, 29, "1. 모집단위 및 모집인원", "4. 선발원칙", "덕성여자대학교", "2027학년도 수시모집요강 29쪽",
                 "덕성인재Ⅱ 데이터사이언스학과·AI신약학과 각 15명 · 3배수 · 60% + 면접 40%", start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "duksung-2027-aidata-schedule.png", DUK, 30, "2026.11.12.(목)", "6. 제출서류", "덕성여자대학교", "2027학년도 수시모집요강 30쪽",
                 "1단계 발표 11월 12일(목) · 데이터사이언스학과·AI신약학과 면접 11월 21일(토)", start_pad=16, end_pad=10)
    make_capture(HERE / "duksung-2027-aidata-criteria.png", DUK, 73, "미래인재대학", "나. 면접평가항목 평가내용", "덕성여자대학교", "2027학년도 수시모집요강 73쪽",
                 "데이터에 대한 수학적 이해·해석 능력 · 서류 신뢰성 50 + 종합적 사고력 30 + 공동체 20", start_pad=7, end_pad=10, start_idx=2, lr=45)
    make_capture(HERE / "duksung-2027-aidata-questions.png", DUK, 74, "다. 면접평가 운영방법", "4. 블라인드 평가 안내", "덕성여자대학교", "2027학년도 수시모집요강 74쪽",
                 "10분 내외 개별면접(2인) · 블라인드 · 평가항목별 면접질문 예시 공개", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-aidata-track.png", SM, 20, "가. 모집단위 및 모집인원", "마. 전형요소별", "숙명여자대학교", "2027학년도 수시모집요강 16쪽(PDF 20쪽)",
                 "소프트웨어인재 인공지능공학부 14명·데이터사이언스전공 9명 · 4배수 · 70% + 면접 30%", start_pad=10, end_pad=10)
    make_capture(HERE / "sm-2027-aidata-interview.png", SM, 21, "2) 면접평가", ("after", "(p.46~47)"), "숙명여자대학교", "2027학년도 수시모집요강 17쪽(PDF 21쪽)",
                 "평가위원 2인 개별면접 · 블라인드 · 12분 내외 제출서류 기반", start_pad=10, end_pad=8)
    mju_interview(HERE / "mju-2027-aidata-interview.png", "명지인재면접 데이터사이언스전공·인공지능전공 각 6명 · 4배수 · 70% + 면접 30%")
    mju_schedule(HERE / "mju-2027-aidata-schedule.png", "1단계 발표 11월 20일(금) · 인문캠퍼스 모집단위 면접 11월 29일(일)")
    make_structure(HERE / "structure-aidata.png", [
        "AI를 쓰는 사람보다, 데이터가 어떻게 모델의 판단이 되는지 그 과정을 이해하고 설계하는 사람이 되고 싶어서 지원했습니다.",
        "고2 수학 탐구에서 급식 잔반량을 메뉴별로 3주간 기록해 회귀선을 그렸는데, 비 오는 날 데이터를 빼자 결론이 완전히 바뀌었습니다.",
        "모델보다 데이터를 어떻게 모으고 무엇을 빼느냐가 결론을 정한다는 것, 그래서 통계와 데이터 처리가 AI의 기초라는 것을 배웠습니다.",
        "AI·데이터사이언스학과에서 확률·통계와 기계학습을 제대로 배워, 결과를 설명할 수 있는 모델을 만드는 데이터 사이언티스트가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 34 건축학과
def jobs_arch():
    make_thumb(HERE / "thumb-arch.png", "건축학과")
    kw_track(HERE / "kw-2027-arch-track.png", "참빛인재Ⅰ 면접형 건축학과(5년제) 6명·건축공학과 6명 · 3.5배수 · 60% + 면접 40%")
    kw_interview(HERE / "kw-2027-arch-interview.png")
    kw_schedule(HERE / "kw-2027-arch-schedule.png", "건축학과·건축공학과 면접 10월 31일(토) · 1단계 발표 10월 28일(수)")
    ssu_method(HERE / "ssu-2027-arch-method.png", "SSU미래인재 면접형 건축학부 15명·실내건축 11명 · 3.5배수 · 50% + 면접 50%")
    ssu_interview(HERE / "ssu-2027-arch-interview.png", "서류 기반 블라인드 12분 · 전공적합성 50% + 잠재력 50% · 면접질문 예시 공개")
    mju_interview(HERE / "mju-2027-arch-interview.png", "명지인재면접 건축학전공·전통건축학전공·공간디자인학과 각 6명 · 4배수 · 70% + 면접 30%")
    mju_schedule(HERE / "mju-2027-arch-schedule.png", "1단계 발표 11월 20일(금) · 자연캠퍼스 면접 11월 28일(토) · 장소는 서울 인문캠퍼스")
    khu_method(HERE / "khu-2027-arch-method.png", "네오르네상스 건축학과(5년제) 8명·건축공학과 11명 · 3배수 · 70% + 면접 30%")
    khu_detail(HERE / "khu-2027-arch-schedule.png", "공과대학 면접 12월 6일(일) 09:00~13:00 국제캠퍼스")
    make_structure(HERE / "structure-arch.png", [
        "건물을 튼튼하게 세우는 기술보다, 그 안에서 사람이 어떻게 움직이고 머무는지를 설계하는 쪽에 관심이 있어서 건축학과를 택했습니다.",
        "고2 때 학교 도서관 리모델링 설문을 맡았는데, 학생들이 창가 자리만 찾는 이유를 관찰해 보니 조명보다 '등 뒤가 막혀 있는 자리'를 원한다는 걸 알게 됐습니다.",
        "공간은 면적보다 사람이 느끼는 안정감과 동선이 결정하고, 그걸 읽어 내는 관찰이 설계의 시작이라는 것을 배웠습니다.",
        "건축학과 5년 과정에서 설계 스튜디오와 건축계획을 제대로 배워, 사람이 오래 머물고 싶은 공공 공간을 설계하는 건축가가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    names = sys.argv[1:] or ["jobs_food", "jobs_sped", "jobs_aidata", "jobs_arch"]
    for name in names:
        try:
            globals()[name]()
            print("OK", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
