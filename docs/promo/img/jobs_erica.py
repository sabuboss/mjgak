# 한양대 ERICA 학생부종합(면접형) 면접 블로그 글(naver-108) 이미지. python jobs_erica.py
# PDF: src/m_한양대학교ERICA.pdf (한양대학교 ERICA 2027학년도 수시 모집요강, 116쪽,
#      입학처 goerica.hanyang.ac.kr/upload/BBS0061/202606040853276MB97Z.PDF, 2026-06-04 수정본).
# 인쇄 쪽수 = PDF 쪽수 (표지가 1쪽).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, make_thumb, make_capture, make_structure, pdf

ER = pdf("한양대학교ERICA")
U, LBL = "한양대학교 ERICA", "2027학년도 수시 모집요강"


def jobs_erica():
    make_thumb(HERE / "thumb-erica.png", "한양대 ERICA", line2="학생부종합(면접형)", line3="면접 예상 질문 7개")
    make_capture(HERE / "erica-2027-myeonjeop-method.png", ER, 42, "1. 모집인원", ("after", "면접 최고점"),
                 U, f"{LBL} 42쪽", "LIONS자율전공학부 60명 · 1단계 3배수 · 1단계 70 + 면접 30 · 최저 없음",
                 start_pad=6, end_pad=8, lr=40)
    make_capture(HERE / "erica-2027-myeonjeop-doc.png", ER, 42, "가. 1단계 서류평가", "나. 2단계 면접평가",
                 U, f"{LBL} 42쪽", "1단계 서류평가 학업 역량 70% · 공동체 역량 30%",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "erica-2027-myeonjeop-schedule.png", ER, 43, "7. 전형 일정", ("after", "최초합격자 발표"),
                 U, f"{LBL} 43쪽", "1단계 11/13(금) 18시 예정 · 접수 11/17(화) · 면접 11/21(토)",
                 start_pad=6, end_pad=10, lr=40)
    make_capture(HERE / "erica-2027-myeonjeop-interview.png", ER, 42, "나. 2단계 면접평가", ("after", "책임은 지원자 본인에게 있음"),
                 U, f"{LBL} 42쪽", "다대일 면접 10분 내외 · 통합적 사고역량 70 · 의사소통역량 30",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "erica-2027-myeonjeop-tie.png", ER, 43, "5. 동점자 처리기준", "6. 제출서류",
                 U, f"{LBL} 43쪽", "동점자: 면접 성적 → 서류 학업 역량 → 면접 통합적 사고역량",
                 start_pad=6, end_pad=8, lr=40)
    make_capture(HERE / "erica-2027-lions-major.png", ER, 22, "LIONS칼리지는 LIONS자율전공학부", ("after", "B0 이상 1과목"),
                 U, f"{LBL} 22쪽", "2학년 진급 때 전공 선택 · 인원 제한 없음 · 일부 학과 이수 요건",
                 start_pad=3, end_pad=17, lr=40)
    make_structure(HERE / "structure-erica.png", [
        "가장 깊이 탐구한 것은 2학년 물리학 시간에 배운 전력 계산을 우리 교실 멀티탭에 적용해 본 일입니다.",
        "수업에서 전력은 전압과 전류의 곱이라고 배운 뒤, 교실 멀티탭 세 개에 연결된 기기를 적고 소비전력을 더해 비교했습니다.",
        "한 멀티탭에 전열기 두 대가 몰려 있어 허용 전력에 가까웠고, 배운 공식이 교실 안전 문제와 바로 이어진다는 것을 배웠습니다.",
        "LIONS자율전공학부에서 1년 동안 전자공학부와 산업경영공학과 수업을 들어 보고, 전기를 안전하게 쓰는 설계를 공부할 전공을 고르고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_erica()
