# 유입 리포트 API 준비 (한 번만, 약 5분, 무료)

브라우저로 GA4·서치콘솔 화면을 여는 대신, 읽기 전용 "로봇 계정"(서비스 계정)이 숫자를 API 로 읽는다.
로그인이 풀려도 리포트가 멈추지 않는다. 두 API 모두 무료이고 결제가 생기지 않는다.

## 1. 로봇 계정과 열쇠 만들기 (Google Cloud, 프로젝트 mjgak-images)
1. API 두 개 켜기 — 각 링크에서 **사용** 버튼
   - https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com?project=mjgak-images
   - https://console.cloud.google.com/apis/library/searchconsole.googleapis.com?project=mjgak-images
2. 서비스 계정 만들기: https://console.cloud.google.com/iam-admin/serviceaccounts/create?project=mjgak-images
   - 이름 `mjgak-reader` → **만들고 계속하기** → 역할은 **비워 두고** 완료
3. 만든 계정 클릭 → **키** 탭 → 키 추가 → 새 키 만들기 → **JSON** → 내려받기
4. 내려받은 파일을 `C:\Users\nkkim\my-html-project\mjgak\docs\promo\.secrets\ga-reader.json` 으로 옮기기
   (이 폴더는 git 에 올라가지 않는다. 파일은 남에게 보내지 않는다.)
5. 계정 이메일 복사: `mjgak-reader@mjgak-images.iam.gserviceaccount.com`

## 2. 읽기 권한 주기
- GA4: https://analytics.google.com/analytics/web/#/a283647920p556489763/admin/suiteusermanagement/property
  → 오른쪽 위 **+** → 사용자 추가 → 위 이메일 → 역할 **뷰어** → 추가 (알림 메일 체크 해제)
- 서치콘솔: https://search.google.com/search-console/users?resource_id=https%3A%2F%2Fmjgak.com%2F
  → **사용자 추가** → 위 이메일 → 권한 **제한됨** → 추가

## 3. 확인
```
python docs/promo/analytics/report.py --check
```
"GA4: … 세션 OK", "서치콘솔: … 클릭 OK" 가 나오면 끝. 이후 리포트는 `python docs/promo/analytics/report.py`.
