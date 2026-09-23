/**
 * 시드 로더: data/seed/universities.json, data/seed/profiles/*.json, pipeline/out/<univ>.jsonl → DB
 *
 *   npm run db:seed              # 전체
 *   npm run db:seed -- --univ snu  # 특정 대학 문항만
 *
 * 멱등: universities/admission_types/profiles 는 upsert, questions 는 (univ, year, source_url, text) 기준 중복 삽입 안 함.
 * verified 는 이미 사람이 켠 값을 덮어쓰지 않는다.
 */
import fs from "node:fs";
import path from "node:path";
import { and, eq, sql } from "drizzle-orm";
import { z } from "zod";

import { db, schema } from "./index";

const ROOT = process.cwd();
const SEED_DIR = path.join(ROOT, "data", "seed");
const OUT_DIR = path.join(ROOT, "pipeline", "out");

const UniversitySeed = z.object({
  code: z.string(),
  name: z.string(),
  region: z.string(),
  type: z.enum(schema.UNIVERSITY_TYPES),
  admission_url: z.string().url(),
  report_board_url: z.string().url().optional(),
  priority: z.number().int().optional(),
});

const ProfileSeed = z.object({
  code: z.enum(schema.PROFILE_CODES),
  label: z.string(),
  description: z.string().default(""),
  seed_questions: z
    .array(z.object({ id: z.string(), text: z.string(), why_asked: z.string(), tips: z.string(), tags: z.array(z.string()).optional() }))
    .min(10),
  answer_frame: z.object({
    structure: z.array(z.string()).min(3),
    cautions: z.array(z.string()),
    avoid: z.array(z.string()),
    length_hint: z.string(),
  }),
  llm_notes: z.string().default(""),
});

const QuestionRecord = z.object({
  university_code: z.string(),
  admission_name: z.string(),
  category: z.enum(schema.ADMISSION_CATEGORIES),
  unit: z.string().default(""),
  year: z.number().int(),
  kind: z.enum(schema.QUESTION_KINDS),
  text: z.string().min(1),
  presented_material: z.string().default(""),
  intent: z.string().default(""),
  rubric: z.string().default(""),
  model_answer_hint: z.string().default(""),
  source_url: z.string().url(),
  source_page: z.number().int().nullable().optional(),
  verified: z.boolean().default(false),
});

function readJson(p: string) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

export function seedUniversities() {
  const list = z.array(UniversitySeed).parse(readJson(path.join(SEED_DIR, "universities.json")).universities);
  for (const u of list) {
    db.insert(schema.universities)
      .values({
        code: u.code,
        name: u.name,
        region: u.region,
        type: u.type,
        admissionUrl: u.admission_url,
        reportBoardUrl: u.report_board_url,
        priority: u.priority ?? 9,
      })
      .onConflictDoUpdate({
        target: schema.universities.code,
        set: { name: u.name, region: u.region, type: u.type, admissionUrl: u.admission_url, reportBoardUrl: u.report_board_url, priority: u.priority ?? 9 },
      })
      .run();
  }
  return list.length;
}

export function seedProfiles() {
  const dir = path.join(SEED_DIR, "profiles");
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  for (const f of files) {
    const p = ProfileSeed.parse(readJson(path.join(dir, f)));
    db.insert(schema.applicantProfiles)
      .values({ code: p.code, label: p.label, description: p.description, seedQuestions: p.seed_questions, answerFrame: p.answer_frame, llmNotes: p.llm_notes })
      .onConflictDoUpdate({
        target: schema.applicantProfiles.code,
        set: { label: p.label, description: p.description, seedQuestions: p.seed_questions, answerFrame: p.answer_frame, llmNotes: p.llm_notes },
      })
      .run();
  }
  return files.length;
}

function admissionTypeId(universityId: number, name: string, category: (typeof schema.ADMISSION_CATEGORIES)[number]) {
  const found = db
    .select({ id: schema.admissionTypes.id })
    .from(schema.admissionTypes)
    .where(and(eq(schema.admissionTypes.universityId, universityId), eq(schema.admissionTypes.name, name)))
    .get();
  if (found) return found.id;
  return db.insert(schema.admissionTypes).values({ universityId, name, category }).returning({ id: schema.admissionTypes.id }).get().id;
}

export function seedQuestions(univCode?: string) {
  const files = fs.readdirSync(OUT_DIR).filter((f) => f.endsWith(".jsonl") && (!univCode || f === `${univCode}.jsonl`));
  let inserted = 0;
  let skipped = 0;
  let invalid = 0;
  for (const f of files) {
    const lines = fs.readFileSync(path.join(OUT_DIR, f), "utf8").split("\n").filter(Boolean);
    for (const line of lines) {
      const parsed = QuestionRecord.safeParse(JSON.parse(line));
      if (!parsed.success) {
        invalid++;
        continue;
      }
      const r = parsed.data;
      const univ = db.select({ id: schema.universities.id }).from(schema.universities).where(eq(schema.universities.code, r.university_code)).get();
      if (!univ) throw new Error(`universities.json 에 없는 대학: ${r.university_code}`);
      const atId = admissionTypeId(univ.id, r.admission_name, r.category);
      const res = db
        .insert(schema.questions)
        .values({
          universityId: univ.id,
          admissionTypeId: atId,
          unit: r.unit,
          year: r.year,
          kind: r.kind,
          text: r.text,
          presentedMaterial: r.presented_material,
          intent: r.intent,
          rubric: r.rubric,
          modelAnswerHint: r.model_answer_hint,
          sourceUrl: r.source_url,
          sourcePage: r.source_page ?? null,
          verified: r.verified,
        })
        .onConflictDoUpdate({
          target: [schema.questions.universityId, schema.questions.year, schema.questions.unit, schema.questions.sourceUrl, schema.questions.text],
          // 내용 갱신은 허용하되 사람이 켠 verified 는 유지
          set: {
            unit: r.unit,
            presentedMaterial: r.presented_material,
            intent: r.intent,
            rubric: r.rubric,
            modelAnswerHint: r.model_answer_hint,
            sourcePage: r.source_page ?? null,
            admissionTypeId: atId,
            updatedAt: sql`(datetime('now'))`,
          },
        })
        .run();
      if (res.changes > 0) inserted++;
      else skipped++;
    }
  }
  return { files: files.length, inserted, skipped, invalid };
}

if (process.argv[1] && /seed\.(ts|js)$/.test(process.argv[1])) {
  const univArg = process.argv.indexOf("--univ");
  const univ = univArg >= 0 ? process.argv[univArg + 1] : undefined;
  console.log(`universities: ${seedUniversities()}`);
  console.log(`profiles: ${seedProfiles()}`);
  console.log(`questions:`, seedQuestions(univ));
  const counts = db.select({ kind: schema.questions.kind, n: sql<number>`count(*)` }).from(schema.questions).groupBy(schema.questions.kind).all();
  console.log("questions by kind:", counts);
}
