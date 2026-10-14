# 사이트 대학 데이터 독립 검수 지침 (2026-10-14)

ROOT = `C:\Users\nkkim\my-html-project\mjgak`. 당신은 이 데이터를 **만들지 않은 검수자**다. 수험생이 mjgak.com 대학 페이지에서
이 정보를 보고 면접일·전형료·준비물을 판단한다. 틀린 숫자 하나가 실제 피해다. 만든 사람의 판단을 믿지 말고 원문 PDF에서 다시 확인한다.

## 대상
1. `site/content/rich/univ/<code>.json` (맡은 대학): summary, tracks[*](name, units, method, interview, criteria, first, date, min, notes, source),
   published_questions(대학 공개 질문 — 원문과 글자 단위), tips, dress.
2. `site/content/rich/dept/*.json` 의 `y2027.rows` 중 `code` 가 맡은 대학인 행 전부(univ, track, unit, method, interview, criteria, first, date, min, source).
   `grep -l '"code": "<code>"' site/content/rich/dept/*.json` 로 찾는다.

## 원문
`docs/promo/img/src/m_<대학명>.pdf` (대학명 = `site/content/university_profiles*.json` 의 name). 예외: cau.pdf(중앙), kyungnam.pdf, nambu.pdf, ulsan.pdf,
단국대 m_단국대학교(죽전).pdf·(천안).pdf, 홍익대 m_홍익대학교(서울).pdf·(세종).pdf, 상명대 m_상명대학교(천안).pdf 포함.
pymupdf 로 텍스트를 뽑고, 표가 이미지면 `page.get_pixmap(dpi=150)` 로 렌더링해 Read 로 눈으로 확인한다. `PYTHONIOENCODING=utf-8`.

## 확인 방법
- 모든 숫자(인원·배수·비율·점수·분·쪽수), 날짜와 요일(달력 검산: `datetime.date(2026,m,d).strftime('%a')`), 전형·모집단위 이름,
  평가 항목·배점, 수능 최저, 결격·불합격 조건, 복장·블라인드 규정을 원문과 대조한다.
- source 의 쪽수는 인쇄 쪽 번호 기준인지 확인(PDF 쪽과 다르면 인쇄 쪽으로 통일).
- 근거 없는 추론·일반화("가장 많이", "거의 나온다", "~일 가능성이 크다", 원문에 없는 조언을 사실처럼)는 원문 사실 문장으로 바꾸거나 지운다.
  tips 는 조언이라도 원문에 근거한 내용이어야 한다.
- 지난 날짜(2026-10-14 이전 면접)는 summary 에 "진행됐습니다"처럼 시점이 바뀌어도 맞는 표현인지.

## 고치는 방법
- 명백한 오류는 json 을 직접 고친다. `json.load` → 수정 → `json.dump(..., ensure_ascii=False, indent=1)`. 키 순서 유지.
  고친 뒤 `json.load` 로 검증. `checked` 는 "2026-10-14" 로 바꾼다(고친 파일만).
- 원문끼리 모순되거나 원문에 없는 정보는 고치지 말고 보고만 한다.
- 맡은 대학 파일과 그 대학 code 행이 있는 dept 파일만 수정. 다른 dept 행·다른 대학·build.py·templates 수정 금지. git commit/push 금지.
  dept 파일은 여러 검수자가 동시에 고칠 수 있으니, 그 파일을 읽은 직후 고치고 곧바로 저장한다(오래 열어 두지 않기).

## 보고 형식
1. 대학별: 확인한 항목 수 / 맞음 / 고친 수
2. 고친 것: `파일 | 필드 | 원래 → 고친 내용 | 근거(PDF 인쇄 쪽)`
3. 보고만 하는 것(판단 필요)
