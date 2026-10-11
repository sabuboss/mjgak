# 공통 질문 페이지 보강 지침 (2026-10-11)

저장소 ROOT = `C:\Users\nkkim\my-html-project\mjgak`. 애드센스가 "가치가 별로 없는 콘텐츠"로 거절했다.
공통 질문 48페이지(/q/<slug>/)가 약 1,800자로 얇다. 질문마다 `site/content/rich/common/<slug>.json` 을 만들어
페이지를 3,500자 이상, **다른 사이트에 없는 구체적 내용**으로 키운다.

먼저 읽을 것: `site/content/common.json`(해당 질문의 why/answer/frame/tips/avoid), `site/content/rich/examples.json`의
common[slug](이미 있는 완성 예시 — 중복 금지), `site/templates/question.html`, `docs/SITE-RICH-BRIEF.md` 0번(공통 규칙).

## 파일 형식
```json
{
 "slug": "why-this-major",
 "deep": "면접관이 이 질문으로 실제로 가려내는 것 3~4문장. 평가 항목 이름(전공적합성, 진로역량, 발전가능성, 공동체역량 등)과 연결. 기존 why 를 되풀이하지 말고 한 단계 더 깊게.",
 "bad_good": [
  {"bad": "나쁜 답 예시(따옴표 없이 본문, 60~120자)", "good": "같은 학생이 고친 답(80~160자)", "why": "무엇이 달라졌는지 1~2문장"},
  {"bad": "...", "good": "...", "why": "..."}
 ],
 "followups": [
  {"q": "이 답 뒤에 실제로 이어지기 쉬운 꼬리질문", "tip": "대응 요령 1~2문장"},
  {"q": "...", "tip": "..."},
  {"q": "...", "tip": "..."}
 ],
 "by_major": [
  {"group": "인문", "point": "이 계열 지원자가 이 질문에서 강조할 것 1~2문장, 구체적 소재 예시 포함"},
  {"group": "사회·상경", "point": "..."},
  {"group": "자연", "point": "..."},
  {"group": "공학", "point": "..."},
  {"group": "의약·보건", "point": "..."},
  {"group": "교육", "point": "..."},
  {"group": "예체능", "point": "..."}
 ],
 "univ_examples": [
  {"univ": "숭실대학교", "code": "soongsil", "q": "대학이 공개한 질문 원문", "source": "2027학년도 수시모집요강 62쪽"}
 ],
 "check": ["답하기 전 스스로 확인할 것 3~4개 (예: 60초 안에 끝나는가)"]
}
```

## 규칙
- **univ_examples 는 저장소 안에서 확인되는 것만**: `site/content/rich/univ/*.json` 의 published_questions (대학 공개 질문)에서
  이 질문과 같은 취지인 것을 0~3개 고른다. source 는 그 파일의 tracks[0].source 등에서 학년도·쪽수를 옮기되, 확실치 않으면
  "2027학년도 수시모집요강"까지만 쓴다. code 는 파일 이름. 맞는 것이 없으면 []. 지어내기 절대 금지.
- 시사·사고력 질문(social-issue, ai-impact, debate-topic 등)은 특정 사건·통계·인물 이름을 쓰지 않는다(시간이 지나면 틀림).
- 답변 예시는 가상의 학생, 완성된 문장, 대괄호 빈칸 금지, "~입니다/했습니다" 말투. 실존 인물 이름·근거 없는 수치 금지.
- 48개 질문끼리 bad_good·followups 소재가 겹치지 않게(학과·활동을 다양하게).
- 블라인드 면접 원칙: 답 속에 학교 이름, 부모 직업, 수상 실적 이름을 넣지 않는다.
- 문체: 짧은 문장, 존댓말, 이모지 금지.
- 맡은 slug 파일만 만든다. build.py·templates·기존 json 수정 금지. git commit/push 금지.
- JSON UTF-8, ensure_ascii=False, indent 1. 만든 뒤 json.load 로 검증.

## 끝나면 보고
만든 파일 수, univ_examples 를 넣은 질문과 출처, 걱정거리.
