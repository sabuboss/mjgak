# 숭실대 SSU미래인재(면접형) 블로그 글 이미지. python jobs_ssu.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, pdf, make_thumb, make_capture, make_structure

SSU = pdf("숭실대학교")
U, LBL = "숭실대학교", "2027학년도 수시모집요강"


def jobs_ssu():
    make_thumb(HERE / "thumb-ssu.png", "숭실대 면접", line2="SSU미래인재", line3="질문 예시 7개 총정리")
    make_capture(HERE / "ssu-2027-future-compare.png", SSU, 60, "학생부종합전형 안내", "공정한 학생부종합전형",
                 U, f"{LBL} 55쪽(PDF 60쪽)", "2027 이원화 · 서류형 신설 · 면접형은 진로역량 중심 + 면접으로 전공적합성 심층 평가", start_pad=12, end_pad=10)
    make_capture(HERE / "ssu-2027-future-units.png", SSU, 17, "모집인원", ("after", "배수 선발"),
                 U, f"{LBL} 12쪽(PDF 17쪽)", "SSU미래인재(면접형) 522명 · 인문대학·국제법무·정보보호 3배수, 그 외 3.5배수", start_pad=60, end_pad=10)
    make_capture(HERE / "ssu-2027-future-method.png", SSU, 18, "전형요소 및 반영 비율", 293,
                 U, f"{LBL} 13쪽(PDF 18쪽)", "1단계 서류 100% · 2단계 1단계 50% + 면접 50% · 둘 중 하나라도 0점이면 불합격", start_pad=36)
    make_capture(HERE / "ssu-2027-future-schedule.png", SSU, 18, "전형일정", ("after", "합격자 발표 및 등록 안내"),
                 U, f"{LBL} 13쪽(PDF 18쪽)", "1단계 11월 23일(월) 10:00 · 면접 11월 27일(금) · 최초 합격 12월 18일(금)", start_pad=14, end_pad=8)
    make_capture(HERE / "ssu-2027-future-docs.png", SSU, 61, "미래인재면접형", ("after", "학교폭력 조치사항 반영"),
                 U, f"{LBL} 56쪽(PDF 61쪽)", "면접형 서류평가 · 학업역량 20% + 진로역량 50% + 공동체역량 30%", start_pad=5, end_pad=2, end_idx=-1)
    make_capture(HERE / "ssu-2027-future-interview.png", SSU, 62, "학생부종합전형 면접평가 안내", ("after", "기울였던 노력에 대해 이야기해 주세요"),
                 U, f"{LBL} 57쪽(PDF 62쪽)", "2:1 서류 기반 블라인드 12분 · 전공적합성 50% + 잠재력 50% · 질문 예시 7개", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-ssu.png", [
        "고2 물리 수업에서 전기회로 단원을 배우며 처음으로 '이걸로 무언가를 만들 수 있겠다'고 느낀 것이 전기공학부를 정한 구체적인 계기입니다.",
        "수행평가로 직렬·병렬 회로의 전력 손실을 비교하는 실험을 했는데, 예상과 달리 측정값이 계속 어긋나서 도선 저항까지 계산에 넣어 세 번 다시 측정했습니다.",
        "교과서 공식은 이상적인 조건이고, 실제 회로에서는 작은 손실까지 따져야 한다는 것을 배웠고, 그때부터 전력 손실을 줄이는 기술에 관심이 생겼습니다.",
        "전기공학부에서 전력공학을 제대로 배워, 발전소에서 집까지 오는 동안 사라지는 전기를 줄이는 엔지니어가 되고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_ssu()
