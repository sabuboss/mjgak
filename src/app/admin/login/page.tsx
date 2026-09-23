import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { ADMIN_COOKIE, adminToken } from "@/lib/admin-auth";

async function login(formData: FormData) {
  "use server";
  const token = adminToken();
  const input = String(formData.get("token") ?? "");
  const next = String(formData.get("next") ?? "/admin/review");
  if (!token || input !== token) redirect(`/admin/login?error=1&next=${encodeURIComponent(next)}`);
  const c = await cookies();
  c.set(ADMIN_COOKIE, token, { httpOnly: true, sameSite: "lax", path: "/admin", maxAge: 60 * 60 * 12 });
  redirect(next.startsWith("/admin") ? next : "/admin/review");
}

export default async function AdminLoginPage({ searchParams }: { searchParams: Promise<{ error?: string; next?: string }> }) {
  const { error, next } = await searchParams;
  const enabled = Boolean(adminToken());
  return (
    <main className="mx-auto max-w-sm px-4 py-16">
      <h1 className="text-xl font-semibold">관리자 로그인</h1>
      {!enabled && (
        <p className="mt-4 rounded bg-amber-50 p-3 text-sm text-amber-900">
          <code>ADMIN_TOKEN</code> 환경변수가 설정되지 않아 관리자 기능이 꺼져 있습니다. <code>.env.local</code> 에 값을 넣고 서버를 재시작하세요.
        </p>
      )}
      {error && <p className="mt-4 text-sm text-red-600">토큰이 일치하지 않습니다.</p>}
      <form action={login} className="mt-6 flex flex-col gap-3">
        <input type="hidden" name="next" value={next ?? "/admin/review"} />
        <input name="token" type="password" placeholder="ADMIN_TOKEN" className="rounded border px-3 py-2" autoFocus />
        <button type="submit" disabled={!enabled} className="rounded bg-black px-3 py-2 text-white disabled:opacity-40">
          들어가기
        </button>
      </form>
    </main>
  );
}
