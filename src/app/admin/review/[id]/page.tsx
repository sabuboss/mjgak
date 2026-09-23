import Link from "next/link";
import { notFound } from "next/navigation";

import { QUESTION_KINDS } from "@/db/schema";
import { requireAdmin } from "@/lib/admin-auth";
import { getQuestion } from "@/lib/questions";

import { deleteQuestion, updateQuestion } from "../actions";

const KIND_LABEL = { actual: "실제 기출", example: "대학 예시", predicted: "예상(LLM)", none: "미공개(평가영역만)" } as const;

function Field({ label, name, value, rows = 3 }: { label: string; name: string; value: string; rows?: number }) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      <span className="font-medium">{label}</span>
      <textarea name={name} defaultValue={value} rows={rows} className="rounded border px-2 py-1 font-mono text-xs leading-relaxed" />
    </label>
  );
}

export default async function EditQuestionPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ saved?: string; error?: string }>;
}) {
  const { id } = await params;
  await requireAdmin(`/admin/review/${id}`);
  const { saved, error } = await searchParams;
  const row = getQuestion(Number(id));
  if (!row) notFound();
  const q = row.q;

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <Link href="/admin/review" className="text-sm text-blue-700 hover:underline">
        ← 목록
      </Link>
      <h1 className="mt-2 text-xl font-semibold">
        #{q.id} · {row.univName} {q.year} · {row.admissionName}
      </h1>
      <p className="mt-1 text-sm">
        <a href={q.sourceUrl} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline">
          원문 출처 열기{q.sourcePage ? ` (p.${q.sourcePage})` : ""} ↗
        </a>
        <span className="ml-3 text-gray-500">검수는 반드시 원문과 대조한 뒤에 켜세요. 수학·과학 문항은 수식이 빠져 있을 수 있습니다.</span>
      </p>
      {saved && <p className="mt-3 rounded bg-green-50 p-2 text-sm text-green-800">저장했습니다.</p>}
      {error && <p className="mt-3 rounded bg-red-50 p-2 text-sm text-red-800">{error}</p>}

      <form action={updateQuestion} className="mt-6 flex flex-col gap-4">
        <input type="hidden" name="id" value={q.id} />
        <div className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
          <label className="flex flex-col gap-1">
            <span className="font-medium">종류</span>
            <select name="kind" defaultValue={q.kind} className="rounded border px-2 py-1">
              {QUESTION_KINDS.map((k) => (
                <option key={k} value={k}>
                  {KIND_LABEL[k]}
                </option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className="font-medium">학년도</span>
            <input name="year" defaultValue={q.year} className="rounded border px-2 py-1" inputMode="numeric" />
          </label>
          <label className="flex flex-col gap-1">
            <span className="font-medium">출처 페이지</span>
            <input name="sourcePage" defaultValue={q.sourcePage ?? ""} className="rounded border px-2 py-1" inputMode="numeric" />
          </label>
          <label className="flex items-end gap-2 pb-1">
            <input type="checkbox" name="verified" defaultChecked={q.verified} />
            <span className="font-medium">검수 완료</span>
          </label>
        </div>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">모집단위</span>
          <input name="unit" defaultValue={q.unit} className="rounded border px-2 py-1" />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">출처 URL</span>
          <input name="sourceUrl" defaultValue={q.sourceUrl} className="rounded border px-2 py-1 font-mono text-xs" />
        </label>
        <Field label="문항 (원문 그대로)" name="text" value={q.text} rows={4} />
        <Field label="제시문" name="presentedMaterial" value={q.presentedMaterial} rows={10} />
        <Field label="출제 의도 (요약)" name="intent" value={q.intent} />
        <Field label="채점 기준 / 평가 요소 (요약)" name="rubric" value={q.rubric} />
        <Field label="해설 요점" name="modelAnswerHint" value={q.modelAnswerHint} rows={5} />
        <div className="flex gap-2">
          <button className="rounded bg-black px-4 py-2 text-sm text-white">저장</button>
        </div>
      </form>
      <form action={deleteQuestion} className="mt-6 border-t pt-4">
        <input type="hidden" name="id" value={q.id} />
        <button className="rounded border border-red-300 px-3 py-1 text-xs text-red-700">이 문항 삭제</button>
      </form>
    </main>
  );
}
