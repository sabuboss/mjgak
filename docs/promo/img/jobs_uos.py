# 서울시립대 학생부종합전형Ⅰ(면접형) 블로그 글 이미지. python jobs_uos.py
# PDF 쪽수 = 인쇄 쪽수 + 2
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

UOS = pdf("서울시립대학교")
U, LBL = "서울시립대학교", "2027학년도 수시모집요강"


def jobs_uos():
    make_thumb(HERE / "thumb-uos.png", "서울시립대", line2="학생부종합Ⅰ 면접형", line3="면접 예상 질문 7개 총정리")
    make_capture(HERE / "uos-2027-int-units.png", UOS, 4, "Ⅱ. 모집단위별", 719.0,
                 U, f"{LBL} 2쪽(PDF 4쪽)", "학생부종합전형Ⅰ 410명 · 기회균형전형Ⅰ 132명 · 사회공헌·통합 46명", start_pad=8, end_pad=6)
    make_capture(HERE / "uos-2027-int-method.png", UOS, 16, "다. 전형요소별", ("after", "1단계 합격자 발표"),
                 U, f"{LBL} 14쪽(PDF 16쪽)", "1단계 서류 100% 3배수 · 2단계 서류 50 + 면접 50 · 11/20 발표 예정", start_pad=10, end_pad=8)
    make_capture(HERE / "uos-2027-int-rule.png", UOS, 17, "신상정보가 평가에", ("after", "영역별 점수에 대한"),
                 U, f"{LBL} 15쪽(PDF 17쪽)", "교복 착용 금지 · 결시는 불합격 · 수능최저 없음 · 동점자 기준", start_pad=10, end_pad=8)
    make_capture(HERE / "uos-2027-int-schedule.png", UOS, 5, "학생부(종합) 전형", "최초합격자 등록",
                 U, f"{LBL} 3쪽(PDF 5쪽)", "1단계 11/20(금) · 면접 11/28(토) 인문·예체능, 11/29(일) 자연", start_pad=12, end_pad=17)
    make_capture(HERE / "uos-2027-int-interview.png", UOS, 16, "[면접평가]", ("after", "면접평가는 블라인드"),
                 U, f"{LBL} 14쪽(PDF 16쪽)", "면접위원 2인 : 지원자 1인 · 약 12분 내외 · 블라인드 면접", start_pad=3, end_pad=8)
    make_capture(HERE / "uos-2027-int-weight.png", UOS, 36, "나. 평가 기준", 570.0,
                 U, f"{LBL} 34쪽(PDF 36쪽)", "서류·면접 모두 학업 35 · 잠재 40 · 사회 25", start_pad=6, end_pad=6)
    make_capture(HERE / "uos-2027-int-items.png", UOS, 36, "2) 평가영역별 평가 사항", ("after", "위 평가사항을 기준으로"),
                 U, f"{LBL} 34쪽(PDF 36쪽)", "평가 항목 6개 · 같은 기준으로 서류평가와 면접평가", start_pad=4, end_pad=8)
    make_structure(HERE / "structure-uos.png", [
        "행정학과에 지원한 이유는 주민이 실제로 겪는 불편을 자료로 확인하고 제도로 고치는 일을 배우고 싶어서입니다.",
        "2학년 사회 수업에서 학교 앞 횡단보도 신호가 짧다는 이야기를 듣고, 친구들과 등교 시간대 보행자 수와 신호 시간을 직접 세어 보았습니다.",
        "기록을 정리하며 불편을 말로 전하는 것보다 숫자로 보여 줄 때 설득력이 생긴다는 것을 알았고, 3학년에는 지역 민원 사례를 찾아 처리 과정을 비교했습니다.",
        "행정학과에서 정책과 지방행정을 공부해, 시민의 불편을 근거로 정책을 설계하는 사람이 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_uos()
