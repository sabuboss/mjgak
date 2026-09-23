import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

/**
 * 요청 제한.
 * - Upstash Redis 환경변수(UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN)가 있으면 인스턴스 간 공유되는 슬라이딩 윈도우.
 * - 없으면 인메모리(인스턴스별) 폴백. 서버리스에서는 우회될 수 있으므로 운영에서는 Upstash 를 권장한다.
 */

const redis =
  process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN
    ? new Redis({ url: process.env.UPSTASH_REDIS_REST_URL, token: process.env.UPSTASH_REDIS_REST_TOKEN })
    : null;

export const durableLimits = redis !== null;
export function redisClient(): Redis | null {
  return redis;
}

const limiters = new Map<string, Ratelimit>();
function limiter(limit: number, windowSec: number): Ratelimit {
  const k = `${limit}:${windowSec}`;
  let l = limiters.get(k);
  if (!l) {
    l = new Ratelimit({
      redis: redis!,
      limiter: Ratelimit.slidingWindow(limit, `${windowSec} s`),
      prefix: "rl",
      analytics: false,
    });
    limiters.set(k, l);
  }
  return l;
}

// ── 인메모리 폴백 ─────────────────────────────────────────
const buckets = new Map<string, number[]>();
function memoryAllow(key: string, limit: number, windowSec: number): boolean {
  const now = Date.now();
  const windowMs = windowSec * 1000;
  const hits = (buckets.get(key) ?? []).filter((t) => now - t < windowMs);
  if (hits.length >= limit) {
    buckets.set(key, hits);
    return false;
  }
  hits.push(now);
  buckets.set(key, hits);
  if (buckets.size > 5000) {
    for (const [k, v] of buckets) {
      const alive = v.filter((t) => now - t < windowMs);
      if (alive.length === 0) buckets.delete(k);
      else buckets.set(k, alive);
    }
  }
  return true;
}

/** 허용이면 true. id 는 IP 등 주체, scope 는 용도 */
export async function allow(scope: string, id: string, limit: number, windowSec: number): Promise<boolean> {
  const key = `${scope}:${id}`;
  if (redis) {
    try {
      const r = await limiter(limit, windowSec).limit(key);
      return r.success;
    } catch {
      // Redis 장애 시 폴백 (fail-open 보다 메모리 제한이 낫다)
      return memoryAllow(key, limit, windowSec);
    }
  }
  return memoryAllow(key, limit, windowSec);
}

// ── 동시 실행 상한 (인스턴스별) ──────────────────────────
const running = new Map<string, number>();
export function acquire(scope: string, max: number): boolean {
  const n = running.get(scope) ?? 0;
  if (n >= max) return false;
  running.set(scope, n + 1);
  return true;
}
export function release(scope: string) {
  running.set(scope, Math.max(0, (running.get(scope) ?? 0) - 1));
}

export function clientIp(req: Request): string {
  const xf = req.headers.get("x-forwarded-for");
  if (xf) return xf.split(",")[0].trim();
  return req.headers.get("x-real-ip") ?? "unknown";
}

const n = (v: string | undefined, d: number) => (v && Number.isFinite(Number(v)) ? Number(v) : d);

export const LIMITS = {
  // 예상질문 생성: 1회 수십 초·수천 토큰. 같은 입력은 캐시.
  generate: {
    perIpHour: n(process.env.LIMIT_GENERATE_PER_IP_HOUR, 5),
    perIpDay: n(process.env.LIMIT_GENERATE_PER_IP_DAY, 15),
    daily: n(process.env.LIMIT_GENERATE_DAILY, 300),
    concurrent: n(process.env.LIMIT_GENERATE_CONCURRENT, 3),
  },
  // 답변 피드백: 짧지만 횟수가 많다.
  feedback: {
    perIpHour: n(process.env.LIMIT_FEEDBACK_PER_IP_HOUR, 20),
    perIpDay: n(process.env.LIMIT_FEEDBACK_PER_IP_DAY, 60),
    daily: n(process.env.LIMIT_FEEDBACK_DAILY, 1500),
    concurrent: n(process.env.LIMIT_FEEDBACK_CONCURRENT, 5),
  },
  HOUR: 3600,
  DAY: 86400,
} as const;
