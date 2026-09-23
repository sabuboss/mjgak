/** 페이지(서버 컴포넌트)가 발급해 클라이언트에 내려 보내는 세션 토큰. API 직접 열거 호출을 막는다 (A3). */
import { randomUUID } from "node:crypto";

import { mintToken } from "./security/token";

export type SessionAuth = { sid: string; token: string };

export function issueSession(): SessionAuth {
  const sid = randomUUID();
  return { sid, token: mintToken("session", sid) };
}
