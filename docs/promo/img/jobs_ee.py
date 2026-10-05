# 전기전자공학과 블로그 이미지. python jobs_ee.py
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure


def jobs_ee():
    make_thumb(HERE / "thumb-ee.png", "전기전자공학과")
    # 광운대 참빛인재Ⅰ 면접형
    make_capture(HERE / "kw-2027-ee-track.png", pdf("광운대학교"), 19, "학생부종합【광운참빛인재전형", ("after", "600점/0점"),
                 "광운대학교", "2027학년도 수시모집요강 19쪽", "참빛인재Ⅰ 면접형 전자공학과 18명·전기공학과 10명 · 3.5배수 · 60% + 면접 40% · 최저 없음", start_pad=10, end_pad=3)
    make_capture(HERE / "kw-2027-ee-interview.png", pdf("광운대학교"), 46, "2. 면접평가 안내", "학생부종합【소프트웨어우수인재전형】",
                 "광운대학교", "2027학년도 수시모집요강 46쪽", "2인 개별 대면 10분 이내 · 문제 제시형 없음 · 발전가능성 45% + 종합적사고력 30% + 인성 25%", start_pad=10, end_pad=8)
    make_capture(HERE / "kw-2027-ee-schedule.png", pdf("광운대학교"), 21, "6. 모집단위별 면접 일자", ("after", "반도체시스템공학전공"),
                 "광운대학교", "2027학년도 수시모집요강 21쪽", "면접 10월 31일(토)·11월 1일(일) · 전자공학과·전자통신·반도체시스템은 양일 중 하루 배정", start_pad=10, end_pad=8)
    # 명지대 명지인재면접전형
    make_capture(HERE / "mju-2027-ee-interview.png", pdf("명지대학교"), 50, "4. 전형방법", ("after", "자기주도성, 도전정신"),
                 "명지대학교", "2027학년도 수시모집요강 48쪽(PDF 50쪽)", "명지인재면접 전기정보 8명·전자 13명 · 4배수 · 70% + 면접 30% · 심층면접 10분 · 진로역량 40%", start_pad=10, end_pad=8)
    make_capture(HERE / "mju-2027-ee-schedule.png", pdf("명지대학교"), 49, "3. 전형일정", ("after", "전형일정 상세내용은 p. 10 참조"),
                 "명지대학교", "2027학년도 수시모집요강 47쪽(PDF 49쪽)", "1단계 발표 11월 20일(금) · 자연캠퍼스 모집단위 면접 11월 28일(토) · 면접은 서울 인문캠퍼스에서", start_pad=10, end_pad=8)
    # 숭실대 SSU미래인재 면접형
    make_capture(HERE / "ssu-2027-ee-method.png", pdf("숭실대학교"), 18, "전형요소 및 반영 비율", "동점자 처리 기준",
                 "숭실대학교", "2027학년도 수시모집요강 13쪽(PDF 18쪽)", "SSU미래인재 면접형 전기공학부 24명·지능전자공학부 30명 · 3.5배수 · 50% + 면접 50% · 0점이면 불합격", start_pad=36, end_pad=20)
    make_capture(HERE / "ssu-2027-ee-interview.png", pdf("숭실대학교"), 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"),
                 "숭실대학교", "2027학년도 수시모집요강 57쪽(PDF 62쪽)", "서류 기반 블라인드 12분 · 전공적합성 50% + 잠재력 50% · 면접질문 예시 공개 · 11월 27일(금)", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-ee.png", [
        "전기는 에너지를 만들어 보내는 쪽, 전자는 그 에너지로 신호를 다루는 쪽이고, 저는 신호를 다루는 전자 쪽에 더 끌려서 지원했습니다.",
        "고2 때 아두이노로 초음파 센서 주차 경보기를 만들었는데, 센서 값이 튀어서 경보가 오작동했고 3주 동안 평균 필터를 넣어 고쳤습니다.",
        "회로를 연결하는 것보다 노이즈를 걸러 신호를 믿을 수 있게 만드는 것이 전자공학의 핵심이라는 것을 배웠습니다.",
        "전기전자공학과에서 회로이론과 신호처리를 제대로 배워, 센서 하나의 값도 믿을 수 있게 만드는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    try:
        jobs_ee()
        print("OK")
    except Exception:
        traceback.print_exc()
