# 면접각 데이터 파이프라인

대학 입학처가 공개한 면접·구술고사 PDF → 문항 단위 JSON. SPEC 4장.

```
data/seed/universities.json   (대학·출처 URL 시드)
   ↓ python run.py fetch <univ>
pipeline/raw/<univ>/<year>/*.pdf   (git 제외, 재배포 금지)
   ↓ python run.py parse <univ> [--llm]
pipeline/out/<univ>.jsonl          (문항 레코드, DB 시드 입력)
   ↓ npm run db:seed (앱 쪽)
```

## 설치

```bash
cd pipeline
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt      # Windows
# source .venv/bin/activate && pip install -r requirements.txt   # mac/linux
```

사내망처럼 TLS 검사 프록시가 있으면 `truststore` 가 OS 인증서 저장소를 쓰므로 그대로 동작한다.

## 사용

```bash
.venv/Scripts/python run.py fetch snu            # 15개 PDF 다운로드 (2022~2026 + 2028 예시)
.venv/Scripts/python run.py parse snu            # 규칙 기반 파싱 (API 키 불필요)
.venv/Scripts/python run.py parse snu --llm      # + Claude 로 문항 단위 정밀 구조화 (ANTHROPIC_API_KEY 필요)
.venv/Scripts/python run.py stats snu
```

`--llm` 은 저장소 루트의 `.env.local` 에서 `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`(기본 claude-sonnet-5) 을 읽는다.
프롬프트는 `prompts/structure_questions.md`. 블록당 1회 호출하며 system 프롬프트는 캐시된다.

## 대학별 파서 추가

`parsers/<code>.py` 에 두 함수를 만든다.

```python
def segment(pdf_path, meta) -> list[Block]        # LLM 에 넣을 블록 단위로 자르기
def parse(pdf_path, meta) -> list[QuestionRecord] # 규칙 기반 rough 레코드
```

`meta` 는 `universities.json` 의 source 항목 + `university_code`. 레코드 스키마는 `mjgak_pipeline/models.py`.

## 서울대(snu) 메모

- 선행학습 영향평가 **보고서**(`kind=report`)에는 출제의도·검토의견만 있고 **문항 원문이 없다**. 문항은 같은 날 올라오는 "면접 및 구술고사 문항" 게시글의 PDF 2개(일반전형 제시문 면접 / 적성·인성면접)에 있다. 보고서는 파싱 대상에서 제외.
- 게시판 파일은 게시글을 먼저 열어 세션 쿠키를 받고 Referer 를 붙여야 내려온다 (`fetch.py` 처리).
- 수학·과학 문항은 수식이 글꼴 글리프로 박혀 있어 텍스트 추출 시 변수·기호가 빠진다("자연수 에 대하여"). 이런 문항은 `text` 만으로 불완전하므로 앱에서 반드시 출처 링크를 함께 보여주고, 검수 시 `verified` 를 신중히 켠다.
- 2028학년도 예시 문항 PDF 의 헤더는 "분석적 주제토론 [인문학]" 식이며 `kind=example` 로 들어간다.
- PDF 첫 줄에 "상업적 목적 사용 불가, 변형·발췌 금지" 문구가 있다. 앱에는 문항·요약만 싣고 원문 PDF 는 서빙하지 않으며 출처 링크를 항상 표시한다 (SPEC 1-2 원칙 2). 상업화 전 법률 검토 필요.

## 출력 파일

- `out/<univ>_<year>_<kind>.json` : 파일별 레코드 (가독용)
- `out/<univ>.jsonl` : 대학 전체 (DB 시드 입력)
- `out/_*_text.txt` : 디버그용 텍스트 덤프 (git 제외)
