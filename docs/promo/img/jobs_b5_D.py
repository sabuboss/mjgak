# 그룹 D: 호텔관광학과(32)·광고홍보학과(33)·간호학과 v2(36)·유아교육과 v3(37) 블로그 이미지. python jobs_b5_D.py [jobs_tour ...]
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

KHU = pdf("경희대학교"); SSU = pdf("숭실대학교"); SEJONG = pdf("세종대학교"); KGU = pdf("경기대학교")
DONGGUK = pdf("동국대학교"); CAU = str(SRC / "cau.pdf"); AJOU = pdf("아주대학교"); EULJI = pdf("을지대학교")
ULSAN = str(SRC / "ulsan.pdf"); BAEKSEOK = pdf("백석대학교"); KANGNAM = pdf("강남대학교"); DUKSUNG = pdf("덕성여자대학교")


# ---------------------------------------------------------------- 공통 헬퍼 (jobs_batch4.py 에서 복사)
def ssu_method(out, note):
    make_capture(out, SSU, 18, "전형요소 및 반영 비율", 293, "숭실대학교", "2027학년도 수시모집요강 13쪽(PDF 18쪽)", note, start_pad=36, end_pad=20)


def ssu_interview(out, note):
    make_capture(out, SSU, 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"), "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", note, start_pad=10, end_pad=8)


def khu_interview(out, note):
    make_capture(out, KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적", "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)", note, start_pad=10, end_pad=8)


def khu_method(out, note):
    make_capture(out, KHU, 40, "3. 전형 방법", "※ 서류평가 및 면접평가 안내는", "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", note, start_pad=10, end_pad=8)


def khu_detail(out, note):
    make_capture(out, KHU, 42, "[면접평가 상세일정]", ("after", "모든 의학계열"), "경희대학교", "2027학년도 수시모집요강 40쪽(PDF 42쪽)", note, start_pad=10, end_pad=22)


def cau_method(out, note):
    make_capture(out, CAU, 28, "라. 수능최저학력기준", "2) 서류평가", "중앙대학교", "2027학년도 수시모집요강 28쪽", note, start_pad=10, end_pad=6)


def cau_schedule(out, note):
    make_capture(out, CAU, 27, "다. 전형일정", ("after", "1단계 합격자 발표 시 조정 방법 안내"), "중앙대학교", "2027학년도 수시모집요강 27쪽", note, start_pad=10, end_pad=8)


def cau_interview(out, note):
    make_capture(out, CAU, 95, "2. 면접평가", 730, "중앙대학교", "2027학년도 수시모집요강 95쪽", note, start_pad=10)


# ---------------------------------------------------------------- 32 호텔관광학과
def jobs_tour():
    make_thumb(HERE / "thumb-tour.png", "호텔관광학과")
    make_capture(HERE / "sejong-2027-tour-track.png", SEJONG, 13, "학생부종합", 790, "세종대학교", "2027학년도 수시모집요강 13쪽",
                 "세종인재 면접형 호텔관광외식경영학부 14명 · 3배수 · 60% + 면접 40% · 9분 내외", start_pad=10)
    make_capture(HERE / "sejong-2027-tour-schedule.png", SEJONG, 14, "전형일정", "제출서류", "세종대학교", "2027학년도 수시모집요강 14쪽",
                 "1단계 발표 11월 13일(금) · 인문·자연계열 면접 11월 22일(일)", start_pad=10, end_pad=6, start_idx=0)
    make_capture(HERE / "kyonggi-2027-tour-interview.png", KGU, 46, "라. 학생부종합전형 면접평가 방법", "6) 평가항목 및 평가내용", "경기대학교", "2027학년도 수시모집요강 42쪽(PDF 46쪽)",
                 "KGU학생부종합 면접 30% · 잠재역량 15% + 사회역량 10% + 소통역량 5%", start_pad=10, end_pad=8)
    make_capture(HERE / "kyonggi-2027-tour-schedule.png", KGU, 13, "KGU학생부종합전형", "SW우수자전형", "경기대학교", "2027학년도 수시모집요강 9쪽(PDF 13쪽)",
                 "관광문화대학 면접 12월 5일(토) 수원캠퍼스 · 1단계 발표 11월 20일(금)", start_pad=12, end_pad=10)
    khu_method(HERE / "khu-2027-tour-method.png", "네오르네상스 호텔관광대학 4개 모집단위 86명 · 3배수 · 70% + 면접 30% · 최저 없음")
    khu_detail(HERE / "khu-2027-tour-detail.png", "호텔관광대학 면접 12월 5일(토) 09:00~13:00 서울캠퍼스 · 1단계 발표 11월 25일")
    make_structure(HERE / "structure-tour.png", [
        "여행이 좋아서가 아니라, 한 도시에 관광객이 몰릴 때 그 도시와 사람들에게 무슨 일이 생기는지를 다루고 싶어서 호텔관광학과에 지원했습니다.",
        "고2 때 가족 여행으로 간 바닷가 마을에서 주차 문제로 주민과 관광객이 다투는 장면을 봤고, 돌아와 그 마을의 관광객 수와 민원 기사를 찾아 보고서를 썼습니다.",
        "관광은 손님을 즐겁게 하는 일만이 아니라 손님과 주민이 함께 살 수 있게 설계하는 일이라는 것을 배웠습니다.",
        "호텔관광학과에서 관광 경영과 정책을 제대로 배워, 관광객도 주민도 다시 찾고 싶은 지역을 만드는 사람이 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 33 광고홍보학과
def jobs_adpr():
    make_thumb(HERE / "thumb-adpr.png", "광고홍보학과")
    make_capture(HERE / "dongguk-2027-adpr-track.png", DONGGUK, 18, "학생부종합[Do Dream]", 756, "동국대학교", "2027학년도 수시모집요강 16쪽(PDF 18쪽)",
                 "Do Dream 광고홍보학과 10명 · 70% + 면접 30% · 수능 최저 미적용", start_pad=8)
    make_capture(HERE / "dongguk-2027-adpr-interview.png", DONGGUK, 19, "1단계 선발배수", "5 선발원칙", "동국대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)",
                 "광고홍보학과 3.5배수 · 면접위원 2인 10분 내외 · 전공적합성 30% + 발전가능성 30%", start_pad=10, end_pad=8)
    make_capture(HERE / "dongguk-2027-adpr-schedule.png", DONGGUK, 21, "9 면접일정", 633.5, "동국대학교", "2027학년도 수시모집요강 19쪽(PDF 21쪽)",
                 "광고홍보학과 면접 12월 12일(토) · 1단계 발표 11월 13일(금) 예정", start_pad=10, end_pad=8)
    make_capture(HERE / "cau-2027-adpr-units.png", CAU, 26, "2. 학생부종합 (탐구형인재)", ("after", "총계"), "중앙대학교", "2027학년도 수시모집요강 26쪽",
                 "탐구형인재 광고홍보학부(광고홍보학) 7명 · 수능 최저 미적용", start_pad=10, end_pad=8)
    cau_schedule(HERE / "cau-2027-adpr-schedule.png", "1단계 발표 11월 26일(목) · 광고홍보학 3.5배수 · 면접 12월 5일(토)")
    cau_interview(HERE / "cau-2027-adpr-interview.png", "입학사정관 2인 10분 이내 · 학업준비도 60% + 전공적합성 30% + 인성 10%")
    ssu_method(HERE / "ssu-2027-adpr-method.png", "SSU미래인재 면접형 언론홍보학과 4명 · 3.5배수 · 50% + 면접 50% · 0점이면 불합격")
    ssu_interview(HERE / "ssu-2027-adpr-interview.png", "서류 기반 블라인드 12분 · 면접질문 예시 공개 · 11월 27일(금)")
    make_structure(HERE / "structure-adpr.png", [
        "광고를 잘 만들고 싶어서라기보다, 같은 제품이 어떤 말로 소개되느냐에 따라 사람들이 다르게 움직이는 이유를 배우고 싶어서 지원했습니다.",
        "고2 때 학교 축제 부스 홍보 포스터를 두 가지로 만들어 반씩 붙였는데, 가격을 앞세운 쪽보다 '친구랑 같이 오면'이라는 문구를 쓴 쪽 앞에 줄이 더 길었습니다.",
        "사람은 정보보다 자기 이야기처럼 느껴지는 메시지에 움직이고, 그걸 먼저 찾는 것이 광고의 출발이라는 것을 배웠습니다.",
        "광고홍보학과에서 소비자 심리와 캠페인 기획을 제대로 배워, 사람을 움직이되 속이지 않는 메시지를 만드는 사람이 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 36 간호학과 v2
def jobs_nurse2():
    make_thumb(HERE / "thumb-nurse2.png", "간호학과")
    make_capture(HERE / "eulji-2027-nurse2-method.png", EULJI, 17, "1. EU면접형", ("after", "면접태도 및 자세"), "을지대학교", "2027학년도 수시모집요강 17쪽",
                 "EU면접형 · 4배수 · 70% + 면접 30% · 최저 없음 · 면접 11월 21일(토) 성남", start_pad=10, end_pad=8)
    make_capture(HERE / "eulji-2027-nurse2-questions.png", EULJI, 18, "라. 전년도(2026학년도) 면접문항 예시", ("after", "장례지도사의 역할은 무엇인가요?"), "을지대학교", "2027학년도 수시모집요강 18쪽",
                 "EU면접형 2026학년도 실제 면접 문항 공개 · 서류기반면접", start_pad=10, end_pad=8)
    make_capture(HERE / "ajou-2027-nurse2-method.png", AJOU, 11, "학생부종합", 667, "아주대학교", "2027학년도 수시모집요강 9쪽(PDF 11쪽)",
                 "ACE전형 간호학과 25명 · 3배수 · 70% + 면접 30% · 간호학과 최저 없음", start_pad=10, end_pad=8)
    make_capture(HERE / "ajou-2027-nurse2-interview.png", AJOU, 12, "나. 면접평가(의학과 제외)", "다. 면접평가(의학과)", "아주대학교", "2027학년도 수시모집요강 10쪽(PDF 12쪽)",
                 "2인 이상 면접관 · 10분 내외 · 학교생활기록부 기반 개별 질문", start_pad=10, end_pad=8)
    make_capture(HERE / "ajou-2027-nurse2-schedule.png", AJOU, 13, "5. 전형일정", "6. 제출서류", "아주대학교", "2027학년도 수시모집요강 11쪽(PDF 13쪽)",
                 "1단계 발표 11월 17일(화) · 간호대학 면접 11월 28일(토)", start_pad=10, end_pad=8)
    make_capture(HERE / "ulsan-2027-nurse2-method.png", ULSAN, 24, "1. 모집인원", "5. 수능최저학력기준", "울산대학교", "2027학년도 수시모집요강 24쪽",
                 "잠재역량 간호학과 18명 · 4배수 · 서류 50% + 면접 50% · 최저 없음", start_pad=5, end_pad=6)
    cau_schedule(HERE / "cau-2027-nurse2-schedule.png", "1단계 발표 11월 26일(목) · 간호학과 3.5배수 · 면접 12월 6일(일)")
    cau_interview(HERE / "cau-2027-nurse2-interview.png", "입학사정관 2인 10분 이내 · 학업준비도 60% + 전공적합성 30% + 인성 10%")
    make_structure(HERE / "structure-nurse2.png", [
        "간호사는 의사를 돕는 사람이 아니라, 환자 곁에서 하루 종일 변화를 관찰하고 판단하는 전문가라서 간호학과에 지원했습니다.",
        "고1 때 할머니가 3주간 입원하셨을 때, 간호사 선생님이 밤사이 열과 소변량 변화를 보고 먼저 담당의에게 알려 감염을 빨리 잡았다는 설명을 들었습니다.",
        "회복은 회진 몇 분이 아니라 24시간의 관찰로 지켜지고, 그 관찰이 간호의 전문성이라는 것을 배웠습니다.",
        "간호학과에서 기본간호와 성인간호를 제대로 배워, 작은 변화를 먼저 알아차리는 간호사가 되고 싶습니다.",
    ])


# ---------------------------------------------------------------- 37 유아교육과 v3
def jobs_ece3():
    make_thumb(HERE / "thumb-ece3.png", "유아교육과")
    make_capture(HERE / "baekseok-2027-ece3-track.png", BAEKSEOK, 19, "◈ 전형 : 백석인재", ("after", "환산점수(점)"), "백석대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)",
                 "백석인재(교과) 유아교육과 10명 · 학생부교과 60% + 면접 40% · 최저 없음", start_pad=10, end_pad=10)
    make_capture(HERE / "baekseok-2027-ece3-interview.png", BAEKSEOK, 20, "라. 면접고사", "4) 유의사항", "백석대학교", "2027학년도 수시모집요강 18쪽(PDF 20쪽)",
                 "유아교육과 면접 10월 16일(금) · 2인 대 1인 5분 내외 · 인·적성 문제 출제", start_pad=10, end_pad=8)
    make_capture(HERE / "kangnam-2027-ece3-interview.png", KANGNAM, 49, "■ 면접평가", ("after", "개인별 지정된"), "강남대학교", "2027학년도 수시모집요강 49쪽",
                 "면접관 3인 대 1인 · 15분 이내 · 면접 11월 7일(토)~8일(일) 중 지정일", start_pad=10, end_pad=22, start_idx=0)
    make_capture(HERE / "duksung-2027-ece3-method.png", DUKSUNG, 29, "1. 모집단위 및 모집인원", "4. 선발원칙", "덕성여자대학교", "2027학년도 수시모집요강 29쪽",
                 "덕성인재Ⅱ 유아교육과 12명 · 3배수 · 60% + 면접 40% · 최저 없음", start_pad=10, end_pad=8, lr=42)
    make_capture(HERE / "duksung-2027-ece3-questions.png", DUKSUNG, 74, "다. 면접평가 운영방법", "4. 블라인드 평가 안내", "덕성여자대학교", "2027학년도 수시모집요강 74쪽",
                 "10분 내외 개별면접(2인) · 평가항목별 면접질문 예시 공개", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-ece3.png", [
        "아이가 좋은 것이 시작이었지만, 유아기 경험이 평생을 좌우한다는 걸 알고 그 시기를 전문적으로 돕는 교사가 되고 싶어 지원했습니다.",
        "어린이집 봉사 때 말이 늦던 아이를 선생님이 매일 그림책으로 이끌어 한 학기 만에 문장으로 말하게 하는 걸 옆에서 봤습니다.",
        "그 변화는 좋아하는 마음이 아니라 매일 관찰하고 기록하고 방법을 바꾸는 전문성에서 나온다는 것을 배웠습니다.",
        "유아교육과에서 아동 발달과 관찰 방법을 제대로 배워, 아이 한 명 한 명의 속도를 읽어 내는 교사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    names = sys.argv[1:] or ["jobs_tour", "jobs_adpr", "jobs_nurse2", "jobs_ece3"]
    for name in names:
        try:
            globals()[name]()
            print("OK", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
