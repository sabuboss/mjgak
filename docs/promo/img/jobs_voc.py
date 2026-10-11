# 마이스터고·특성화고 졸업(예정)자 면접 블로그 글 이미지. python jobs_voc.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

LBL = "2027학년도 수시모집요강"
SG, U_SG = pdf("서강대학교"), "서강대학교"
JB, U_JB = pdf("전북대학교"), "전북대학교"
DG, U_DG = pdf("동국대학교"), "동국대학교"


def jobs_voc():
    make_thumb(HERE / "thumb-voc.png", "특성화고 면접", line2="마이스터고·재직자", line3="질문 6개 답변 예시")

    # 서강대 학생부종합(특성화고교졸업자)
    make_capture(HERE / "sogang-2027-voc-track.png", SG, 27, "5. 학생부종합(특성화고교졸업자)", "라. 평가방법",
                 U_SG, f"{LBL} 27쪽", "정원 외 6명 · 1단계 서류 100%로 5배수 · 2단계 1단계 80% + 면접 20%",
                 start_pad=10, end_pad=8)
    make_capture(HERE / "sogang-2027-voc-interview.png", SG, 28, "바. 면접평가 안내", ("after", "종합적으로 평가"),
                 U_SG, f"{LBL} 28쪽", "면접위원 2명 · 7분 내외 블라인드 개별 면접 · 교복 착용 금지",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "sogang-2027-voc-schedule.png", SG, 12, "1단계 합격자 발표", "최초 합격자 발표",
                 U_SG, f"{LBL} 12쪽", "학생부종합(특성화고교졸업자) 1단계 발표 11월 18일(수) · 면접 11월 28일(토)",
                 start_pad=7, end_pad=8)

    # 전북대 학생부종합(특성화고교졸업자)
    make_capture(HERE / "jbnu-2027-voc-track.png", JB, 39, "특성화고교졸업자전형", "나. 제출서류",
                 U_JB, f"{LBL} 39쪽", "특성화고 졸업(예정)자 · 마이스터고 졸업(예정)자는 제외",
                 start_pad=12, end_pad=8)
    make_capture(HERE / "jbnu-2027-voc-method.png", JB, 17, "가. 전형 방법", ("after", "각 단계별 평가 시"),
                 U_JB, f"{LBL} 17쪽", "1단계 서류 3배수(300%) · 2단계 1단계 800점 + 면접 200점",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "jbnu-2027-voc-interview.png", JB, 19, "나. 면접", "⑤ 유의사항",
                 U_JB, f"{LBL} 19쪽", "면접위원 3인 · 10분 내외 블라인드 · 11월 26일(목) 1일차",
                 start_pad=10, end_pad=6)

    # 동국대 학생부종합(특성화고등을졸업한재직자-면접형)
    make_capture(HERE / "dongguk-2027-voc-track.png", DG, 37, "학생부종합[특성화고등을졸업한재직자-면접형]", "산업체 범위 및 재직기간",
                 U_DG, f"{LBL} 35쪽(PDF 37쪽)", "미래융합대학 3개 학과 58명 · 산업체 통산 3년 이상 재직",
                 start_pad=10, end_pad=6)
    make_capture(HERE / "dongguk-2027-voc-method.png", DG, 38, "전형방법", "선발원칙 및 동점자",
                 U_DG, f"{LBL} 36쪽(PDF 38쪽)", "1단계 2.5배수 · 1단계 70% + 면접 30% · 면접위원 2인 7분 내외",
                 start_pad=14, end_pad=12)
    make_capture(HERE / "dongguk-2027-voc-schedule.png", DG, 40, "전형일정", "면접일정",
                 U_DG, f"{LBL} 38쪽(PDF 40쪽)", "1단계 11월 13일(금) · 면접 12월 12일(토)~13일(일)",
                 start_pad=14, end_pad=12)

    make_structure(HERE / "structure-voc.png", [
        "취업도 진지하게 고민했지만, 설비가 왜 그렇게 움직이는지 원리를 더 배우고 싶어서 진학을 선택했습니다.",
        "냉동공조과 실습에서 같은 장비인데도 날마다 목표 온도까지 내려가는 시간이 달랐고, 이유를 설명하려니 열과 압력의 계산에서 막혔습니다.",
        "정해진 순서대로 점검하는 것과 원리를 알고 판단하는 것은 다르다는 걸 그때 알았습니다.",
        "대학에서 열역학과 유체역학을 배워 설비를 직접 설계하는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_voc()
