/**
 * Anthropic 클라이언트 (서버 전용). 키는 ANTHROPIC_API_KEY, 모델은 ANTHROPIC_MODEL(기본 claude-sonnet-5).
 * 키가 없으면 hasLlm() 이 false 이고, 호출부는 템플릿/규칙 기반 폴백으로 동작한다 (베타·로컬 개발용).
 */
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";
import path from "node:path";

export const MODEL = process.env.ANTHROPIC_MODEL ?? "claude-sonnet-5";

export function hasLlm(): boolean {
  return Boolean(process.env.ANTHROPIC_API_KEY);
}

let _client: Anthropic | null = null;
export function anthropic(): Anthropic {
  if (!_client) _client = new Anthropic({ timeout: 90_000, maxRetries: 1 });
  return _client;
}

const promptCache = new Map<string, { text: string; version: string }>();

/** prompts/<name>.md 를 읽는다. 첫 줄 주석의 "vN" 을 버전으로 쓴다 (캐시 키에 포함). */
export function loadPrompt(name: string): { text: string; version: string } {
  const hit = promptCache.get(name);
  if (hit && process.env.NODE_ENV === "production") return hit;
  const file = path.join(process.cwd(), "prompts", `${name}.md`);
  const raw = fs.readFileSync(file, "utf8");
  const version = /<!--\s*(v\d+[^\s·]*)/.exec(raw)?.[1] ?? "v0";
  const text = raw.replace(/^<!--[\s\S]*?-->\s*/, "");
  const out = { text, version };
  promptCache.set(name, out);
  return out;
}

/** 사용자 입력을 LLM 에 넣을 때: 지시가 아닌 자료임을 구조로 표시하고 길이를 자른다 (C2). */
export function userBlock(tag: string, value: string, max = 4000): string {
  const v = value.replace(/<\/?[a-z_]+>/gi, "").slice(0, max);
  return `<${tag}>\n${v}\n</${tag}>`;
}
