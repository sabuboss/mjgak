import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

import { candidatesFromLines } from "./record-parse";

async function extractLines(file: string): Promise<string[]> {
  // 브라우저 컴포넌트와 같은 라이브러리의 Node(legacy) 빌드로 추출 → 동일 휴리스틱 검증
  const pdfjs = await import("pdfjs-dist/legacy/build/pdf.mjs");
  const data = new Uint8Array(fs.readFileSync(file));
  const doc = await pdfjs.getDocument({ data }).promise;
  const lines: string[] = [];
  for (let i = 1; i <= doc.numPages; i++) {
    const content = await (await doc.getPage(i)).getTextContent();
    let cur = "";
    for (const item of content.items) {
      if (!("str" in item)) continue;
      cur += item.str;
      if (item.hasEOL) {
        lines.push(cur.trim());
        cur = "";
      }
    }
    if (cur.trim()) lines.push(cur.trim());
  }
  return lines;
}

describe("record-parse", () => {
  it("샘플 생기부 PDF 에서 활동 문장만 뽑고 인적사항·출결은 제외한다", async () => {
    const lines = await extractLines(path.join(process.cwd(), "tests/fixtures/sample_record.pdf"));
    expect(lines.length).toBeGreaterThan(5);
    const c = candidatesFromLines(lines);
    const texts = c.map((x) => x.text).join("\n");
    expect(c.length).toBeGreaterThanOrEqual(3);
    expect(texts).toContain("탐구 보고서");
    expect(texts).toContain("캠페인");
    expect(texts).not.toMatch(/주민등록|결석|지각/);
    expect(c.some((x) => x.section === "세특")).toBe(true);
  });

  it("짧은 줄·노이즈만 있으면 빈 배열", () => {
    expect(candidatesFromLines(["성명 홍길동", "결석 0", "짧다"])).toEqual([]);
  });
});
