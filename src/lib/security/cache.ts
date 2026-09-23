import { redisClient } from "./ratelimit";

/**
 * 생성 결과 캐시. Upstash Redis 가 있으면 인스턴스 간 공유 + 30일 보존, 없으면 인메모리.
 * 같은 입력에는 같은 결과를 돌려주어 재생성 비용과 "매번 다른 해석" 불만을 함께 줄인다.
 */
const memory = new Map<string, unknown>();
const TTL_SEC = 30 * 24 * 3600;

export async function cacheGet<T>(key: string): Promise<T | null> {
  const redis = redisClient();
  if (redis) {
    try {
      const v = await redis.get<T>(key);
      if (v !== null && v !== undefined) return v;
    } catch {
      /* 폴백 */
    }
  }
  return (memory.get(key) as T | undefined) ?? null;
}

export async function cacheSet<T>(key: string, value: T): Promise<void> {
  memory.set(key, value);
  const redis = redisClient();
  if (redis) {
    try {
      await redis.set(key, value, { ex: TTL_SEC });
    } catch {
      /* 무시 */
    }
  }
}
