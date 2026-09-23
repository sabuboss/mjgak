"use client";
/**
 * 브라우저 로컬 저장소 (IndexedDB, idb). 프로필·예상질문·답변·피드백은 기본적으로 여기만 저장한다 (SPEC 원칙 1).
 * 서버 저장은 옵트인 기능으로 나중에 추가. "모든 데이터 삭제" 는 clearAll().
 */
import { openDB, type IDBPDatabase } from "idb";

import type { ApplicantInput, FeedbackResponse, GeneratedQuestion } from "./llm/schemas";

export type StoredProfile = ApplicantInput & {
  birthYear: number;
  guardianConsent: boolean;
  univName?: string;
  createdAt: string;
};

export type StoredQuestionSet = {
  mode: "llm" | "template";
  notice?: string;
  questions: GeneratedQuestion[];
  createdAt: string;
};

export type StoredAnswer = {
  questionIndex: number;
  question: string;
  answer: string;
  feedback: FeedbackResponse | null;
  createdAt: string;
};

const DB = "mjgak";
let _db: Promise<IDBPDatabase> | null = null;

function db() {
  if (!_db) {
    _db = openDB(DB, 1, {
      upgrade(d) {
        d.createObjectStore("kv");
        const a = d.createObjectStore("answers", { keyPath: "id", autoIncrement: true });
        a.createIndex("byQuestion", "questionIndex");
      },
    });
  }
  return _db;
}

export async function getProfile(): Promise<StoredProfile | undefined> {
  return (await db()).get("kv", "profile");
}
export async function setProfile(p: StoredProfile) {
  await (await db()).put("kv", p, "profile");
}
export async function getQuestionSet(): Promise<StoredQuestionSet | undefined> {
  return (await db()).get("kv", "questionSet");
}
export async function setQuestionSet(s: StoredQuestionSet) {
  await (await db()).put("kv", s, "questionSet");
}
export async function listAnswers(): Promise<(StoredAnswer & { id: number })[]> {
  return (await db()).getAll("answers");
}
export async function addAnswer(a: StoredAnswer) {
  await (await db()).add("answers", a);
}
export async function clearAll() {
  const d = await db();
  await d.clear("kv");
  await d.clear("answers");
  try {
    localStorage.clear();
  } catch {
    /* private mode 등 */
  }
}
