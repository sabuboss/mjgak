# 그룹 A(인문사회): 행정학과·영어영문학과·국어국문학과·경제학과 블로그 이미지. python jobs_b5_A.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

KW = pdf("광운대학교"); MJU = pdf("명지대학교"); SSU = pdf("숭실대학교"); KHU = pdf("경희대학교"); AJOU = pdf("아주대학교"); DGU = pdf("동국대학교")


# ---------------------------------------------------------------- 광운대 (jobs_batch4.py 에서 복사)
def kw_track(out, note):
    make_capture(out, KW, 19, "학생부종합【광운참빛인재전형", 749, "광운대학교", "2027학년도 수시모집요강 19쪽", note, start_pad=10)


def kw_interview(out):
    make_capture(out, KW, 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】", "광운대학교", "2027학년도 수시모집요강 46쪽",
                 "2인 개별 대면 10분 이내 · 문제 제시형 없음 · 발전가능성 45% + 종합적사고력 30% + 인성 25%", start_pad=10, end_pad=8)


def kw_schedule(out, note, end=("after", "국제통상학부")):
    make_capture(out, KW, 21, "6. 모집단위별 면접 일자", end, "광운대학교", "2027학년도 수시모집요강 21쪽", note, start_pad=10, end_pad=3)


# ---------------------------------------------------------------- 명지대 (복사)
def mju_interview(out, note):
    make_capture(out, MJU, 50, "4. 전형방법", ("after", "자기주도성, 도전정신"), "명지대학교", "2027학년도 수시모집요강 48쪽(PDF 50쪽)", note, start_pad=10, end_pad=8)


def mju_schedule(out, note):
    make_capture(out, MJU, 49, "3. 전형일정", ("after", "전형일정 상세내용은 p. 10 참조"), "명지대학교", "2027학년도 수시모집요강 47쪽(PDF 49쪽)", note, start_pad=10, end_pad=8)


# ---------------------------------------------------------------- 숭실대 (복사)
def ssu_method(out, note):
    make_capture(out, SSU, 18, "전형요소 및 반영 비율", 293, "숭실대학교", "2027학년도 수시모집요강 13쪽(PDF 18쪽)", note, start_pad=36)


def ssu_interview(out, note="서류 기반 블라인드 12분 · 전공적합성 50% + 잠재력 50% · 면접질문 예시 공개 · 11월 27일(금)"):
    make_capture(out, SSU, 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"), "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", note, start_pad=10, end_pad=8)


# ---------------------------------------------------------------- 경희대 (복사 + 상세일정)
def khu_interview(out):
    make_capture(out, KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적", "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)",
                 "공통질문 + 서류확인 면접 · 출제문항 없음 · 2:1 개인면접 10분 · 인성 50% + 전공적합성 50%", start_pad=10, end_pad=8)


def khu_method(out, note):
    make_capture(out, KHU, 40, "3. 전형 방법", "※ 서류평가 및 면접평가 안내는", "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", note, start_pad=10, end_pad=8)


def khu_detail(out, note):
    make_capture(out, KHU, 42, "[면접평가 상세일정]", ("after", "진행합니다."), "경희대학교", "2027학년도 수시모집요강 40쪽(PDF 42쪽)", note, start_pad=10, end_pad=10)


# ---------------------------------------------------------------- 아주대
def ajou_method(out, note):
    make_capture(out, AJOU, 11, "1. 모집단위 및 모집인원", 665, "아주대학교", "2027학년도 수시모집요강 9쪽(PDF 11쪽)", note, start_pad=10)


def ajou_interview(out, note):
    make_capture(out, AJOU, 12, "나. 면접평가(의학과 제외)", "다. 면접평가(의학과)", "아주대학교", "2027학년도 수시모집요강 10쪽(PDF 12쪽)", note, start_pad=10, end_pad=12)


def ajou_schedule(out, note):
    make_capture(out, AJOU, 13, "5. 전형일정", ("after", "변경은 불가능함"), "아주대학교", "2027학년도 수시모집요강 11쪽(PDF 13쪽)", note, start_pad=10, end_pad=8)


# ---------------------------------------------------------------- 동국대
def dgu_method(out, note):
    make_capture(out, DGU, 19, "※ 1단계 선발배수", "선발원칙 및 동점자", "동국대학교", "2027학년도 수시모집요강 17쪽(PDF 19쪽)", note, start_pad=10, end_pad=10)


def dgu_day1(out, note):
    """면접일정 머리말 + 12월 11일(금) 표."""
    make_capture(out, DGU, 21, "면접일정", 397.5, "동국대학교", "2027학년도 수시모집요강 19쪽(PDF 21쪽)", note, start_pad=3)


def dgu_day3(out, note):
    """12월 13일(일) 표."""
    make_capture(out, DGU, 21, "12월 13일(일)", ("after", "사회복지학과"), "동국대학교", "2027학년도 수시모집요강 19쪽(PDF 21쪽)", note, start_pad=1, end_pad=8)


# ================================================================ 25 행정학과
def jobs_padm():
    make_thumb(HERE / "thumb-padm.png", "행정학과")
    kw_track(HERE / "kw-2027-padm-track.png", "참빛인재Ⅰ 면접형 행정학과 8명 · 3.5배수 · 60% + 면접 40% · 최저 없음")
    kw_interview(HERE / "kw-2027-padm-interview.png")
    kw_schedule(HERE / "kw-2027-padm-schedule.png", "행정학과 면접 11월 1일(일) · 1단계 발표 10월 28일(수) · 순서는 발표 시 확정")
    mju_interview(HERE / "mju-2027-padm-interview.png", "명지인재면접 행정학전공 14명 · 4배수 · 70% + 면접 30% · 심층면접 10분 · 진로역량 40%")
    mju_schedule(HERE / "mju-2027-padm-schedule.png", "1단계 발표 11월 20일(금) · 인문캠퍼스 모집단위 면접 11월 29일(일) · 서울 인문캠퍼스")
    dgu_method(HERE / "dongguk-2027-padm-method.png", "Do Dream 행정학전공 6명 · 3.5배수 · 70% + 면접 30% · 2인 10분 · 최저 미적용")
    dgu_day3(HERE / "dongguk-2027-padm-schedule.png", "1단계 발표 11월 13일(금) 예정 · 행정학전공 면접 12월 13일(일)")
    make_structure(HERE / "structure-padm.png", [
        "정치학이 제도가 만들어지는 과정을, 경영학이 기업의 운영을 다룬다면, 행정학은 정해진 정책이 현장에서 어떻게 집행되고 왜 어긋나는지를 다루는 학문이라서 지원했습니다.",
        "고2 때 동네 버스 노선 개편을 조사했는데, 시가 확정한 계획이 정류장 안내와 배차 조정이 늦어지면서 주민 민원이 한 달 넘게 이어졌습니다.",
        "좋은 정책도 집행 과정에서 무너질 수 있고, 계획과 현장 사이를 설계하는 일이 행정이라는 것을 배웠습니다.",
        "행정학과에서 정책 집행과 평가를 제대로 배워, 계획과 현장의 간극을 줄이는 공공 부문 전문가가 되고 싶습니다.",
    ])


# ================================================================ 28 영어영문학과
def jobs_eng():
    make_thumb(HERE / "thumb-eng.png", "영어영문학과")
    kw_track(HERE / "kw-2027-eng-track.png", "참빛인재Ⅰ 면접형 영어영문학과 6명 · 3.5배수 · 60% + 면접 40% · 최저 없음")
    kw_interview(HERE / "kw-2027-eng-interview.png")
    kw_schedule(HERE / "kw-2027-eng-schedule.png", "영어영문학과 면접 11월 1일(일) · 1단계 발표 10월 28일(수) · 순서는 발표 시 확정")
    ssu_method(HERE / "ssu-2027-eng-method.png", "SSU미래인재 면접형 영어영문학과 21명 · 인문대학 3배수 · 50% + 면접 50%")
    ssu_interview(HERE / "ssu-2027-eng-interview.png")
    ajou_method(HERE / "ajou-2027-eng-method.png", "ACE 영어영문학과 24명 · 3배수 · 70% + 면접 30% · 최저 없음(의·약 제외)")
    ajou_interview(HERE / "ajou-2027-eng-interview.png", "학생부 기반 개별 면접 10분 · 서류 신뢰도 80% + 의사소통능력·태도 20%")
    ajou_schedule(HERE / "ajou-2027-eng-schedule.png", "1단계 발표 11월 17일(화) · 인문대학 면접 11월 29일(일)")
    make_structure(HERE / "structure-eng.png", [
        "영어를 잘하는 것은 도구를 쓰는 능력이고, 영어영문학은 그 언어로 쓰인 문학과 문화를 연구 대상으로 삼는 학문이라서 지원했습니다.",
        "고2 때 '마지막 잎새'를 원문으로 읽으며 문장은 다 해석했는데, 왜 하필 가난한 화가들이 모여 사는 동네가 배경인지는 설명하지 못했습니다.",
        "문장을 옮기는 일과 작품이 그 시대에 무엇을 말했는지 읽어 내는 일은 다르고, 저는 뒤쪽에 더 끌린다는 것을 알았습니다.",
        "영어영문학과에서 영미 문학과 영어학을 체계적으로 배워, 작품을 시대와 함께 읽어 내는 사람이 되고 싶습니다.",
    ])


# ================================================================ 29 국어국문학과
def jobs_kor():
    make_thumb(HERE / "thumb-kor.png", "국어국문학과")
    ssu_method(HERE / "ssu-2027-kor-method.png", "SSU미래인재 면접형 국어국문학과 7명 · 인문대학 3배수 · 50% + 면접 50%")
    ssu_interview(HERE / "ssu-2027-kor-interview.png")
    khu_method(HERE / "khu-2027-kor-method.png", "네오르네상스 국어국문학과 20명 · 3배수 · 70% + 면접 30% · 수능 최저 없음")
    khu_interview(HERE / "khu-2027-kor-interview.png")
    khu_detail(HERE / "khu-2027-kor-schedule.png", "1단계 발표 11월 25일(수) · 문과대학 면접 12월 5일(토) 09:00~13:00 서울캠퍼스")
    dgu_method(HERE / "dongguk-2027-kor-method.png", "Do Dream 국어국문·문예창작학부 8명 · 3.5배수 · 70% + 면접 30% · 2인 10분")
    dgu_day1(HERE / "dongguk-2027-kor-schedule.png", "1단계 발표 11월 13일(금) 예정 · 국어국문·문예창작학부 면접 12월 11일(금)")
    make_structure(HERE / "structure-kor.png", [
        "창작이 '쓰는 일'이라면 국문학 연구는 '작품이 왜 그렇게 쓰였고 어떻게 읽히는지'를 근거로 밝히는 일이고, 저는 그 읽기를 배우고 싶어서 지원했습니다.",
        "고2 문학 시간에 '진달래꽃'의 '사뿐히 즈려밟고'를 체념으로만 읽었는데, 반어로 읽으면 원망이 된다는 해석을 찾아보고 같은 구절이 정반대로 읽힐 수 있다는 걸 알았습니다.",
        "작품의 의미는 외우는 정답이 아니라 구절과 시대를 근거로 따지는 것이고, 그 근거를 찾는 일이 연구라는 것을 배웠습니다.",
        "국어국문학과에서 현대시와 국어학을 체계적으로 배워, 근거 있게 읽고 그 읽기를 쉬운 글로 전하는 사람이 되고 싶습니다.",
    ])


# ================================================================ 35 경제학과
def jobs_econ():
    make_thumb(HERE / "thumb-econ.png", "경제학과")
    ssu_method(HERE / "ssu-2027-econ-method.png", "SSU미래인재 면접형 경제학과 14명 · 3.5배수 · 50% + 면접 50% · 0점이면 불합격")
    ssu_interview(HERE / "ssu-2027-econ-interview.png")
    mju_interview(HERE / "mju-2027-econ-interview.png", "명지인재면접 경제학전공 6명 · 4배수 · 70% + 면접 30% · 심층면접 10분 · 진로역량 40%")
    mju_schedule(HERE / "mju-2027-econ-schedule.png", "1단계 발표 11월 20일(금) · 인문캠퍼스 모집단위 면접 11월 29일(일) · 서울 인문캠퍼스")
    khu_method(HERE / "khu-2027-econ-method.png", "네오르네상스 경제학과 20명 · 3배수 · 70% + 면접 30% · 수능 최저 없음")
    khu_interview(HERE / "khu-2027-econ-interview.png")
    khu_detail(HERE / "khu-2027-econ-schedule.png", "1단계 발표 11월 25일(수) · 정경대학 면접 12월 5일(토) 14:00~18:00 서울캠퍼스")
    make_structure(HERE / "structure-econ.png", [
        "경제학은 사람들의 선택을 수식으로 모형화하고 자료로 검증하는 학문이라 수학이 필수라고 생각해서, 미적분과 확률과 통계를 모두 이수했습니다.",
        "고2 때 '한정된 용돈으로 간식과 문구를 살 때 만족이 가장 커지는 조합'을 미분으로 풀어 보는 탐구를 했고, 한계효용이 같아지는 지점이 최적이라는 것을 직접 계산했습니다.",
        "경제학에서 말하는 '한계'가 결국 미분이고, 수학은 경제학을 정확하게 말하기 위한 언어라는 것을 배웠습니다.",
        "경제학과에서 미시경제학과 계량경제학을 제대로 배우기 위해 지금은 통계를 보강하고 있고, 자료로 인과를 따지는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    names = sys.argv[1:] or ["jobs_padm", "jobs_eng", "jobs_kor", "jobs_econ"]
    for name in names:
        try:
            globals()[name]()
            print("OK", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
