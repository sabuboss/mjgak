/**
 * 비싼 API 라우트 공통 가드 (web-launch-security A2~A6, E1).
 * 순서: 입력 검증 → 세션 토큰(403) → Turnstile(403) → IP 시간/일 + 전체 일일(429) → 동시성(503) → 실행.
 */
import { z } from "zod";

import { LIMITS, acquire, allow, clientIp, release } from "./ratelimit";
import { verifyToken } from "./token";
import { verifyTurnstile } from "./turnstile";

export const SessionAuth = z.object({
  sid: z.string().regex(/^[a-f0-9-]{16,64}$/),
  token: z.string().min(10).max(200),
  turnstile: z.string().max(4000).optional(),
});

export const NO_STORE = { "Cache-Control": "no-store" } as const;

export function json(body: unknown, status = 200, headers: Record<string, string> = {}) {
  return Response.json(body, { status, headers: { ...NO_STORE, ...headers } });
}

type Scope = keyof Pick<typeof LIMITS, "generate" | "feedback">;

export async function guarded<T>(req: Request, scope: Scope, bodySchema: z.ZodType<T>, run: (body: T, ip: string) => Promise<Response>): Promise<Response> {
  let raw: unknown;
  try {
    raw = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  const auth = SessionAuth.safeParse(raw);
  if (!auth.success) return json({ error: "missing_session" }, 403);
  const body = bodySchema.safeParse(raw);
  if (!body.success) return json({ error: "invalid_input", issues: body.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`) }, 400);
  if (!verifyToken(auth.data.token, "session", auth.data.sid)) return json({ error: "bad_token" }, 403);
  const ip = clientIp(req);
  if (!(await verifyTurnstile(auth.data.turnstile, ip))) return json({ error: "bot_check_failed" }, 403);
  const L = LIMITS[scope];
  const ipHash = ip.split(".").slice(0, 3).join(".") + "." + (ip.split(".")[3] ?? ""); // 로그용은 아니고 키용
  if (!(await allow(`${scope}:h`, ipHash, L.perIpHour, LIMITS.HOUR))) return json({ error: "rate_limited", scope: "hour" }, 429, { "Retry-After": "3600" });
  if (!(await allow(`${scope}:d`, ipHash, L.perIpDay, LIMITS.DAY))) return json({ error: "rate_limited", scope: "day" }, 429, { "Retry-After": "86400" });
  if (!(await allow(`${scope}:all`, "global", L.daily, LIMITS.DAY))) return json({ error: "daily_quota_exhausted" }, 429, { "Retry-After": "3600" });
  if (!acquire(scope, L.concurrent)) return json({ error: "busy" }, 503, { "Retry-After": "5" });
  try {
    return await run(body.data, ip);
  } finally {
    release(scope);
  }
}
