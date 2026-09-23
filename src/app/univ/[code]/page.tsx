import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { KindBadge } from "@/components/KindBadge";
import { QuestionCard } from "@/components/QuestionCard";
import { getUniversityByCode, questionsForUniversity, yearsForUniversity } from "@/lib/questions";

type Props = { params: Promise<{ code: string }>; searchParams: Promise<{ year?: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const u = getUniversityByCode(code);
  if (!u) return { title: "대학을 찾을 수 없음" };
  const years = yearsForUniversity(code);
  const span = years.length ? `${years[years.length - 1].year}~${years[0].year}학년도` : "";
  return {
    title: `${u.name} 면접 기출문항 ${span}`,
    description: `${u.name} 입학처가 공개한 면접·구술고사 기출문항과 출제의도를 전형·연도별로 정리했습니다. 실제 기출과 예상질문을 구분해 표시합니다.`,
  };
}

const CATEGORY_LABEL: Record<string, string> = {
  student_record: "서류(학생부) 기반 면접",
  essay_based: "제시문 기반 면접",
  personality: "인성면접",
  major: "전공 면접",
  english: "영어 면접",
  mmi: "적성·인성(MMI) 면접",
};

export default async function UnivPage({ params, searchParams }: Props) {
  const { code } = await params;
  const { year } = await searchParams;
  const u = getUniversityByCode(code);
  if (!u) notFound();
  const years = yearsForUniversity(code);
  const selectedYear = year && years.some((y) => String(y.year) === year) ? Number(year) : undefined;
  const qs = questionsForUniversity(code, selectedYear);

  // 연도 → 전형 → 문항
  const byYear = new Map<number, Map<string, typeof qs>>();
  for (const q of qs) {
    const adm = q.admissionName ?? "전형 미상";
    if (!byYear.has(q.year)) byYear.set(q.year, new Map());
    const m = byYear.get(q.year)!;
    if (!m.has(adm)) m.set(adm, []);
    m.get(adm)!.push(q);
  }
  const admissionSummary = new Map<string, { category: string | null; n: number }>();
  for (const q of qs) {
    const k = q.admissionName ?? "전형 미상";
    const cur = admissionSummary.get(k) ?? { category: q.category, n: 0 };
    cur.n++;
    admissionSummary.set(k, cur);
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <nav className="text-sm text-gray-500">
        <Link href="/univ" className="hover:underline">
          대학별 기출
        </Link>{" "}
        / {u.name}
      </nav>
      <h1 className="mt-2 text-2xl font-semibold">{u.name} 면접 기출문항</h1>
      <p className="mt-1 text-sm text-gray-600">
        <a href={u.admissionUrl} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline">
          입학처 홈페이지 ↗
        </a>
        {u.reportBoardUrl && (
          <>
            {" · "}
            <a href={u.reportBoardUrl} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline">
              공개자료 게시판 ↗
            </a>
          </>
        )}
      </p>

      <section className="mt-5 rounded-lg border bg-gray-50 p-4 text-sm">
        <h2 className="font-medium">전형별 면접 유형</h2>
        <ul className="mt-2 space-y-1">
          {[...admissionSummary.entries()].map(([name, v]) => (
            <li key={name} className="flex flex-wrap justify-between gap-2">
              <span>{name}</span>
              <span className="text-gray-600">
                {v.category ? CATEGORY_LABEL[v.category] ?? v.category : ""} · {v.n}문항
              </span>
            </li>
          ))}
        </ul>
        <p className="mt-3 text-xs text-gray-500">
          <KindBadge kind="actual" /> 는 대학이 공개한 실제 시행 문항, <KindBadge kind="example" /> 는 대학이 낸 예시, <KindBadge kind="predicted" /> 는 면접각이 생성한 예상질문입니다.
        </p>
      </section>

      <div className="mt-6 flex flex-wrap gap-2 text-sm">
        <Link href={`/univ/${code}`} className={`rounded-full border px-3 py-1 ${!selectedYear ? "bg-black text-white" : ""}`}>
          전체
        </Link>
        {years.map((y) => (
          <Link key={y.year} href={`/univ/${code}?year=${y.year}`} className={`rounded-full border px-3 py-1 ${selectedYear === y.year ? "bg-black text-white" : ""}`}>
            {y.year} ({y.n})
          </Link>
        ))}
      </div>

      {[...byYear.entries()].map(([yr, adms]) => (
        <section key={yr} className="mt-8">
          <h2 className="text-xl font-semibold">{yr}학년도</h2>
          {[...adms.entries()].map(([adm, list]) => (
            <div key={adm} className="mt-4">
              <h3 className="text-base font-medium text-gray-800">
                {adm} <span className="text-sm font-normal text-gray-500">({list.length})</span>
              </h3>
              <div className="mt-2 space-y-3">
                {list.map((q) => (
                  <QuestionCard key={q.id} q={q} showAdmission={false} />
                ))}
              </div>
            </div>
          ))}
        </section>
      ))}
      {qs.length === 0 && <p className="mt-8 text-sm text-gray-500">아직 등록된 문항이 없습니다. 이 대학은 평가영역·예시를 바탕으로 예상질문을 제공할 예정입니다.</p>}
    </main>
  );
}
