/** API 입출력 스키마 (클라이언트·서버 공용, zod). */
import { z } from "zod";

import { PROFILE_CODES } from "@/db/schema";

export const ApplicantInput = z.object({
  profileCode: z.enum(PROFILE_CODES),
  univCode: z.string().regex(/^[a-z0-9_]{2,20}$/).optional(),
  admissionName: z.string().trim().max(60).optional(),
  unit: z.string().trim().max(80).optional(),
  activities: z.array(z.string().trim().min(2).max(300)).max(5).default([]),
  notes: z.string().trim().max(600).default(""), // 유형별 추가 정보 (자퇴 사유, 거주국·이수과정 등)
});
export type ApplicantInput = z.infer<typeof ApplicantInput>;

export const GeneratedQuestion = z.object({
  question: z.string(),
  basis: z.enum(["actual", "predicted"]),
  source_question_id: z.number().int().nullable(),
  why_asked: z.string(),
  tips: z.string(),
  tags: z.array(z.string()),
});
export type GeneratedQuestion = z.infer<typeof GeneratedQuestion>;

export const GeneratedSet = z.object({ questions: z.array(GeneratedQuestion) });
export type GeneratedSet = z.infer<typeof GeneratedSet>;

export const GenerateResponse = z.object({
  mode: z.enum(["llm", "template"]),
  cached: z.boolean(),
  notice: z.string().optional(),
  questions: z.array(GeneratedQuestion),
});
export type GenerateResponse = z.infer<typeof GenerateResponse>;

export const FeedbackInput = z.object({
  question: z.string().trim().min(2).max(600),
  answer: z.string().trim().min(10).max(3000),
  basis: z.enum(["actual", "predicted"]).default("predicted"),
  whyAsked: z.string().trim().max(400).default(""),
  profileCode: z.enum(PROFILE_CODES),
  univCode: z.string().regex(/^[a-z0-9_]{2,20}$/).optional(),
});
export type FeedbackInput = z.infer<typeof FeedbackInput>;

const Score = z.number().int().min(1).max(5);
export const FeedbackResult = z.object({
  scores: z.object({ structure: Score, evidence: Score, authenticity: Score, length: Score, fit: Score }),
  summary: z.string(),
  improvements: z.array(z.string()),
  example_answer: z.string(),
});
export type FeedbackResult = z.infer<typeof FeedbackResult>;

export const FeedbackResponse = FeedbackResult.extend({
  mode: z.enum(["llm", "rules"]),
  notice: z.string().optional(),
});
export type FeedbackResponse = z.infer<typeof FeedbackResponse>;
