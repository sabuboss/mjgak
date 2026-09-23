/** 문항 조회 (서버 전용). /univ/[id], /admin/review, 예상질문 생성에서 공용. */
import { and, desc, eq, sql, type SQL } from "drizzle-orm";

import { db, schema } from "@/db";
import type { QuestionKind } from "@/db/schema";

export type QuestionFilter = {
  univ?: string; // code
  year?: number;
  kind?: QuestionKind;
  category?: (typeof schema.ADMISSION_CATEGORIES)[number];
  verified?: boolean;
  q?: string; // text LIKE
  page?: number;
  pageSize?: number;
};

export function listQuestions(f: QuestionFilter) {
  const page = Math.max(1, f.page ?? 1);
  const pageSize = Math.min(200, f.pageSize ?? 50);
  const where: SQL[] = [];
  if (f.univ) where.push(eq(schema.universities.code, f.univ));
  if (f.year) where.push(eq(schema.questions.year, f.year));
  if (f.kind) where.push(eq(schema.questions.kind, f.kind));
  if (f.category) where.push(eq(schema.admissionTypes.category, f.category));
  if (f.verified !== undefined) where.push(eq(schema.questions.verified, f.verified));
  if (f.q) where.push(sql`${schema.questions.text} LIKE ${"%" + f.q + "%"}`);
  const cond = where.length ? and(...where) : undefined;

  const base = db
    .select({
      id: schema.questions.id,
      year: schema.questions.year,
      kind: schema.questions.kind,
      unit: schema.questions.unit,
      text: schema.questions.text,
      verified: schema.questions.verified,
      sourceUrl: schema.questions.sourceUrl,
      sourcePage: schema.questions.sourcePage,
      univCode: schema.universities.code,
      univName: schema.universities.name,
      admissionName: schema.admissionTypes.name,
      category: schema.admissionTypes.category,
    })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .leftJoin(schema.admissionTypes, eq(schema.questions.admissionTypeId, schema.admissionTypes.id));

  const rows = base
    .where(cond)
    .orderBy(desc(schema.questions.year), schema.universities.code, schema.questions.id)
    .limit(pageSize)
    .offset((page - 1) * pageSize)
    .all();

  const [{ n }] = db
    .select({ n: sql<number>`count(*)` })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .leftJoin(schema.admissionTypes, eq(schema.questions.admissionTypeId, schema.admissionTypes.id))
    .where(cond)
    .all();

  return { rows, total: n, page, pageSize };
}

export function getQuestion(id: number) {
  return db
    .select({
      q: schema.questions,
      univCode: schema.universities.code,
      univName: schema.universities.name,
      admissionName: schema.admissionTypes.name,
      category: schema.admissionTypes.category,
    })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .leftJoin(schema.admissionTypes, eq(schema.questions.admissionTypeId, schema.admissionTypes.id))
    .where(eq(schema.questions.id, id))
    .get();
}

export function listUniversities() {
  return db.select().from(schema.universities).orderBy(schema.universities.priority, schema.universities.name).all();
}

export function reviewStats() {
  return db
    .select({
      univCode: schema.universities.code,
      univName: schema.universities.name,
      total: sql<number>`count(*)`,
      verified: sql<number>`sum(case when ${schema.questions.verified} then 1 else 0 end)`,
    })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .groupBy(schema.universities.code, schema.universities.name)
    .orderBy(schema.universities.code)
    .all();
}

// ---- 공개 대학 페이지용 ----
export function getUniversityByCode(code: string) {
  return db.select().from(schema.universities).where(eq(schema.universities.code, code)).get();
}

export function universitySummaries() {
  return db
    .select({
      code: schema.universities.code,
      name: schema.universities.name,
      region: schema.universities.region,
      type: schema.universities.type,
      priority: schema.universities.priority,
      admissionUrl: schema.universities.admissionUrl,
      total: sql<number>`count(${schema.questions.id})`,
      actual: sql<number>`sum(case when ${schema.questions.kind} = 'actual' then 1 else 0 end)`,
      minYear: sql<number | null>`min(${schema.questions.year})`,
      maxYear: sql<number | null>`max(${schema.questions.year})`,
    })
    .from(schema.universities)
    .leftJoin(schema.questions, eq(schema.questions.universityId, schema.universities.id))
    .groupBy(schema.universities.id)
    .orderBy(sql`count(${schema.questions.id}) desc`, schema.universities.priority, schema.universities.name)
    .all();
}

export function questionsForUniversity(code: string, year?: number) {
  const where: SQL[] = [eq(schema.universities.code, code)];
  if (year) where.push(eq(schema.questions.year, year));
  return db
    .select({
      id: schema.questions.id,
      year: schema.questions.year,
      kind: schema.questions.kind,
      unit: schema.questions.unit,
      text: schema.questions.text,
      presentedMaterial: schema.questions.presentedMaterial,
      intent: schema.questions.intent,
      rubric: schema.questions.rubric,
      modelAnswerHint: schema.questions.modelAnswerHint,
      verified: schema.questions.verified,
      sourceUrl: schema.questions.sourceUrl,
      sourcePage: schema.questions.sourcePage,
      admissionName: schema.admissionTypes.name,
      category: schema.admissionTypes.category,
    })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .leftJoin(schema.admissionTypes, eq(schema.questions.admissionTypeId, schema.admissionTypes.id))
    .where(and(...where))
    .orderBy(desc(schema.questions.year), schema.admissionTypes.name, schema.questions.id)
    .all();
}

export function yearsForUniversity(code: string) {
  return db
    .select({ year: schema.questions.year, n: sql<number>`count(*)` })
    .from(schema.questions)
    .innerJoin(schema.universities, eq(schema.questions.universityId, schema.universities.id))
    .where(eq(schema.universities.code, code))
    .groupBy(schema.questions.year)
    .orderBy(desc(schema.questions.year))
    .all();
}
