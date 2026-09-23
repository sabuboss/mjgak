/**
 * Phase 1 임시 관리자 인증: .env 의 ADMIN_TOKEN 과 같은 값을 가진 httpOnly 쿠키가 있으면 관리자.
 * 정식 인증(매직링크)은 사용자 인증과 함께 나중에 교체한다.
 */
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const ADMIN_COOKIE = "mjgak_admin";

export function adminToken(): string | undefined {
  const t = process.env.ADMIN_TOKEN;
  if (!t || t === "change-me") return undefined; // 기본값 그대로면 관리자 기능 비활성
  return t;
}

export async function isAdmin(): Promise<boolean> {
  const t = adminToken();
  if (!t) return false;
  const c = await cookies();
  return c.get(ADMIN_COOKIE)?.value === t;
}

export async function requireAdmin(next = "/admin/review") {
  if (!(await isAdmin())) redirect(`/admin/login?next=${encodeURIComponent(next)}`);
}
