# 건국대 학생부종합 KU자기추천전형 블로그 글 이미지. python jobs_konkuk.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

KK = pdf("건국대학교")
U, LBL = "건국대학교", "2027학년도 수시모집요강"


def jobs_konkuk():
    make_thumb(HERE / "thumb-konkuk.png", "건국대 면접", line2="KU자기추천", line3="예상 질문 7개 총정리")
    make_capture(HERE / "konkuk-2027-self-units.png", KK, 29, "1. 모집단위 및 모집인원", ("after", "무전공 모집단위임"),
                 U, f"{LBL} 29쪽", "KU자기추천 903명 · (★) 12/5(토) 면접, 그 외 12/6(일)", start_pad=10, end_pad=10)
    make_capture(HERE / "konkuk-2027-self-method.png", KK, 29, "2. 지원자격", ("after", "학생부위주전형 안내"),
                 U, f"{LBL} 29쪽", "1단계 서류 100% 3배수 · 2단계 1단계 70 + 면접 30 · 수능최저 없음", start_pad=10, end_pad=4)
    make_capture(HERE / "konkuk-2027-self-tie.png", KK, 32, "9. 동점자 처리기준", ("after", "서류 학업역량 점수 우수자"),
                 U, f"{LBL} 32쪽", "2단계 동점자 1~3순위는 모두 면접 점수", start_pad=10, end_pad=12, end_idx=-1)
    make_capture(HERE / "konkuk-2027-self-schedule.png", KK, 31, "7. 전형일정", "8. 제출서류",
                 U, f"{LBL} 31쪽", "1단계 11/20(금) 14시 예정 · 전형료 11/23 14시까지 · 면접 12/5~6", start_pad=10, end_pad=10)
    make_capture(HERE / "konkuk-2027-self-interview.png", KK, 72, "3. 학생부종합 면접평가", 226.5,
                 U, f"{LBL} 72쪽", "평가자 2인 개별면접 10분 내외 · 서류 진위 확인 및 인성평가", start_pad=10)
    make_capture(HERE / "konkuk-2027-self-eval.png", KK, 73, "5) 평가요소 및 평가항목", ("after", "매우 미흡"),
                 U, f"{LBL} 73쪽", "학업역량 300 · 진로역량 400 · 공동체역량 300", start_pad=10, end_pad=12)
    make_capture(HERE / "konkuk-2027-self-banned.png", KK, 72, "※ 학교생활기록부 기재금지 항목", ("after", "독서활동 대입 미반영"),
                 U, f"{LBL} 72쪽", "수상·공인어학·대학명·기관명·부모 직업 등은 면접에서 언급 금지", start_pad=13, end_pad=12)
    make_structure(HERE / "structure-konkuk.png", [
        "미디어커뮤니케이션학과에 지원한 이유는 같은 사실도 전달 방식에 따라 받아들이는 사람이 달라지는 까닭을 공부하고 싶어서입니다.",
        "2학년 국어 시간에 같은 사건을 다룬 기사 두 편의 제목을 비교했는데, 반 친구들의 반응이 제목에 따라 크게 갈렸습니다.",
        "그때부터 방송부에서 학교 소식 영상을 만들 때 자막을 두 가지로 써 보고, 어느 쪽이 더 정확하게 이해되는지 친구들에게 확인하게 됐습니다.",
        "미디어커뮤니케이션학과에서 미디어가 사람들의 생각에 미치는 영향을 배워, 정확하게 전달하는 콘텐츠를 만들고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_konkuk()
