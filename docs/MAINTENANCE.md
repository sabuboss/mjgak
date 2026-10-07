# 면접각 유지보수 달력

사이트(mjgak.com)와 네이버 블로그 글을 해마다 어떻게 갱신하는지 정리한 문서. 작업은 모두 이 저장소의 스크립트로 하고, 발행(네이버 붙여넣기)만 사람이 한다.

## 한눈에 보기

| 시기 | 할 일 | 소요 | 도구 |
|---|---|---|---|
| 매달 1회 | GA4·서치콘솔 유입 확인, 애드센스 상태 확인 | 10분 | 크롬에서 직접 |
| 3월 | 대학 선행학습 영향평가 보고서(전년도 기출) 수집 → 사이트 기출 추가 | 반나절 | pipeline/ |
| 5월 말~6월 | 2028학년도 수시 모집요강 공개 → PDF 내려받기 → 캡처 재생성 → 블로그 글 숫자 갱신 | 1~2일 | 아래 "연간 갱신" |
| 6월 | 사이트 학년도·수능 날짜 갱신, 신설학과 추가, 대학 영상 링크 점검 | 2시간 | build.py, 아래 스크립트 |
| 9월 초 | 가비아 도메인 갱신(만료 2027-09), 수시 원서 접수 시작에 맞춰 블로그 글 재발행 | 30분 | 가비아 |
| 9~12월 | 블로그 글 1일 1편 발행(또는 기존 글 수정), 유입 확인 | 매일 5분 | docs/promo/paste |
| 분기 1회 | 유튜브 임베드 생존 확인(삭제·비공개 영상 교체) | 20분 | 아래 스크립트 |

## 자동 감시 (GitHub Actions, 매달 1일 09:00)

`.github/workflows/monitor.yml` 이 `monitor/check.py` 를 돌려 세 가지를 확인하고, 달라진 게 있으면 저장소에 **이슈**를 연다(이슈 알림 메일은 GitHub 계정 설정의 Notifications → Watching 에 따라 온다. 저장소 Watch 가 켜져 있어야 함).

1. 다음 학년도 수시 모집요강 PDF 가 CDN 에 올라왔는지 — 블로그 글에 쓴 36개 대학(`GUIDE_UNIVS`). 새로 올라온 대학이 생기면 이슈에 목록이 적힌다 → 위 "연간 갱신" 시작 신호.
2. 선행학습 영향평가 보고서(전년도 면접 기출)가 올라왔는지 — 기출 공개 10개 대학(`REPORT_UNIVS`).
3. 사이트의 유튜브 영상 전부(oembed) + 전국 대학 홈페이지 링크. 영상은 새로 죽은 것, 홈페이지는 두 달 연속 실패한 것만 알린다.

상태는 `monitor/state.json` 에 커밋된다(지난달과 비교용). 수동 실행: GitHub → Actions → monitor → Run workflow. 로컬: `MJGAK_INSECURE=1 python monitor/check.py` (회사망).
블로그에 새 대학을 쓰면 `GUIDE_UNIVS` 에 대학명을 추가한다.

## 연간 갱신 (5~6월, 2028학년도 모집요강 나오면)

1. PDF 내려받기 — 블로그 글에 쓴 대학은 `docs/promo/img/promo_style.py`의 `jobs_*` 함수에 모두 적혀 있다.
   ```bash
   # 4년제는 CDN 패턴으로 받는다 (univ_info2027 로 연도만 바꿈)
   # https://cdn013.negagea.net/dgsmidc/omr/seoul/web/univ_info2027/<대학명>/<대학명>_2028학년도_수시모집요강.pdf
   # 교대·일부 대학은 입학처 게시판에서 직접 (memory 메모 참고)
   ```
   받은 파일은 `docs/promo/img/src/m_<대학명>.pdf` 로 저장(기존 파일 덮어쓰기). src/ 는 gitignore라 저장소엔 안 올라간다.
2. 캡처 재생성 — `promo_style.py` 안의 `"2027학년도 모집요강"` 칩 문구와 각 `jobs_*`의 캡처 설명(`"… 2027학년도 수시모집요강 N쪽"`)을 2028로 바꾼 뒤:
   ```bash
   cd docs/promo/img && ../../../pipeline/.venv/Scripts/python.exe -c "import promo_style as p; p.jobs_nursing(); p.jobs_med(); ..."
   ```
   앵커 문구(예: `"4) 면접평가 방법"`)를 못 찾으면 에러가 난다 → 그 페이지를 `pymupdf`로 열어 새 문구/쪽수로 고친다. 보통 전체의 20~30%가 바뀐다.
3. 캡처를 눈으로 확인하고(잘림·겹침), 글의 숫자(배수·비율·날짜·최저)를 캡처와 맞춰 고친다. 글 파일은 `docs/promo/naver-NN-학과-v2.md`.
4. 붙여넣기 페이지 재생성:
   ```bash
   cd docs/promo/paste && ../../../pipeline/.venv/Scripts/python.exe make_paste.py ../naver-NN-학과-v2.md
   ```
5. 네이버 블로그에서 **기존 글을 수정**(제목 2027→2028, 본문 숫자·이미지 교체). 새 글로 올리면 누적 조회가 끊긴다.

## 사이트 연간 갱신 (6월)

- `site/pages/schedule.md` — 수능 날짜, 시기별 일정
- `site/content/universities.json` — `report_year`, 보고서 링크
- `site/content/new_departments.json` — 신설학과 추가/정리(개설 대학·인원은 보도자료 기준)
- `site/site.json` — 필요 시 `publish_date`
- 빌드: `python site/build.py` → 깨진 링크 0 확인 → 커밋·푸시하면 GitHub Actions가 배포

## 유튜브 영상 점검 (분기)

```bash
# 모든 videos 항목에 대해 oembed 200 + embed 페이지에 UNPLAYABLE 없음 확인
cd site && ../pipeline/.venv/Scripts/python.exe - <<'EOF'
import json, glob, requests, urllib3; urllib3.disable_warnings()
H={"User-Agent":"Mozilla/5.0"}
for f in glob.glob("content/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    items=d.get("departments") or d.get("universities") or []
    for it in items:
        for v in it.get("videos",[]):
            r=requests.get("https://www.youtube.com/oembed",params={"url":"https://www.youtube.com/watch?v="+v["id"],"format":"json"},verify=False,timeout=20,headers=H)
            if r.status_code!=200: print("DEAD",f,it.get("slug") or it.get("code"),v["id"],v["title"][:30])
EOF
```
죽은 영상은 같은 대학 공식 채널에서 다시 찾아 교체(`docs/promo/img/src/*_video_candidates.txt` 참고).

## 하지 않는 것

- 네이버 블로그 자동 발행 프로그램 — 약관 위반, 계정 정지 위험. 붙여넣기 페이지로 수동 발행한다.
- 대학 홈페이지 사진 사용 — 저작권·애드센스 위험. 모집요강 캡처(출처 표기), 제미나이 생성 이미지, 대학 공식 유튜브 임베드만 쓴다.

## 비용

도메인 1년 약 2만 원(가비아) 외에 없음. GitHub Pages·GA4·검색 색인 모두 무료.
