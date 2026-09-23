import { describe, it, expect } from "vitest";
import { mintToken, verifyToken } from "./token";

describe("request token", () => {
  it("같은 scope·subject 로 검증되면 통과", () => {
    const t = mintToken("report", "y=1990&m=1&d=1");
    expect(verifyToken(t, "report", "y=1990&m=1&d=1")).toBe(true);
  });
  it("subject 가 다르면 실패 (파라미터 바꿔치기 방지)", () => {
    const t = mintToken("report", "y=1990&m=1&d=1");
    expect(verifyToken(t, "report", "y=1991&m=1&d=1")).toBe(false);
  });
  it("scope 가 다르면 실패", () => {
    const t = mintToken("report", "x");
    expect(verifyToken(t, "card", "x")).toBe(false);
  });
  it("만료된 토큰은 실패", () => {
    const t = mintToken("report", "x", -1);
    expect(verifyToken(t, "report", "x")).toBe(false);
  });
  it("형식이 깨진 토큰은 실패", () => {
    expect(verifyToken("", "report", "x")).toBe(false);
    expect(verifyToken("abc", "report", "x")).toBe(false);
    expect(verifyToken(undefined, "report", "x")).toBe(false);
    expect(verifyToken("123.", "report", "x")).toBe(false);
  });
});
