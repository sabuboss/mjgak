import { createHash, createHmac, timingSafeEqual } from "node:crypto";

/**
 * 요청 토큰: 페이지(서버 컴포넌트)가 발급하고 API 가 검증한다.
 * 토큰은 scope(report/card)와 subject(정규화된 입력)에 묶이므로, 페이지를 거치지 않고
 * API 만 직접 두드리며 파라미터를 열거하는 공격을 막는다. 페이지 자체는 Vercel 봇 차단이 지킨다.
 *
 * 비밀키: APP_SECRET 환경변수. 없으면 배포 식별자로 파생(경고), 로컬은 고정 개발용 키.
 */
function secret(): string {
  if (process.env.APP_SECRET) return process.env.APP_SECRET;
  const parts = [process.env.VERCEL_PROJECT_ID, process.env.VERCEL_GIT_COMMIT_SHA, process.env.VERCEL_URL].filter(Boolean);
  if (parts.length) {
    if (!warned) {
      console.warn("[security] APP_SECRET 미설정: 배포 식별자로 파생한 키를 사용합니다. Vercel 환경변수에 APP_SECRET 을 넣어 주세요.");
      warned = true;
    }
    return createHash("sha256").update(parts.join("|")).digest("hex");
  }
  return "dev-insecure-secret-change-me";
}
let warned = false;

function sign(payload: string): string {
  return createHmac("sha256", secret()).update(payload).digest("base64url");
}

export const DEFAULT_TOKEN_TTL_SEC = 30 * 60;

/** scope: "report" | "card" 등, subject: 정규화된 파라미터 문자열 */
export function mintToken(scope: string, subject: string, ttlSec = DEFAULT_TOKEN_TTL_SEC): string {
  const exp = Math.floor(Date.now() / 1000) + ttlSec;
  return `${exp}.${sign(`${scope}|${subject}|${exp}`)}`;
}

export function verifyToken(token: unknown, scope: string, subject: string): boolean {
  if (typeof token !== "string") return false;
  const dot = token.indexOf(".");
  if (dot <= 0) return false;
  const exp = Number(token.slice(0, dot));
  const sig = token.slice(dot + 1);
  if (!Number.isFinite(exp) || exp < Math.floor(Date.now() / 1000)) return false;
  const expected = sign(`${scope}|${subject}|${exp}`);
  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}
