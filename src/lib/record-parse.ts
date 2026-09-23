/**
 * 생기부 텍스트 → 활동 후보 문장 (순수 함수, 브라우저·테스트 공용).
 * 원문은 호출자의 메모리에만 있고 여기서는 저장·전송하지 않는다.
 */
export type Candidate = { text: string; section: string };

const SECTION_KEYS: [RegExp, string][] = [
  [/세부능력\s*및\s*특기사항|세특/, "세특"],
  [/자율활동/, "자율"],
  [/동아리/, "동아리"],
  [/진로활동/, "진로"],
  [/봉사활동/, "봉사"],
  [/독서활동/, "독서"],
  [/행동특성\s*및\s*종합의견/, "행특"],
];
const ACTIVITY_HINT = /(탐구|프로젝트|발표|실험|조사|참여|주도|기획|제작|분석|작성|토론|대회|캠페인|봉사|독서|읽고|활동|수행|설계|개발|연구)/;
const NOISE = /(주민등록|생년월일|성별|보호자|주소|전화|담임|출결|결석|지각|조퇴|석차|등급|원점수|평균|표준편차|수강자수)/;

export function candidatesFromLines(lines: string[], limit = 40): Candidate[] {
  const out: Candidate[] = [];
  const seen = new Set<string>();
  let section = "기타";
  // PDF 줄은 문장 중간에서 끊기므로 한 덩어리로 붙인 뒤 문장 단위로 다시 나눈다
  const joined = lines.join(" ").replace(/\s+/g, " ");
  const sentences = joined.split(/(?<=[.。])\s+|(?<=[함음됨임]\.)\s*/);
  for (const raw of sentences) {
    const s = raw.trim();
    for (const [re, name] of SECTION_KEYS) if (re.test(s.slice(0, 40))) section = name;
    if (s.length < 20 || s.length > 220) continue;
    if (NOISE.test(s)) continue;
    if (!ACTIVITY_HINT.test(s)) continue;
    const key = s.slice(0, 40);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ text: s, section });
    if (out.length >= limit) break;
  }
  return out;
}
