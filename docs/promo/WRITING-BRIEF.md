# 면접각 네이버 블로그 글 작성 지침 (v2 형식)

저장소: `C:\Users\nkkim\my-html-project\mjgak` (이하 ROOT). 오늘은 2026-10-08, 2027학년도 수능은 2026-11-19(목).

## 1. 반드시 먼저 읽을 것

- 형식 견본 두 편을 **처음부터 끝까지** 읽는다: `ROOT/docs/promo/naver-22-화학공학과-v2.md`, `ROOT/docs/promo/naver-18-약학과-v2.md`.
- 이미지 도구: `ROOT/docs/promo/img/promo_style.py` (make_thumb, make_capture, make_structure, pdf) — **수정 금지**. 사용 예: `ROOT/docs/promo/img/jobs_batch4.py` (광운·명지·숭실·경희 공통 헬퍼가 있다. 필요한 헬퍼는 자기 jobs 파일에 복사해서 쓴다).
- 사이트 질문 원본: `ROOT/site/content/departments_*.json`, `new_departments.json` 의 해당 학과 `questions` 6개.
- 학과별 PDF 후보 쪽수: `ROOT/docs/promo/img/src/keyword_pages.json` (키워드와 '면접'이 같이 나오는 쪽).

## 2. 원고 구조 (견본과 똑같이)

파일: `ROOT/docs/promo/naver-NN-<학과명>-v2.md`

1. `제목: <학과> 면접 질문 6가지와 답변 예시 총정리 (2027 수시 <별칭> 면접 준비법, <대학A>·<대학B>·<대학C> 면접 방식)`
2. `[썸네일 — thumb-<code>.png (대표 이미지로 지정)]`
3. 도입 문단 1개: "가장 많이 떨어지는 답은 …" → 면접관이 보는 것 4가지 → 이 글이 담은 것 → 누가 읽으면 되는지.
4. `■ <학과> 면접, 올해는 어떻게 보나` — 대학 2~4곳 비교. **대학마다 한 문단 + 그 아래 캡처 자리** `[캡처 N — <대학> 2027학년도 수시모집요강 <쪽>쪽: <파일>.png]`. 마지막에 "나란히 놓으면 방향이 보입니다" 정리 문단 + "지원 대학 모집요강에서 다시 확인하세요" 캐비엇.
5. `■ <학과> 면접 질문 6가지와 답변 예시` — 공통 원칙 한 줄 → `▶ 질문 1~6` 각각 `왜 묻나:`(실제 모집요강 평가 항목 이름과 연결) / `답변 구조:` / `답변 예시:`(따옴표, 가상의 학생 경험, 120~200자대) / `주의:`. **질문 2 아래**에 `[이미지 1 — 제미나이 생성: <장면> / "제미나이 프롬프트 1"]`.
6. `■ 답변은 이 4단계로 만드세요` + `[도식 — structure-<code>.png]`
7. `■ <학과> 면접 준비 순서 (2주 계획)` — 1~2일차 … 11~12일차, 전날.
8. `■ <학과> 면접은 언제 보나` — 날짜순, 수능 전/후 구분.
9. `■ <학과> 면접 자주 묻는 것들` — Q/A 5개 (문제 풀이 여부, 학과 차이, 경험 부족, 수능 최저, 복장).
10. `■ 면접 전날 체크리스트` — □ 7개.
11. 마무리 한 문장("…를 보는 자리입니다.") → `※ 이 글의 모집요강 내용은 … 인용했습니다 …` → 사이트 소개 문단 → `→ https://mjgak.com/<경로>/?utm_source=naver_blog&utm_medium=post` → 해시태그 15~17개.
12. `=====` 구분선 아래 작업용 메모: `[이미지 배치 요약 — 총 N장]` 목록, `[제미나이 프롬프트 1 — <장면> (4:3)]` 영문 프롬프트. 프롬프트 끝은 견본과 **똑같은** 스타일 문장(Style: clean flat vector … No text, no letters, no numbers, no logos, no watermark. Aspect ratio 4:3.)으로 끝낸다.

분량: 견본과 비슷하게(공백 포함 9,000~12,000자). 문체: "~입니다/~하세요" 존댓말, 짧은 문장.

## 3. 사실 규칙 (가장 중요)

- "올해는 어떻게 보나"와 "언제 보나", FAQ의 수능 최저·복장 답변에 나오는 **모든 숫자·날짜·비율·배수·인원·면접 시간·평가 항목**은 직접 PDF에서 읽은 텍스트로만 쓴다. pymupdf 로 해당 쪽을 덤프해서 확인한다. 못 찾으면 쓰지 않는다.
- 모집 인원은 그 전형·그 학과 행에서 읽는다. 1단계 발표·면접일은 그 전형의 전형일정 표에서 읽는다(전형마다 다르다).
- 학과가 실기 위주인 경우(체육·디자인·실용음악)에는 **면접이 들어가는 전형**만 고른다. 실기만 있는 전형을 면접 전형처럼 쓰지 않는다.
- 대학이 모집요강에 면접 질문 예시를 공개했으면(숭실·덕성·을지 등) 그대로 인용하고 캡처한다(따옴표).
- PDF 에 없는 대학은 본문에서 사실 단정 금지. 정리 문단의 "참고로"에서도 확인한 것만 쓴다.
- 답변 예시의 학생 경험은 가상이다(본문에 "가상의 예시" 안내 문구가 이미 있다). 실존 인물 이름, 근거 없는 통계 수치는 쓰지 않는다. 시사·산업 내용은 널리 알려진 수준으로만.

## 4. 이미지

자기 jobs 파일을 만든다: `ROOT/docs/promo/img/jobs_b5_<그룹>.py` (아래 템플릿). 파이썬 파일은 **Write 도구로** 만든다(bash heredoc 은 따옴표 때문에 깨진다).

```python
import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from promo_style import HERE, SRC, pdf, make_thumb, make_capture, make_structure
# pdf("광운대학교") -> src/m_광운대학교.pdf. 다른 파일은 str(SRC / "cau.pdf") 처럼.
def jobs_xxx():
    make_thumb(HERE / "thumb-xxx.png", "학과명")
    make_capture(HERE / "kw-2027-xxx-track.png", pdf("광운대학교"), 19, "시작 문구", ("after", "끝 문구"),
                 "광운대학교", "2027학년도 수시모집요강 19쪽", "푸터 요약(60자 이내)", start_pad=10, end_pad=8)
    make_structure(HERE / "structure-xxx.png", ["결론 문장", "경험 문장", "배운 점 문장", "연결 문장"])
```

- make_capture(out, pdf, page(1부터), start, end, univ, doc_label, note, dpi=200, start_pad=14, end_pad=6, lr=28, start_idx=0, end_idx=0). end 는 문구(그 문구 **위**에서 자름) / ("after", 문구)(그 문구 **아래**까지) / y좌표 숫자.
- doc_label 쪽수: 인쇄 쪽수와 PDF 쪽수가 다르면 `"2027학년도 수시모집요강 13쪽(PDF 18쪽)"`. 인쇄 쪽수는 덤프 첫 줄 등에서 확인.
- 푸터 note 는 60자 이내(길면 오른쪽 "면접각 mjgak.com" 과 겹친다).
- **생성한 모든 캡처 PNG 를 Read 도구로 직접 열어 본다.** 위·아래에 잘린 글자 줄, 표가 중간에 끊김, 오른쪽에 다른 칼럼 흔적이 있으면 start_pad/end_pad/lr/end 를 고쳐 다시 만든다. 다른 학과·전형 내용이 많이 섞이면 범위를 좁힌다.
- 썸네일: `make_thumb(out, "학과명")`. 도식: 질문 1 답변 예시를 4문장(결론·경험·배운 점·연결)으로.
- 파일 이름: `<대학약자>-2027-<code>-<내용>.png` (kw=광운, mju=명지, ssu=숭실, khu=경희, ajou=아주, cau=중앙, duksung=덕성, sm=숙명, ewha=이화, kookmin=국민, dongguk=동국, konkuk=건국, sejong=세종, inha=인하, kangnam=강남, baekseok=백석, hoseo=호서, namseoul=남서울, sunmoon=선문, cheongju=청주, eulji=을지, sungshin=성신, yongin=용인, kyonggi=경기, hansei=한세, hufs=외대, uos=시립, syu=삼육, kangwon=강원, cnu=충남, jbnu=전북, jnu=전남, jeju=제주, pusan=부산, kyungnam=경남, nambu=남부). **이미 있는 파일 이름과 겹치지 않게** code 를 학과마다 고유하게.
- 실행: `cd ROOT/docs/promo/img && PYTHONIOENCODING=utf-8 python jobs_b5_<그룹>.py 2>&1 | grep -v "MuPDF error"`.
- PDF 가 더 필요하면 CDN 에서 받는다(회사망이라 verify=False): `https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info2026/<대학명>/<대학명>_2027학년도_수시모집요강.pdf` → `src/m_<대학명>.pdf` 로 저장.

## 5. 붙여넣기 페이지

`cd ROOT/docs/promo/paste && PYTHONIOENCODING=utf-8 python make_paste.py ../naver-NN-<학과명>-v2.md` → `naver-NN-<학과명>-붙여넣기.html`. 출력의 images 수가 원고의 이미지 자리 수와 맞는지 확인.

## 6. 금지

- git commit / push 하지 않는다(취합해서 따로 커밋한다).
- promo_style.py, 다른 그룹의 jobs 파일·원고, site/ 아래 파일은 고치지 않는다.
- localhost:8765 등 다른 서비스, 네이버 사이트에 접속하지 않는다.

## 7. 끝나면 보고할 것

편마다: 원고·붙여넣기·이미지 파일 목록, 쓴 대학과 핵심 사실(인원·배수·비율·면접 시간·면접일·최저), 확인 못 해서 뺀 것, 남은 걱정거리.
