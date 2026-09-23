@AGENTS.md

# 면접각 (mjgak) — 대입 면접 준비 앱

전체 스펙은 `docs/SPEC.md`. 작업 전 반드시 읽을 것. 작업 순서는 SPEC 8장, 완료 기준은 9장.

## 설계 원칙 (SPEC 1-2, 절대 위반 금지)
1. **생기부 원문은 서버에 저장하지 않는다.** 브라우저에서 파싱 → 요약된 구조화 데이터만 세션 동안 사용. 사용자가 명시적으로 "요약만 저장"을 선택하지 않는 한 서버 전송 없음. LLM에도 요약만 보낸다. 서버 로그·DB·LLM 요청 로그에 원문이 남으면 안 된다.
2. **대학 보고서 원문 PDF를 재배포하지 않는다.** 문항은 구조화·요약해 제공하고 원문은 각 대학 입학처 링크로 연결. 모든 문항 레코드에 `source_url`과 `year` 필수. `data/raw/`는 git 제외.
3. **차별화 축은 지원자 유형별 특화.** 일반고 3학년을 기본값으로 가정하는 UX 문구 금지. 온보딩에서 유형(GENERAL/VOCATIONAL/GED/REPEAT/OVERSEAS_3/OVERSEAS_12/ALTERNATIVE)을 먼저 묻는다.
4. **공개 문항이 없는 대학은 "예상질문"으로 채우되**, 화면에서 `actual`(실제 기출)과 `predicted`(예상)를 항상 구분 표시한다. 구분 없이 섞어 보여주지 않는다.
5. **만 14세 미만은 법정대리인 동의 플로우.** 회원가입에 생년 연령 게이트.

## 확정된 결정 (2026-09-23)
- 서비스명: 면접각 (임시, 슬러그 `mjgak`)
- 스택: Next.js 16 App Router + TypeScript + Tailwind 4 / Drizzle ORM + SQLite(better-sqlite3, 배포 시 Postgres 전환 가능) / zod / `@anthropic-ai/sdk`
- 파이프라인: Python 3.10 (`pipeline/`), requests + pymupdf + anthropic
- LLM 모델: `claude-sonnet-5`. 키는 `ANTHROPIC_API_KEY` 환경변수, 서버 라우트(`src/app/api/**`)에서만 호출. 클라이언트 노출 금지.
- 프롬프트는 `prompts/*.md`에 파일로 두고 버전 관리.
- Phase 1에 결제·이용권·음성/영상 모의면접 넣지 않음.

## 레이아웃
- `src/app` 화면, `src/app/api` 서버 라우트, `src/db` Drizzle 스키마·시드, `src/lib` 공용 로직
- `data/seed/universities.json`, `data/seed/profiles/{code}.json` 시드 데이터
- `pipeline/` Python 수집·파싱 (`pipeline/parsers/{univ_code}.py`, 공통 인터페이스 `parse(pdf_path) -> list[QuestionRecord]`)
- `docs/` 스펙·설계 문서

## 명령
- `npm run dev` 개발 서버, `npm run build`, `npm run lint`, `npm test`
- `npm run db:push` 스키마 반영, `npm run db:seed` 시드 로드
- 파이프라인: `cd pipeline && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt`, 실행법은 `pipeline/README.md`
