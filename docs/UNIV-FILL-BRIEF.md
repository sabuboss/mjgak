# 대학 2027 면접 정보 채우기 지침 (2차, 2026-10-11)

저장소 ROOT = `C:\Users\nkkim\my-html-project\mjgak`. 애드센스가 "가치가 별로 없는 콘텐츠"로 거절했다.
원인은 대학 이름만 바뀐 템플릿 대학 페이지다. 맡은 대학마다 2027학년도 수시모집요강에서 **확인한 사실**로
`site/content/rich/univ/<code>.json` 을 만든다. 형식과 공통 규칙은 `docs/SITE-RICH-BRIEF.md` 의 0번(공통 규칙)과 2번(대학 rich 파일)을 그대로 따른다.
예시 파일: `site/content/rich/univ/soongsil.json`, `duksung.json`, `eulji.json` 을 먼저 읽고 같은 수준으로 쓴다.

## 모집요강 PDF 구하기
1. 이미 있으면 `docs/promo/img/src/m_<대학명>.pdf` 를 쓴다(대학명 = university_profiles*.json 의 name, 괄호 포함 그대로일 수 있음).
2. 없으면 CDN 에서 받는다. 대학명은 정식 이름(예: 한양대학교, 연세대학교(미래)는 먼저 `연세대학교(미래)` 로, 안 되면 `연세대학교미래캠퍼스` 등 변형을 2~3개 시도).
   `https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info2026/<대학명>/<대학명>_2027학년도_수시모집요강.pdf`
   한글은 URL 인코딩. python `urllib.request` 또는 `curl -sL -o`. **TLS 검증을 끄지 않는다**(verify=False, -k 금지). 실패하면 그 대학은 건너뛰고 보고한다.
   받은 파일은 `docs/promo/img/src/m_<대학명>.pdf` 로 저장(이 폴더는 gitignore).
3. 사관학교·경찰대·KAIST·GIST·DGIST·UNIST·POSTECH·KENTECH 처럼 CDN 에 없을 수 있는 곳은 CDN 만 시도하고, 없으면 건너뛴다. 대학 홈페이지 사진·이미지는 쓰지 않는다.
4. PDF 텍스트는 pymupdf(`import fitz`)로 읽는다. `PYTHONIOENCODING=utf-8`. 면접 관련 쪽(전형 요약표, 전형별 세부, 면접 안내, 일정표, 수능 최저)을 찾아 읽는다.

## 내용 규칙
- tracks 에는 **면접이 있는 수시 전형**을 모두 넣는다(모집인원, 1단계 배수, 반영 비율, 면접 방식·시간·인원, 평가 항목과 배점, 1단계 발표일, 면접일, 수능 최저, 쪽수). 모집단위별 날짜가 다르면 그대로 적는다.
- 그 대학 수시에 면접 전형이 아예 없으면 tracks 는 [] 로 두고 summary 에 "2027학년도 수시에는 면접을 보는 전형이 없습니다(…)"처럼 사실과 쪽수를 적는다. 이것도 수험생에게 유용한 정보다.
- 이미 지난 날짜(오늘 2026-10-11 이전 면접)도 그대로 적고, summary 끝에 "○월 ○일 면접은 이미 끝났습니다"를 붙인다.
- published_questions: 모집요강에 공개한 면접 질문 예시나 기출만. 없으면 [].
- tips 3~5개는 그 대학 면접 방식에서 나오는 구체적 조언(일반론 금지). dress 는 모집요강에 복장 규정이 있을 때만 그 내용, 없으면 "모집요강 면접 안내에 복장 규정은 없습니다." 로 시작.
- depts: `site/content/rich/dept/*.json` 의 y2027.rows 에 이 대학 code 가 나오는 학과 slug/label. 없으면 [].
- checked: "2026-10-11".
- summary 는 2~3문장, 첫 문장에 이 대학 2027 면접의 가장 큰 특징(전형 수, 면접 비율, 방식).
- 사실은 PDF 에서 확인한 것만. 추정 금지. 숫자 옆에 쪽수를 source 로.

## 금지
- `site/build.py`, `site/templates/`, 기존 `site/content/*.json`, 다른 작업자의 대학 파일 수정 금지. git commit/push 금지.
- 맡은 대학 파일만 만든다. 만들고 나서 json.load 로 검증.

## 끝나면 보고
대학별 한 줄(만든 파일 / 핵심 사실 / 못 만든 이유), PDF 를 못 받은 대학 목록.
