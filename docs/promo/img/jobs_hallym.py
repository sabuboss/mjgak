# 한림대학교 학생부종합 학교생활우수자전형 블로그 글 이미지. python jobs_hallym.py
# 디자인본 PDF 120쪽: PDF 1~11쪽은 표지·달력·목차·홍보, PDF 12쪽부터 인쇄 쪽수 = PDF 쪽수.
# 선행학습 영향평가 결과보고서(pipeline/raw/hallym/2026/)는 재배포 금지 폴더라 캡처하지 않는다.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

P = str(SRC / "m_한림대학교.pdf")
U, LBL = "한림대학교", "2027학년도 수시모집요강"


def jobs_hallym():
    make_thumb(HERE / "thumb-hallym.png", "한림대 면접", line2="학교생활우수자", line3="예상 질문 7개 총정리")
    make_capture(HERE / "hallym-2027-method.png", P, 24, "2. 전형방법: 단계별 전형", "※ 계산과정에서",
                 U, f"{LBL} 24쪽", "1단계 서류 100% 4배수(의학과 일부 전형 5배수) · 2단계 70 + 면접 30",
                 start_pad=8, end_pad=1, lr=40)
    make_capture(HERE / "hallym-2027-rules.png", P, 25, "3. 선발원칙", ("after", "전체 이수단위 합"),
                 U, f"{LBL} 25쪽", "면접 결시·보정 전 면접총괄 75점 미만 등 불합격 · 동점자 처리기준",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "hallym-2027-schedule.png", P, 24, "1. 전형일정", "2. 전형방법: 단계별 전형",
                 U, f"{LBL} 24쪽", "1단계 발표 12/3(목) 16:00 · 면접 12/8(화)·12/9(수) · 발표 12/17",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "hallym-2027-interview.png", P, 88, "나) 평가영역 및 주요내용", "[면접평가 점수산출 예시]",
                 U, f"{LBL} 88쪽", "의학과 제외: 서류검증 50%(개별문항) · 인성 50%(공통문항)",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "hallym-2027-format.png", P, 93, "5. 면접 진행방식", ("after", "기타 면접과 관련된 세부사항"),
                 U, f"{LBL} 93쪽", "학생부종합 1:2 15분 내외 · 의학과 MMI 3개 면접실 각 10분",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "hallym-2027-caution.png", P, 91, "4. 면접 시 유의사항", ("after", "학교장의 참가 허락을 받은 교외 수상실적이라도"),
                 U, f"{LBL} 91쪽", "공인어학·교외 수상 언급 시 감점 등 · 교과명 교외 대회 수상은 0점(불합격)",
                 start_pad=8, end_pad=8, lr=40)
    make_capture(HERE / "hallym-2027-mmi.png", P, 88, "2) 의학과", ("after", "의사소통능력, 대인관계능력 등 파악"),
                 U, f"{LBL} 88쪽", "의학과: 인성 40% · 상황 30% · 모의상황 30%, 영역별 면접위원 2인",
                 start_pad=8, end_pad=10, lr=40)
    make_structure(HERE / "structure-hallym.png", [
        "정보 수업에서 우리 반 급식 잔반을 2주 동안 기록해 메뉴별로 비교했고, 저는 자료 정리를 맡았습니다.",
        "처음에는 '많이 남음, 조금 남음'으로 적어 친구마다 기준이 달랐습니다.",
        "식판 사진을 찍어 남은 칸 수로 세기로 바꾸자 기록이 하나로 맞춰졌고, 기준을 먼저 정해야 데이터가 쓸모 있다는 것을 배웠습니다.",
        "인공지능컴퓨팅학부에서 데이터를 모으는 단계부터 설계하는 법을 배우고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_hallym()
