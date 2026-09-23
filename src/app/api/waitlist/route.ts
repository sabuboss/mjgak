import { z } from "zod";

import { db, schema } from "@/db";
import { json } from "@/lib/security/guard";
import { LIMITS, allow, clientIp } from "@/lib/security/ratelimit";

export const runtime = "nodejs";

const Body = z.object({
  email: z.string().trim().toLowerCase().email().max(120),
  profileCode: z.enum(schema.PROFILE_CODES).optional(),
  website: z.string().max(0).optional(), // 허니팟: 봇이 채우면 거절
});

export async function POST(req: Request) {
  let raw: unknown;
  try {
    raw = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  const b = Body.safeParse(raw);
  if (!b.success) return json({ error: "invalid_input" }, 400);
  const ip = clientIp(req);
  if (!(await allow("waitlist:h", ip, 5, LIMITS.HOUR))) return json({ error: "rate_limited" }, 429);
  if (!(await allow("waitlist:all", "global", 2000, LIMITS.DAY))) return json({ error: "rate_limited" }, 429);
  db.insert(schema.waitlist).values({ email: b.data.email, profileCode: b.data.profileCode }).onConflictDoNothing().run();
  return json({ ok: true });
}
