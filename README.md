# 면접각 (mjgak)

대학별 공개 면접 기출 + LLM 예상질문 + 지원자 유형별(특성화고·검정고시·재수생·재외국민·대안학교) 맞춤 답변 코칭 웹앱.

- 스펙: [docs/SPEC.md](docs/SPEC.md) · 개발 규칙: [CLAUDE.md](CLAUDE.md) · 파이프라인: [pipeline/README.md](pipeline/README.md)

## 실행

```bash
npm install
cp .env.example .env.local        # ANTHROPIC_API_KEY, ADMIN_TOKEN 입력 (키가 없어도 템플릿/규칙 모드로 동작)
npm run db:push                   # SQLite 스키마 (data/mjgak.db)
npm run db:seed                   # 대학·유형 템플릿·pipeline/out/*.jsonl 문항 로드
npm run dev                       # http://localhost:3000
```

검증: `npm run typecheck` · `npm run lint` · `npm test` · `npm run build`

## 화면

| 경로 | 내용 |
|---|---|
| `/` | 랜딩, 유형별 진입, 대기자 이메일 |
| `/univ`, `/univ/[code]` | 대학별 공개 기출(연도·전형별, 실제 기출/예시/예상 구분, 출처 링크) — SEO 공개 페이지 |
| `/onboarding` | 유형 → 대학·전형·학과 → 활동(직접 입력 또는 생기부 PDF 브라우저 파싱) → 예상질문 생성 |
| `/practice` | 예상질문 카드 → 답변 → 피드백 → 다시 쓰기. 진행 상황은 IndexedDB(로컬) |
| `/my` | 내 프로필·저장 개수, 모든 데이터 삭제 |
| `/admin/login`, `/admin/review`, `/admin/review/[id]` | 문항 검수(ADMIN_TOKEN 쿠키) |

API: `POST /api/generate`, `POST /api/feedback` (세션 토큰·레이트리밋·동시성 가드), `POST /api/waitlist`

## LLM

- 모델 `claude-sonnet-5` (`ANTHROPIC_MODEL`), 프롬프트 `prompts/*.md` (첫 줄 주석의 vN 이 캐시 키에 포함)
- 키가 없으면 `/api/generate` 는 유형 템플릿 + 대학 공개 문항(템플릿 모드), `/api/feedback` 는 규칙 기반 점검(rules 모드)으로 동작하고 화면에 그 사실을 표시한다.
- 같은 입력의 예상질문 세트는 `llm_cache` 테이블에 캐시된다.
- 원가 추정(sonnet-5 기준): 예상질문 생성 1회 입력 ~6K·출력 ~3K 토큰 ≈ $0.04, 답변 피드백 1회 ≈ $0.01. `LIMIT_*` 환경변수로 상한 조정.

## 보안 (web-launch-security 체크리스트)

- 세션 HMAC 토큰(`APP_SECRET`) 없이는 API 직접 호출 403, 입력은 zod 로 검증(400)
- IP 시간/일 + 전체 일일 레이트리밋(429), 동시 실행 상한(503). Upstash 환경변수가 있으면 인스턴스 간 공유, 없으면 인메모리 폴백
- Cloudflare Turnstile 은 `NEXT_PUBLIC_TURNSTILE_SITE_KEY`/`TURNSTILE_SECRET_KEY` 가 있을 때만 켜짐
- 생기부 원문·답변 원문은 서버 로그에 남기지 않음. API 응답 `Cache-Control: no-store`
- 배포 전 해야 할 것: `APP_SECRET`, `ADMIN_TOKEN` 강한 값으로 교체, Anthropic 콘솔 월 예산·알림, Upstash/Turnstile 계정(선택)

## 데이터 현황 (2026-09-23)

| 대학 | 연도 | 문항 | 출처 형태 |
|---|---|---|---|
| 서울대 | 2022~2026, 2028(예시) | 370 | 면접 및 구술고사 문항 PDF + 적성·인성면접 PDF |
| 고려대 | 2025~2026 | 69 | 선행학습 영향평가 보고서 부록 문항카드 |
| 연세대(서울) | 2024~2026 | 56 | 결과보고서 별책(기출문제) |
| 성균관대 | 2025~2026 | 29 | 학종 면접 기출 PDF (텍스트 품질 낮음 → `--llm` 필요) |

모두 규칙 기반 1차 추출(rough) 상태이며 `verified=false`. `/admin/review` 에서 원문 링크와 대조해 검수한다.
수학·과학 문항은 PDF 수식이 글리프로 박혀 있어 변수·기호가 빠져 있다.

## 진행 상황 (SPEC 8장)

- [x] 1. 레포 초기화, SPEC, CLAUDE.md
- [x] 2. pipeline/ 서울대 end-to-end
- [x] 3. DB 스키마 + 시드 로더 + 유형 템플릿 7종
- [x] 4. 연세대·고려대·성균관대 파서, /admin/review
- [x] 5. /univ/[code]
- [x] 6. 온보딩 + 예상질문 생성 API
- [x] 7. 답변 코칭 API + /practice
- [x] 8. 생기부 클라이언트 파싱
- [ ] 9. 나머지 대학 수집 확장 (경희·중앙·시립·이화·외대·동국·인하·UNIST·에너지공대·교대·육사·부산대)
- [~] 10. 배포 + 랜딩 + 대기자 수집 — 랜딩·대기자 완료, 배포는 미실행

## 완료 기준(SPEC 9장) 대비

- 상위 15개 대학 3개 연도: **4개 대학**만 수집됨 (미달)
- 7개 유형 온보딩 → 예상질문 15개 이상 → 피드백: 템플릿/규칙 모드로 동작 확인. LLM 모드는 API 키 투입 후 확인 필요
- 생기부 원문 서버 미전송: 클라이언트 파싱만 사용, 네트워크 요청 없음 (pdfjs 워커도 동일 출처)
- 모든 문항 `source_url` 있음, 원문 PDF 는 `pipeline/raw/`(git 제외)에만 있고 앱에서 서빙하지 않음
- 데이터 삭제: 로컬(IndexedDB·localStorage) 전량 삭제. 서버 옵트인 저장은 아직 없음
- 375px 모바일: 랜딩·대학·연습 화면 가로 스크롤 없음 확인
