/**
 * DB 클라이언트 (서버 전용). Next.js 서버 컴포넌트/라우트 핸들러/스크립트에서만 import 한다.
 * 파일 경로는 DATABASE_URL (기본 data/mjgak.db). 배포 시 Postgres 로 바꾸려면 이 파일만 교체.
 */
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";
import fs from "node:fs";
import path from "node:path";

import * as schema from "./schema";

export const DB_PATH = process.env.DATABASE_URL ?? "data/mjgak.db";

declare global {
  var __mjgakDb: ReturnType<typeof createDb> | undefined;
}

function createDb() {
  fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
  const sqlite = new Database(DB_PATH);
  sqlite.pragma("journal_mode = WAL");
  sqlite.pragma("foreign_keys = ON");
  return drizzle(sqlite, { schema });
}

// dev 핫리로드 시 커넥션이 늘어나지 않도록 globalThis 에 캐시
export const db = globalThis.__mjgakDb ?? createDb();
if (process.env.NODE_ENV !== "production") globalThis.__mjgakDb = db;

export { schema };
