import Link from "next/link";

import { QUESTION_KINDS, type QuestionKind } from "@/db/schema";
import { requireAdmin } from "@/lib/admin-auth";
import { listQuestions, listUniversities, reviewStats } from "@/lib/questions";

import { toggleVerified } from "./actions";

const KIND_LABEL: Record<QuestionKind, string> = { actual: "실제 기출", example: "대학 예시", predicted: "예상", none: "미공개" };

type SP = { univ?: string; year?: string; kind?: string; verified?: string; q?: string; page?: string; deleted?: string };

export default async function ReviewPage({ searchParams }: { searchParams: Promise<SP> }) {
  await requireAdmin("/admin/review");
  const sp = await searchParams;
  const filter = {
    univ: sp.univ || undefined,
    year: sp.year ? Number(sp.year) : undefined,
    kind: (QUESTION_KINDS as readonly string[]).includes(sp.kind ?? "") ? (sp.kind as QuestionKind) : undefined,
    verified: sp.verified === "1" ? true : sp.verified === "0" ? false : undefined,
    q: sp.q || undefined,
    page: sp.page ? Number(sp.page) : 1,
  };
  const { rows, total, page, pageSize } = listQuestions(filter);
  const univs = listUniversities();
  const stats = reviewStats();
  const pages = Math.max(1, Math.ceil(total / pageSize));
  const qs = (over: Partial<SP>) => {
    const p = new URLSearchParams();
    for (const [k, v] of Object.entries({ ...sp, ...over })) if (v && k !== "deleted") p.set(k, String(v));
    return `/admin/review?${p.toString()}`;
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <header className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-2xl font-semibold">문항 검수</h1>
        <p className="text-sm text-gray-500">
          {stats.map((s) => `${s.univName} ${s.verified}/${s.total}`).join(" · ")}
        </p>
      </header>
      {sp.deleted && <p className="mt-2 text-sm text-green-700">삭제했습니다.</p>}

      <form className="mt-4 grid grid-cols-2 gap-2 rounded border p-3 text-sm sm:grid-cols-6" method="get">
        <select name="univ" defaultValue={sp.univ ?? ""} className="rounded border px-2 py-1">
          <option value="">대학 전체</option>
          {univs.map((u) => (
            <option key={u.code} value={u.code}>
              {u.name}
            </option>
          ))}
        </select>
        <input name="year" defaultValue={sp.year ?? ""} placeholder="연도" className="rounded border px-2 py-1" inputMode="numeric" />
        <select name="kind" defaultValue={sp.kind ?? ""} className="rounded border px-2 py-1">
          <option value="">종류 전체</option>
          {QUESTION_KINDS.map((k) => (
            <option key={k} value={k}>
              {KIND_LABEL[k]}
            </option>
          ))}
        </select>
        <select name="verified" defaultValue={sp.verified ?? ""} className="rounded border px-2 py-1">
          <option value="">검수 전체</option>
          <option value="0">미검수</option>
          <option value="1">검수완료</option>
        </select>
        <input name="q" defaultValue={sp.q ?? ""} placeholder="문항 텍스트 검색" className="rounded border px-2 py-1" />
        <button className="rounded bg-black px-3 py-1 text-white">필터</button>
      </form>

      <p className="mt-3 text-sm text-gray-600">
        {total}건 · {page}/{pages} 페이지
      </p>

      <ul className="mt-2 divide-y rounded border">
        {rows.map((r) => (
          <li key={r.id} className="flex flex-col gap-1 p-3 sm:flex-row sm:items-start sm:gap-4">
            <div className="flex shrink-0 gap-2 text-xs text-gray-500 sm:w-40 sm:flex-col">
              <span>
                {r.univName} {r.year}
              </span>
              <span className={r.kind === "actual" ? "text-emerald-700" : r.kind === "predicted" ? "text-purple-700" : "text-sky-700"}>{KIND_LABEL[r.kind]}</span>
              <span className="truncate" title={r.admissionName ?? ""}>
                {r.admissionName}
              </span>
            </div>
            <div className="min-w-0 flex-1">
              <Link href={`/admin/review/${r.id}`} className="line-clamp-3 text-sm hover:underline">
                {r.text}
              </Link>
              <p className="mt-1 truncate text-xs text-gray-500" title={r.unit}>
                {r.unit}
              </p>
              <a href={r.sourceUrl} target="_blank" rel="noreferrer" className="text-xs text-blue-700 hover:underline">
                출처{r.sourcePage ? ` p.${r.sourcePage}` : ""} ↗
              </a>
            </div>
            <form action={toggleVerified} className="shrink-0">
              <input type="hidden" name="id" value={r.id} />
              <input type="hidden" name="value" value={r.verified ? "0" : "1"} />
              <button className={`rounded px-2 py-1 text-xs ${r.verified ? "bg-emerald-600 text-white" : "border"}`}>{r.verified ? "검수완료" : "미검수"}</button>
            </form>
          </li>
        ))}
        {rows.length === 0 && <li className="p-6 text-center text-sm text-gray-500">조건에 맞는 문항이 없습니다.</li>}
      </ul>

      <nav className="mt-4 flex gap-2 text-sm">
        {page > 1 && (
          <Link className="rounded border px-3 py-1" href={qs({ page: String(page - 1) })}>
            이전
          </Link>
        )}
        {page < pages && (
          <Link className="rounded border px-3 py-1" href={qs({ page: String(page + 1) })}>
            다음
          </Link>
        )}
      </nav>
    </main>
  );
}
