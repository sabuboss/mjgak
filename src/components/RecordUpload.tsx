"use client";
/**
 * 생기부 PDF 클라이언트 파싱 (SPEC 3장 5, 원칙 1).
 * - pdfjs-dist 가 브라우저 안에서 텍스트를 뽑는다. 워커도 /pdf.worker.min.mjs (같은 출처). 서버 전송 없음.
 * - 원문은 이 컴포넌트의 메모리에만 있고 저장하지 않는다. 사용자가 고른 활동 한 줄 요약만 부모(온보딩 폼)로 올라간다.
 * - 스캔(이미지) PDF 는 텍스트가 없어 안내만 한다. OCR 은 하지 않는다.
 */
import { useState } from "react";

import { candidatesFromLines, type Candidate } from "@/lib/record-parse";

async function extractText(file: File, onProgress: (p: number) => void): Promise<string[]> {
  const pdfjs = await import("pdfjs-dist");
  pdfjs.GlobalWorkerOptions.workerSrc = "/pdf.worker.min.mjs";
  const data = new Uint8Array(await file.arrayBuffer());
  const doc = await pdfjs.getDocument({ data }).promise;
  const lines: string[] = [];
  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
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
    onProgress(i / doc.numPages);
  }
  return lines;
}

export function RecordUpload({ onPick, max = 5 }: { onPick: (lines: string[]) => void; max?: number }) {
  const [status, setStatus] = useState<"idle" | "parsing" | "done" | "empty" | "error">("idle");
  const [progress, setProgress] = useState(0);
  const [cands, setCands] = useState<Candidate[]>([]);
  const [picked, setPicked] = useState<Set<number>>(new Set());

  async function onFile(f: File | undefined) {
    if (!f) return;
    if (f.size > 20 * 1024 * 1024) {
      setStatus("error");
      return;
    }
    setStatus("parsing");
    setProgress(0);
    setCands([]);
    setPicked(new Set());
    try {
      const lines = await extractText(f, setProgress);
      const c = candidatesFromLines(lines);
      setCands(c);
      setStatus(c.length ? "done" : "empty");
    } catch {
      setStatus("error");
    }
  }

  function toggle(i: number) {
    const n = new Set(picked);
    if (n.has(i)) n.delete(i);
    else if (n.size < max) n.add(i);
    setPicked(n);
  }

  return (
    <div className="rounded-lg border border-dashed p-3 text-sm">
      <p className="font-medium">생기부 PDF로 활동 뽑기 (선택)</p>
      <p className="mt-1 text-xs text-gray-600">파일은 내 브라우저 안에서만 읽습니다. 서버로 전송·저장되지 않으며, 아래에서 고른 한 줄 요약만 사용합니다.</p>
      <input type="file" accept="application/pdf" onChange={(e) => onFile(e.target.files?.[0])} className="mt-2 block text-xs" />
      {status === "parsing" && <p className="mt-2 text-xs text-gray-600">읽는 중… {Math.round(progress * 100)}%</p>}
      {status === "empty" && <p className="mt-2 text-xs text-amber-800">텍스트를 찾지 못했습니다. 스캔 이미지 PDF이거나 형식이 다릅니다. 활동을 직접 입력해 주세요.</p>}
      {status === "error" && <p className="mt-2 text-xs text-red-700">파일을 읽지 못했습니다 (20MB 이하 PDF만).</p>}
      {status === "done" && (
        <>
          <p className="mt-2 text-xs text-gray-600">
            활동 후보 {cands.length}개. 최대 {max}개를 고르세요 ({picked.size}/{max}).
          </p>
          <ul className="mt-2 max-h-64 space-y-1 overflow-auto">
            {cands.map((c, i) => (
              <li key={i}>
                <label className={`flex cursor-pointer gap-2 rounded p-1 text-xs ${picked.has(i) ? "bg-gray-100" : ""}`}>
                  <input type="checkbox" checked={picked.has(i)} onChange={() => toggle(i)} className="mt-0.5" />
                  <span>
                    <span className="mr-1 rounded bg-gray-200 px-1 text-[10px]">{c.section}</span>
                    {c.text}
                  </span>
                </label>
              </li>
            ))}
          </ul>
          <button
            type="button"
            disabled={picked.size === 0}
            onClick={() => {
              onPick([...picked].map((i) => cands[i].text.slice(0, 300)));
              setStatus("idle");
              setCands([]);
              setPicked(new Set());
            }}
            className="mt-2 rounded bg-black px-3 py-1 text-xs text-white disabled:opacity-40"
          >
            선택한 활동 넣기
          </button>
        </>
      )}
    </div>
  );
}
