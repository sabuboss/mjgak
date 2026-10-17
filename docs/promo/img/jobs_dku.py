# 단국대 학생부종합 DKU인재(면접형) 블로그 글 이미지. python jobs_dku.py
# 죽전 PDF: 인쇄 쪽수 = PDF 쪽수 - 2. 천안 PDF: 인쇄 57쪽 = PDF 32쪽.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, make_thumb, make_capture, make_structure

JJ = str(SRC / "m_단국대학교(죽전).pdf")
CA = str(SRC / "m_단국대학교(천안).pdf")
U, LBL = "단국대학교", "2027학년도 수시모집요강"


def jobs_dku():
    make_thumb(HERE / "thumb-dku.png", "단국대 면접", line2="DKU인재(면접형)", line3="공개 질문 6개 총정리")
    make_capture(HERE / "dku-2027-units.png", JJ, 32, "159명", "전형방법",
                 U, f"{LBL} 30쪽(PDF 32쪽)", "죽전 159명 · 경영학부 12명 · 법학과·특수교육과 각 10명",
                 start_pad=12, end_pad=10, lr=45)
    make_capture(HERE / "dku-2027-method.png", JJ, 32, "전형방법", ("after", "입실 불가함"),
                 U, f"{LBL} 30쪽(PDF 32쪽)", "1단계 학생부 100% 3배수 · 2단계 1단계 70% + 면접 30% · 최저 없음",
                 start_pad=10, end_pad=8, lr=45)
    make_capture(HERE / "dku-2027-schedule.png", JJ, 26, "2026. 10. 20.(화) 18:00", ("after", "2027. 2. 10.(수)"),
                 U, f"{LBL} 24쪽(PDF 26쪽)", "1단계 11/20(금) 18시 · 면접 인문 12/5(토) · 자연 12/6(일)",
                 start_pad=19, end_pad=16, lr=45)
    make_capture(HERE / "dku-2027-interview.png", JJ, 85, "2. 면접평가", "2) SW인재",
                 U, f"{LBL} 83쪽(PDF 85쪽)", "입학사정관 2인 · 10분 이내 · 진로 50 · 발전가능성 30 · 공동체 20",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "dku-2027-questions.png", JJ, 86, "마. 면접문항", "바. 블라인드",
                 U, f"{LBL} 84쪽(PDF 86쪽)", "대학이 공개한 면접문항 예시 6개",
                 start_pad=10, end_pad=12, lr=45)
    make_capture(HERE / "dku-2027-blind.png", JJ, 86, "바. 블라인드", ("after", "귀가합니다"),
                 U, f"{LBL} 84쪽(PDF 86쪽)", "가번호 블라인드 면접 · 교복 착용 금지 · 인적사항·고교·부모 언급 금지",
                 start_pad=10, end_pad=10, lr=45)
    make_capture(HERE / "dku-2027-cheonan.png", CA, 32, "57명", ("after", "입실 불가함"),
                 U, f"{LBL} 57쪽(천안 PDF 32쪽)", "천안 57명 · 의약 11/28(토) · 문예창작 11/29(일) · 의약은 최저 있음",
                 start_pad=12, end_pad=8, lr=45)
    make_structure(HERE / "structure-dku.png", [
        "전자전기공학과에 관심을 갖게 된 계기는 2학년 물리 시간에 배운 전기 회로를 직접 만들어 본 경험입니다.",
        "수업에서 저항과 전류의 관계를 배운 뒤, 방과 후에 LED 세 개를 직렬과 병렬로 연결해 밝기를 비교했습니다.",
        "직렬로 연결하면 LED가 훨씬 어두워지는 것을 보고, 같은 부품도 연결 방식에 따라 전기가 다르게 흐른다는 것을 알았습니다.",
        "전자전기공학과에서 회로 설계를 제대로 배워, 전기를 덜 쓰는 조명 장치를 만들어 보고 싶습니다.",
    ])


if __name__ == "__main__":
    jobs_dku()
