# 반도체공학과·미디어커뮤니케이션학과·화학공학과·생명과학과 블로그 이미지. python jobs_batch4.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure

KW = pdf("광운대학교"); MJU = pdf("명지대학교"); SSU = pdf("숭실대학교"); KHU = pdf("경희대학교"); AJOU = pdf("아주대학교")


def kw_track(out, note):
    make_capture(out, KW, 19, "학생부종합【광운참빛인재전형", ("after", "600점/0점"), "광운대학교", "2027학년도 수시모집요강 19쪽", note, start_pad=10, end_pad=3)


def kw_interview(out):
    make_capture(out, KW, 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】", "광운대학교", "2027학년도 수시모집요강 46쪽",
                 "2인 개별 대면 10분 이내 · 문제 제시형 없음 · 발전가능성 45% + 종합적사고력 30% + 인성 25%", start_pad=10, end_pad=8)


def kw_schedule(out, note, end=("after", "반도체시스템공학전공")):
    make_capture(out, KW, 21, "6. 모집단위별 면접 일자", end, "광운대학교", "2027학년도 수시모집요강 21쪽", note, start_pad=10, end_pad=3)


def mju_interview(out, note):
    make_capture(out, MJU, 50, "4. 전형방법", ("after", "자기주도성, 도전정신"), "명지대학교", "2027학년도 수시모집요강 48쪽(PDF 50쪽)", note, start_pad=10, end_pad=8)


def mju_schedule(out, note):
    make_capture(out, MJU, 49, "3. 전형일정", ("after", "전형일정 상세내용은 p. 10 참조"), "명지대학교", "2027학년도 수시모집요강 47쪽(PDF 49쪽)", note, start_pad=10, end_pad=8)


def ssu_method(out, note):
    make_capture(out, SSU, 18, "전형요소 및 반영 비율", "동점자 처리 기준", "숭실대학교", "2027학년도 수시모집요강 13쪽(PDF 18쪽)", note, start_pad=36, end_pad=20)


def ssu_interview(out, note="서류 기반 블라인드 12분 · 전공적합성 50% + 잠재력 50% · 면접질문 예시 공개 · 11월 27일(금)"):
    make_capture(out, SSU, 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"), "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", note, start_pad=10, end_pad=8)


def khu_interview(out):
    make_capture(out, KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적", "경희대학교", "2027학년도 수시모집요강 62쪽(PDF 64쪽)",
                 "공통질문 + 서류확인 면접 · 출제문항 없음 · 2:1 개인면접 10분 · 인성 50% + 전공적합성 50%", start_pad=10, end_pad=8)


def khu_schedule(out, note):
    make_capture(out, KHU, 41, "5. 전형일정 및 면접평가 상세일정", ("after", "2026. 12. 18(금) 18:00"), "경희대학교", "2027학년도 수시모집요강 39쪽(PDF 41쪽)", note, start_pad=10, end_pad=10)


def khu_method(out, note):
    make_capture(out, KHU, 40, "3. 전형 방법", "※ 서류평가 및 면접평가 안내는", "경희대학교", "2027학년도 수시모집요강 38쪽(PDF 40쪽)", note, start_pad=10, end_pad=8)


def jobs_semi():
    make_thumb(HERE / "thumb-semi.png", "반도체공학과")
    kw_track(HERE / "kw-2027-semi-track.png", "참빛인재Ⅰ 면접형 반도체시스템공학전공 14명 · 3.5배수 · 60% + 면접 40% · 최저 없음")
    kw_interview(HERE / "kw-2027-semi-interview.png")
    kw_schedule(HERE / "kw-2027-semi-schedule.png", "면접 10월 31일(토)·11월 1일(일) · 반도체시스템공학전공은 양일 중 하루 배정 · 1단계 발표 10월 28일")
    mju_interview(HERE / "mju-2027-semi-interview.png", "명지인재면접 반도체공학부 6명 · 4배수 · 70% + 면접 30% · 심층면접 10분 · 진로역량 40%")
    mju_schedule(HERE / "mju-2027-semi-schedule.png", "1단계 발표 11월 20일(금) · 자연캠퍼스 모집단위 면접 11월 28일(토) · 면접은 서울 인문캠퍼스에서")
    khu_method(HERE / "khu-2027-semi-method.png", "네오르네상스 전자공학부 반도체공학과 6명 · 3배수 · 70% + 면접 30% · 수능 최저 없음")
    khu_interview(HERE / "khu-2027-semi-interview.png")
    khu_schedule(HERE / "khu-2027-semi-schedule.png", "1단계 발표 11월 25일(수) · 면접 12월 5~6일 · 전자정보대학은 12월 5일(토) 14:00 국제캠퍼스")
    make_structure(HERE / "structure-semi.png", [
        "반도체 중에서도 회로를 설계하는 쪽이 아니라, 설계한 회로가 실제로 똑같이 찍혀 나오게 만드는 공정 쪽에 관심이 있어서 지원했습니다.",
        "고2 때 물리 탐구로 빛의 회절을 배우다가 반도체 노광 공정이 파장 한계 때문에 EUV로 바뀌었다는 것을 알게 됐고, 보고서를 쓰며 공정 단계를 처음부터 정리했습니다.",
        "반도체는 설계보다 '설계대로 만들 수 있느냐'가 경쟁력이고, 그 한계를 물리가 정한다는 것을 배웠습니다.",
        "반도체공학과에서 소자 물리와 공정을 제대로 배워, 한 세대 더 작은 회로를 실제로 찍어 내는 공정 엔지니어가 되고 싶습니다.",
    ])


def jobs_media():
    make_thumb(HERE / "thumb-media.png", "미디어커뮤니케이션학과")
    kw_track(HERE / "kw-2027-media-track.png", "참빛인재Ⅰ 면접형 미디어커뮤니케이션학부 12명 · 3.5배수 · 60% + 면접 40% · 최저 없음")
    kw_interview(HERE / "kw-2027-media-interview.png")
    kw_schedule(HERE / "kw-2027-media-schedule.png", "미디어커뮤니케이션학부 면접 11월 1일(일) · 1단계 발표 10월 28일(수) · 순서는 발표 시 확정", end=("after", "국제통상학부"))
    khu_method(HERE / "khu-2027-media-method.png", "네오르네상스 미디어학과 25명 · 3배수 · 70% + 면접 30% · 수능 최저 없음")
    khu_interview(HERE / "khu-2027-media-interview.png")
    khu_schedule(HERE / "khu-2027-media-schedule.png", "1단계 발표 11월 25일(수) · 면접 12월 5~6일 · 정경대학(미디어학과)은 12월 5일(토) 14:00 서울캠퍼스")
    ssu_method(HERE / "ssu-2027-media-method.png", "SSU미래인재 면접형 언론홍보학과 4명·글로벌미디어학부 17명 · 3.5배수 · 50% + 면접 50%")
    ssu_interview(HERE / "ssu-2027-media-interview.png")
    make_structure(HERE / "structure-media.png", [
        "기자가 되고 싶어서가 아니라, 같은 사실이 어떤 말로 전해지느냐에 따라 사람들의 판단이 달라지는 과정을 공부하고 싶어서 지원했습니다.",
        "고2 때 학교 신문부에서 급식 만족도 기사를 썼는데, 제목을 '불만 60%'로 뽑은 판과 '만족 40%'로 뽑은 판을 나눠 돌렸더니 댓글 반응이 정반대였습니다.",
        "사실을 고르는 것만큼 사실을 어떻게 놓느냐가 메시지이고, 그 책임이 만드는 사람에게 있다는 것을 배웠습니다.",
        "미디어커뮤니케이션학과에서 저널리즘과 미디어 효과를 제대로 배워, 사람을 움직이되 속이지 않는 콘텐츠를 만드는 사람이 되고 싶습니다.",
    ])


def jobs_chem():
    make_thumb(HERE / "thumb-chem.png", "화학공학과")
    kw_track(HERE / "kw-2027-chem-track.png", "참빛인재Ⅰ 면접형 화학공학과 12명 · 3.5배수 · 60% + 면접 40% · 최저 없음")
    kw_interview(HERE / "kw-2027-chem-interview.png")
    kw_schedule(HERE / "kw-2027-chem-schedule.png", "화학공학과 면접 10월 31일(토) · 1단계 발표 10월 28일(수) · 순서는 발표 시 확정", end=("after", "환경공학과"))
    ssu_method(HERE / "ssu-2027-chem-method.png", "SSU미래인재 면접형 화학공학과 19명 · 3.5배수 · 50% + 면접 50% · 0점이면 불합격")
    ssu_interview(HERE / "ssu-2027-chem-interview.png")
    mju_interview(HERE / "mju-2027-chem-interview.png", "명지인재면접 화공신소재공학부 화학공학전공 6명 · 4배수 · 70% + 면접 30% · 심층면접 10분")
    mju_schedule(HERE / "mju-2027-chem-schedule.png", "1단계 발표 11월 20일(금) · 자연캠퍼스 모집단위 면접 11월 28일(토) · 면접은 서울 인문캠퍼스에서")
    khu_schedule(HERE / "khu-2027-chem-schedule.png", "네오르네상스 화학공학과 11명 · 3배수 · 70% + 면접 30% · 공과대학 면접 12월 6일(일) 09:00 국제캠퍼스")
    make_structure(HERE / "structure-chem.png", [
        "화학과는 '왜 반응하는가'를, 화학공학과는 '그 반응을 공장 규모로 안전하게 돌리려면 어떻게 하는가'를 배우는 곳이라서 화학공학과를 택했습니다.",
        "고2 때 비누 만들기 실험을 비커에서 할 땐 잘 됐는데 양을 10배로 늘리자 열이 몰려 굳지 않았고, 저어 주는 속도와 용기 모양을 바꿔서야 해결했습니다.",
        "같은 반응이라도 크기가 커지면 열과 흐름이 문제가 되고, 그걸 설계하는 것이 화학공학이라는 것을 배웠습니다.",
        "화학공학과에서 반응공학과 공정 설계를 제대로 배워, 실험실의 반응을 공장에서 안전하게 재현하는 엔지니어가 되고 싶습니다.",
    ])


def jobs_bio():
    make_thumb(HERE / "thumb-bio.png", "생명과학과")
    khu_method(HERE / "khu-2027-bio-method.png", "네오르네상스 유전생명공학과 14명·생물학과 16명 · 3배수 · 70% + 면접 30% · 수능 최저 없음")
    khu_interview(HERE / "khu-2027-bio-interview.png")
    khu_schedule(HERE / "khu-2027-bio-schedule.png", "1단계 발표 11월 25일(수) · 생명과학대학 12월 5일(토) 14:00 국제캠퍼스 · 이과대학 생물학과 12월 6일(일) 09:00 서울")
    ssu_method(HERE / "ssu-2027-bio-method.png", "SSU미래인재 면접형 의생명시스템학부 13명 · 3.5배수 · 50% + 면접 50% · 0점이면 불합격")
    ssu_interview(HERE / "ssu-2027-bio-interview.png")
    mju_interview(HERE / "mju-2027-bio-interview.png", "명지인재면접 융합바이오학부 시스템생명과학전공 6명 · 4배수 · 70% + 면접 30% · 심층면접 10분")
    mju_schedule(HERE / "mju-2027-bio-schedule.png", "1단계 발표 11월 20일(금) · 자연캠퍼스 모집단위 면접 11월 28일(토) · 면접은 서울 인문캠퍼스에서")
    make_structure(HERE / "structure-bio.png", [
        "생명과학 중에서도 유전자를 읽는 것보다 '읽은 결과를 믿을 수 있는가'를 따지는 실험 설계 쪽에 관심이 있어서 지원했습니다.",
        "고2 때 항균 실험에서 마늘 추출물이 효과가 있다고 결론 냈는데, 선생님이 '대조군은?'이라고 물으셔서 다시 보니 추출에 쓴 알코올 자체가 균을 죽이고 있었습니다.",
        "결과보다 결과를 의심하는 설계가 먼저이고, 대조군 하나가 결론을 뒤집는다는 것을 배웠습니다.",
        "생명과학과에서 분자생물학과 실험 설계를 제대로 배워, 남이 믿을 수 있는 데이터를 만드는 연구자가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    for name in ["jobs_semi", "jobs_media", "jobs_chem", "jobs_bio"]:
        try:
            globals()[name]()
            print("OK", name)
        except Exception:
            print("FAIL", name)
            traceback.print_exc()
