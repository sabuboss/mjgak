# 경희대 학생부종합 네오르네상스전형 블로그 글 이미지. python jobs_khu_neo.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KHU = pdf("경희대학교")
U, LBL = "경희대학교", "2027학년도 수시 신입생 모집요강"


def jobs_khu_neo():
    make_thumb(HERE / "thumb-khu-neo.png", "경희대 면접", line2="네오르네상스전형", line3="예상 질문 7개 총정리")
    make_capture(HERE / "khu-2027-neo-units.png", KHU, 39, "1. 모집단위 및 모집인원", ("after", "그 외 학과는 3배수"),
                 U, f"{LBL} 37쪽(PDF 39쪽)", "네오르네상스 1,076명 · 의예·한의예·치의예·약학과 4배수, 그 외 3배수",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "khu-2027-neo-method.png", KHU, 40, "3. 전형 방법", ("after", "※ 서류평가 및 면접평가 안내는"),
                 U, f"{LBL} 38쪽(PDF 40쪽)", "1단계 서류 100% 3배수(의·약학 4배수) · 2단계 1단계 70 + 면접 30",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "khu-2027-neo-tie.png", KHU, 41, "4. 선발원칙 및 동점자 처리기준", "5. 전형일정 및 면접평가 상세일정",
                 U, f"{LBL} 39쪽(PDF 41쪽)", "면접 결시는 전형 대상 제외 · 2단계 동점자는 서류 총점이 1순위",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "khu-2027-neo-schedule.png", KHU, 41, "5. 전형일정 및 면접평가 상세일정", ("after", "2026. 12. 18(금) 18:00"),
                 U, f"{LBL} 39쪽(PDF 41쪽)", "1단계 11/25(수) 18:00 · 고사장 확인 12/2 · 면접 12/5~6 · 최초 12/18",
                 start_pad=10, end_pad=12)
    make_capture(HERE / "khu-2027-neo-detail.png", KHU, 42, "[면접평가 상세일정]", ("after", "만 진행합니다"),
                 U, f"{LBL} 40쪽(PDF 42쪽)", "단과대학별 날짜·캠퍼스·오전/오후 · 의학계열 12/6(일) 14:00~18:00",
                 start_pad=10, end_pad=12)
    make_capture(HERE / "khu-2027-neo-interview.png", KHU, 64, "2. 학생부종합전형 면접평가", "3. 학교생활기록부 교과 성적",
                 U, f"{LBL} 62쪽(PDF 64쪽)", "공통질문 + 개인 서류확인 · 2:1 10분 내외 · 인성 50 · 전공적합성 50",
                 start_pad=10, end_pad=10)
    make_capture(HERE / "khu-2027-neo-med.png", KHU, 40, "※ 대학수학능력시험(수능) 최저학력기준", "3. 전형 방법",
                 U, f"{LBL} 38쪽(PDF 40쪽)", "의예·한의예·치의예·약학과만 최저: 3개 합 4 이내 + 한국사 5등급",
                 start_pad=10, end_pad=10)
    make_structure(HERE / "structure-khu-neo.png", [
        "간호학과에 지원한 이유는 환자가 자기 치료 과정을 정확히 이해하도록 돕는 간호사가 되고 싶어서입니다.",
        "2학년 생명과학 시간에 만성질환을 조사하다가, 같은 약도 복용 시간을 잘못 이해하면 효과가 떨어진다는 내용을 읽었습니다.",
        "정확한 정보도 받는 사람이 이해해야 의미가 있다는 것을 알게 됐고, 보건 동아리에서 감기약 복용 안내문을 만들 때 어려운 용어를 그림과 짧은 문장으로 바꿨습니다.",
        "경희대 간호학과에서 환자 교육과 의사소통을 깊이 배워, 환자의 눈높이에서 설명하는 간호사가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_khu_neo()
