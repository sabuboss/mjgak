/**
 * DB 스키마 (SPEC 4장). 개발은 SQLite, 배포 시 Postgres 전환을 고려해 타입은 단순하게 유지한다.
 *
 * 원칙:
 *  - questions.source_url / year 는 NOT NULL (원문 재배포 대신 출처 링크로 연결)
 *  - kind: actual(실제 기출) | example(대학 예시) | predicted(LLM 예상) | none(문항 미공개, 평가영역만)
 *  - 생기부 원문은 어디에도 저장하지 않는다. user_answers 는 옵트인 저장에만 쓴다.
 */
import { sql } from "drizzle-orm";
import { index, integer, sqliteTable, text, uniqueIndex } from "drizzle-orm/sqlite-core";

export const UNIVERSITY_TYPES = ["general", "junior", "teachers", "military", "police", "special"] as const;
export const ADMISSION_CATEGORIES = ["student_record", "essay_based", "personality", "major", "english", "mmi"] as const;
export const QUESTION_KINDS = ["actual", "example", "predicted", "none"] as const;
export const PROFILE_CODES = ["GENERAL", "VOCATIONAL", "GED", "REPEAT", "OVERSEAS_3", "OVERSEAS_12", "ALTERNATIVE"] as const;

export type UniversityType = (typeof UNIVERSITY_TYPES)[number];
export type AdmissionCategory = (typeof ADMISSION_CATEGORIES)[number];
export type QuestionKind = (typeof QUESTION_KINDS)[number];
export type ProfileCode = (typeof PROFILE_CODES)[number];

export const universities = sqliteTable("universities", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  code: text("code").notNull().unique(), // snu, yonsei …
  name: text("name").notNull(),
  region: text("region").notNull(),
  type: text("type", { enum: UNIVERSITY_TYPES }).notNull(),
  admissionUrl: text("admission_url").notNull(),
  reportBoardUrl: text("report_board_url"),
  priority: integer("priority").notNull().default(9),
});

export const admissionTypes = sqliteTable(
  "admission_types",
  {
    id: integer("id").primaryKey({ autoIncrement: true }),
    universityId: integer("university_id").notNull().references(() => universities.id, { onDelete: "cascade" }),
    name: text("name").notNull(), // 수시모집 일반전형 …
    category: text("category", { enum: ADMISSION_CATEGORIES }).notNull(),
    interviewWeight: text("interview_weight"), // "50%" 등 자유 텍스트 (대학마다 표기 다름)
    notes: text("notes"),
  },
  (t) => [uniqueIndex("admission_types_univ_name_idx").on(t.universityId, t.name)],
);

export const questions = sqliteTable(
  "questions",
  {
    id: integer("id").primaryKey({ autoIncrement: true }),
    universityId: integer("university_id").notNull().references(() => universities.id, { onDelete: "cascade" }),
    admissionTypeId: integer("admission_type_id").references(() => admissionTypes.id, { onDelete: "set null" }),
    unit: text("unit").notNull().default(""), // 모집단위/계열
    year: integer("year").notNull(),
    kind: text("kind", { enum: QUESTION_KINDS }).notNull(),
    text: text("text").notNull(),
    presentedMaterial: text("presented_material").notNull().default(""),
    intent: text("intent").notNull().default(""),
    rubric: text("rubric").notNull().default(""),
    modelAnswerHint: text("model_answer_hint").notNull().default(""),
    sourceUrl: text("source_url").notNull(),
    sourcePage: integer("source_page"),
    verified: integer("verified", { mode: "boolean" }).notNull().default(false),
    createdAt: text("created_at").notNull().default(sql`(datetime('now'))`),
    updatedAt: text("updated_at").notNull().default(sql`(datetime('now'))`),
  },
  (t) => [
    index("questions_univ_year_idx").on(t.universityId, t.year),
    index("questions_kind_idx").on(t.kind),
    // 같은 출처·연도·모집단위·문항 텍스트는 한 번만 (재시드 시 중복 방지). 같은 문항이 다른 모집단위에 출제되면 별도 행.
    uniqueIndex("questions_dedupe_idx").on(t.universityId, t.year, t.unit, t.sourceUrl, t.text),
  ],
);

export const applicantProfiles = sqliteTable("applicant_profiles", {
  code: text("code", { enum: PROFILE_CODES }).primaryKey(),
  label: text("label").notNull(),
  description: text("description").notNull().default(""),
  seedQuestions: text("seed_questions", { mode: "json" }).notNull().$type<SeedQuestion[]>(),
  answerFrame: text("answer_frame", { mode: "json" }).notNull().$type<AnswerFrame>(),
  llmNotes: text("llm_notes").notNull().default(""),
});

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull().unique(),
  birthYear: integer("birth_year").notNull(),
  guardianConsent: integer("guardian_consent", { mode: "boolean" }).notNull().default(false),
  profileCode: text("profile_code", { enum: PROFILE_CODES }).references(() => applicantProfiles.code),
  targetUnivId: integer("target_univ_id").references(() => universities.id, { onDelete: "set null" }),
  targetAdmissionId: integer("target_admission_id").references(() => admissionTypes.id, { onDelete: "set null" }),
  targetUnit: text("target_unit"),
  createdAt: text("created_at").notNull().default(sql`(datetime('now'))`),
});

/** 옵트인 저장 시에만 사용. 기본은 브라우저 IndexedDB. */
export const userAnswers = sqliteTable(
  "user_answers",
  {
    id: integer("id").primaryKey({ autoIncrement: true }),
    userId: integer("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
    questionId: integer("question_id").references(() => questions.id, { onDelete: "set null" }),
    questionText: text("question_text").notNull(),
    answerText: text("answer_text").notNull(),
    feedback: text("feedback", { mode: "json" }).$type<unknown>(),
    createdAt: text("created_at").notNull().default(sql`(datetime('now'))`),
  },
  (t) => [index("user_answers_user_idx").on(t.userId)],
);

/** 대기자 이메일 (Phase 1 랜딩). */
export const waitlist = sqliteTable("waitlist", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull().unique(),
  profileCode: text("profile_code"),
  createdAt: text("created_at").notNull().default(sql`(datetime('now'))`),
});

// ---- JSON 컬럼 타입 ----
export type SeedQuestion = {
  id: string;
  text: string;
  why_asked: string;
  tips: string;
  tags?: string[];
};

export type AnswerFrame = {
  structure: string[]; // 답변 구조 (두괄식 → 근거 → 경험 → 연결)
  cautions: string[]; // 이 유형이 특히 조심할 점
  avoid: string[]; // 하지 말아야 할 표현/패턴
  length_hint: string; // 권장 길이
};

export type University = typeof universities.$inferSelect;
export type AdmissionType = typeof admissionTypes.$inferSelect;
export type Question = typeof questions.$inferSelect;
export type ApplicantProfile = typeof applicantProfiles.$inferSelect;
