# 면접각 (mjgak)

대학별 공개 면접 기출 + LLM 예상질문 + 지원자 유형별(특성화고·검정고시·재수생·재외국민·대안학교) 맞춤 답변 코칭 웹앱.

- 스펙: [docs/SPEC.md](docs/SPEC.md)
- 개발 규칙: [CLAUDE.md](CLAUDE.md)

## 실행

```bash
npm install
cp .env.example .env.local   # ANTHROPIC_API_KEY 입력
npm run db:push              # SQLite 스키마 생성 (data/mjgak.db)
npm run db:seed              # 대학·지원자 유형 시드 로드
npm run dev                  # http://localhost:3000
```

## 데이터 파이프라인 (Python)

```bash
cd pipeline
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

자세한 사용법은 [pipeline/README.md](pipeline/README.md).

## 진행 상황 (SPEC 8장 작업 순서)

- [x] 1. 레포 초기화, SPEC 저장, CLAUDE.md
- [ ] 2. pipeline/ 서울대 end-to-end
- [ ] 3. DB 스키마 + 시드 로더
- [ ] 4. 연세대·고려대·성균관대 파서, /admin/review
- [ ] 5. /univ/[id]
- [ ] 6. 온보딩 + 예상질문 API
- [ ] 7. 답변 코칭 API + /practice
- [ ] 8. 생기부 클라이언트 파싱
- [ ] 9. 나머지 대학 확장
- [ ] 10. 배포 + 랜딩 + 대기자 수집
