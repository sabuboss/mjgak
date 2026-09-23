"use server";

import { eq, sql } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

import { db, schema } from "@/db";
import { isAdmin } from "@/lib/admin-auth";

async function guard() {
  if (!(await isAdmin())) throw new Error("관리자 권한이 없습니다.");
}

export async function toggleVerified(formData: FormData) {
  await guard();
  const id = Number(formData.get("id"));
  const value = formData.get("value") === "1";
  db.update(schema.questions)
    .set({ verified: value, updatedAt: sql`(datetime('now'))` })
    .where(eq(schema.questions.id, id))
    .run();
  revalidatePath("/admin/review");
  revalidatePath(`/admin/review/${id}`);
}

const UpdateSchema = z.object({
  id: z.coerce.number().int(),
  kind: z.enum(schema.QUESTION_KINDS),
  unit: z.string().max(500),
  year: z.coerce.number().int().min(2015).max(2035),
  text: z.string().min(1).max(4000),
  presentedMaterial: z.string().max(6000),
  intent: z.string().max(3000),
  rubric: z.string().max(3000),
  modelAnswerHint: z.string().max(4000),
  sourceUrl: z.string().url(),
  sourcePage: z.coerce.number().int().optional().or(z.literal("").transform(() => undefined)),
  verified: z.literal("on").optional(),
});

export async function updateQuestion(formData: FormData) {
  await guard();
  const parsed = UpdateSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    redirect(`/admin/review/${formData.get("id")}?error=${encodeURIComponent(parsed.error.issues.map((i) => i.path.join(".") + ": " + i.message).join("; "))}`);
  }
  const d = parsed.data;
  db.update(schema.questions)
    .set({
      kind: d.kind,
      unit: d.unit,
      year: d.year,
      text: d.text,
      presentedMaterial: d.presentedMaterial,
      intent: d.intent,
      rubric: d.rubric,
      modelAnswerHint: d.modelAnswerHint,
      sourceUrl: d.sourceUrl,
      sourcePage: d.sourcePage ?? null,
      verified: d.verified === "on",
      updatedAt: sql`(datetime('now'))`,
    })
    .where(eq(schema.questions.id, d.id))
    .run();
  revalidatePath("/admin/review");
  redirect(`/admin/review/${d.id}?saved=1`);
}

export async function deleteQuestion(formData: FormData) {
  await guard();
  const id = Number(formData.get("id"));
  db.delete(schema.questions).where(eq(schema.questions.id, id)).run();
  revalidatePath("/admin/review");
  redirect("/admin/review?deleted=1");
}
