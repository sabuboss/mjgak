"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { KindBadge } from "@/components/KindBadge";
import { useTurnstile } from "@/components/Turnstile";
import { FeedbackResponse } from "@/lib/llm/schemas";
import { addAnswer, getProfile, getQuestionSet, listAnswers, type StoredAnswer, type StoredProfile, type StoredQuestionSet } from "@/lib/local-store";
import type { SessionAuth } from "@/lib/session";

const SCORE_LABEL: Record<keyof FeedbackResponse["scores"], string> = { structure: "구조", evidence: "근거", authenticity: "진정성", length: "길이", fit: "대학 부합" };

/** 실제 기출은 초록 배지, LLM 예상은 보라 배지, 키 없이 만든 템플릿 질문은 회색 "유형 템플릿" — 셋을 섞어 보이지 않게 한다. */
function BasisBadge({ basis, mode }: { basis: "actual" | "predicted"; mode: "llm" | "template" }) {
  if (basis === "actual") return <KindBadge kind="actual" />;
  if (mode === "template") return <span className="inline-block rounded-full border border-gray-300 bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700">유형 템플릿</span>;
  return <KindBadge kind="predicted" />;
}

export function PracticeClient({ session, turnstileSiteKey }: { session: SessionAuth; turnstileSiteKey?: string }) {
  const [profile, setProfileState] = useState<StoredProfile | null | undefined>(undefined);
  const [set, setSet] = useState<StoredQuestionSet | null>(null);
  const [answers, setAnswers] = useState<(StoredAnswer & { id: number })[]>([]);
  const [idx, setIdx] = useState(0);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [latest, setLatest] = useState<FeedbackResponse | null>(null);
  const turnstile = useTurnstile(turnstileSiteKey);

  useEffect(() => {
    (async () => {
      const [p, s, a] = await Promise.all([getProfile(), getQuestionSet(), listAnswers()]);
      setProfileState(p ?? null);
      setSet(s ?? null);
      setAnswers(a);
    })();
  }, []);

  const q = set?.questions[idx];
  const history = useMemo(() => answers.filter((a) => a.questionIndex === idx).sort((a, b) => b.id - a.id), [answers, idx]);
  const answered = useMemo(() => new Set(answers.map((a) => a.questionIndex)), [answers]);

  function select(i: number) {
    setIdx(i);
    setDraft("");
    setLatest(null);
    setError(null);
  }

  async function submit() {
    if (!q || !profile) return;
    setBusy(true);
    setError(null);
    try {
      const res = await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...session,
          turnstile: (await turnstile.getToken()) ?? undefined,
          question: q.question,
          answer: draft,
          basis: q.basis,
          whyAsked: q.why_asked,
          profileCode: profile.profileCode,
          univCode: profile.univCode,
        }),
      });
      turnstile.consume();
      if (!res.ok) throw new Error(res.status === 429 ? "피드백 요청이 너무 많습니다. 잠시 후 다시 시도해 주세요." : `피드백 실패 (${res.status})`);
      const fb = FeedbackResponse.parse(await res.json());
      const rec: StoredAnswer = { questionIndex: idx, question: q.question, answer: draft, feedback: fb, createdAt: new Date().toISOString() };
      await addAnswer(rec);
      setAnswers(await listAnswers());
      setLatest(fb);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  if (profile === undefined) return <main className="p-8 text-sm text-gray-500">불러오는 중…</main>;
  if (!profile || !set) {
    return (
      <main className="mx-auto max-w-xl px-4 py-16 text-center">
        <p>아직 예상질문이 없습니다.</p>
        <Link href="/onboarding" className="mt-4 inline-block rounded bg-black px-5 py-2 text-white">
          시작하기
        </Link>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <header className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-xl font-semibold">연습 · {profile.univName ?? "대학 미정"}</h1>
        <p className="text-xs text-gray-500">
          {answered.size}/{set.questions.length} 답변함 · <Link href="/my" className="underline">내 정보</Link>
        </p>
      </header>
      {set.notice && <p className="mt-2 rounded bg-amber-50 p-2 text-xs text-amber-900">{set.notice}</p>}

      <div className="mt-4 grid gap-4 md:grid-cols-[280px_1fr]">
        <ol className="max-h-[70vh] overflow-auto rounded border text-sm">
          {set.questions.map((it, i) => (
            <li key={i}>
              <button type="button" onClick={() => select(i)} className={`flex w-full flex-col gap-1 border-b p-2 text-left ${i === idx ? "bg-gray-100" : ""}`}>
                <span className="flex items-center gap-2 text-xs">
                  <BasisBadge basis={it.basis} mode={set.mode} />
                  {answered.has(i) && <span className="text-emerald-700">✓</span>}
                </span>
                <span className="line-clamp-2">{it.question}</span>
              </button>
            </li>
          ))}
        </ol>

        <section>
          {q && (
            <>
              <div className="flex items-center gap-2 text-xs">
                <BasisBadge basis={q.basis} mode={set.mode} />
                <span className="text-gray-500">
                  {idx + 1} / {set.questions.length}
                </span>
              </div>
              <h2 className="mt-2 text-lg font-medium leading-relaxed">{q.question}</h2>
              <details className="mt-2 text-sm text-gray-700">
                <summary className="cursor-pointer">왜 묻나요 · 답변 힌트</summary>
                <p className="mt-1">
                  <span className="font-medium">의도</span> {q.why_asked}
                </p>
                <p className="mt-1">
                  <span className="font-medium">힌트</span> {q.tips}
                </p>
              </details>
              <textarea
                value={draft}
                onChange={(e) => setDraft(e.target.value.slice(0, 3000))}
                rows={7}
                placeholder="말하듯이 써 보세요. 40~60초 분량(200~300자)이 기준입니다."
                className="mt-3 w-full rounded border px-3 py-2 text-sm leading-relaxed"
              />
              <div className="mt-1 flex items-center justify-between text-xs text-gray-500">
                <span>{draft.length}자</span>
                <span>답변은 내 브라우저에만 저장됩니다</span>
              </div>
              {turnstile.element}
              {error && <p className="mt-2 rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}
              <div className="mt-2 flex gap-2">
                <button type="button" onClick={submit} disabled={busy || draft.trim().length < 10} className="rounded bg-black px-4 py-2 text-sm text-white disabled:opacity-40">
                  {busy ? "코칭 중…" : "피드백 받기"}
                </button>
                {idx < set.questions.length - 1 && (
                  <button type="button" onClick={() => select(idx + 1)} className="rounded border px-4 py-2 text-sm">
                    다음 질문
                  </button>
                )}
              </div>

              {(latest ?? history[0]?.feedback) && <FeedbackView fb={(latest ?? history[0]!.feedback)!} />}
              {history.length > 1 && (
                <p className="mt-3 text-xs text-gray-500">이 질문에 {history.length}번 답했습니다. 마지막 답변의 피드백을 표시합니다.</p>
              )}
            </>
          )}
        </section>
      </div>
    </main>
  );
}

function FeedbackView({ fb }: { fb: FeedbackResponse }) {
  return (
    <div className="mt-5 rounded-lg border bg-white p-4">
      {fb.notice && <p className="mb-2 rounded bg-amber-50 p-2 text-xs text-amber-900">{fb.notice}</p>}
      <ul className="flex flex-wrap gap-2 text-xs">
        {(Object.keys(fb.scores) as (keyof typeof fb.scores)[]).map((k) => (
          <li key={k} className="rounded border px-2 py-1">
            {SCORE_LABEL[k]} <strong>{fb.scores[k]}</strong>/5
          </li>
        ))}
      </ul>
      <p className="mt-3 text-sm">{fb.summary}</p>
      <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm">
        {fb.improvements.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ol>
      <details className="mt-3 text-sm">
        <summary className="cursor-pointer font-medium">개선 예시 답변</summary>
        <p className="mt-2 whitespace-pre-line rounded bg-gray-50 p-3 leading-relaxed">{fb.example_answer}</p>
      </details>
    </div>
  );
}
