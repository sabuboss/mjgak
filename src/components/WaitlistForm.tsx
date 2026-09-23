"use client";

import { useState } from "react";

export function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle" | "busy" | "done" | "error">("idle");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setState("busy");
    try {
      const res = await fetch("/api/waitlist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, website: "" }) });
      setState(res.ok ? "done" : "error");
    } catch {
      setState("error");
    }
  }

  if (state === "done") return <p className="text-sm text-emerald-700">등록됐습니다. 정식 오픈 때 알려 드릴게요.</p>;
  return (
    <form onSubmit={submit} className="flex flex-col gap-2 sm:flex-row">
      <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="이메일" className="flex-1 rounded border px-3 py-2 text-sm" />
      <button disabled={state === "busy"} className="rounded bg-black px-4 py-2 text-sm text-white disabled:opacity-40">
        오픈 알림 받기
      </button>
      {state === "error" && <p className="text-xs text-red-700">등록에 실패했습니다. 잠시 후 다시 시도해 주세요.</p>}
    </form>
  );
}
