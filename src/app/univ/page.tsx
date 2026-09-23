import type { Metadata } from "next";
import Link from "next/link";

import { universitySummaries } from "@/lib/questions";

export const metadata: Metadata = {
  title: "대학별 면접 기출",
  description: "대학 입학처가 공개한 면접·구술고사 문항을 대학별로 정리했습니다. 문항마다 출처 링크를 제공합니다.",
};

const TYPE_LABEL: Record<string, string> = { general: "일반대", junior: "전문대", teachers: "교대", military: "사관학교", police: "경찰대", special: "특수대" };

export default function UnivIndexPage() {
  const rows = universitySummaries();
  const withData = rows.filter((r) => r.total > 0);
  const pending = rows.filter((r) => r.total === 0);
  return (
    <main className="mx-auto max-w-4xl px-4 py-10">
      <h1 className="text-2xl font-semibold">대학별 면접 기출</h1>
      <p className="mt-2 text-sm text-gray-600">
        「공교육정상화법」에 따라 각 대학이 공개한 선행학습 영향평가 보고서·기출문항을 구조화했습니다. 원문은 각 대학 입학처 링크에서 확인하세요.
        서류(학생부) 기반 면접·인성면접은 대학이 문항을 공개하지 않는 경우가 많아, 그 경우 평가영역과 예시만 제공됩니다.
      </p>
      <ul className="mt-6 grid gap-3 sm:grid-cols-2">
        {withData.map((u) => (
          <li key={u.code}>
            <Link href={`/univ/${u.code}`} className="block rounded-lg border p-4 hover:border-black">
              <div className="flex items-baseline justify-between">
                <span className="text-lg font-medium">{u.name}</span>
                <span className="text-xs text-gray-500">
                  {u.region} · {TYPE_LABEL[u.type] ?? u.type}
                </span>
              </div>
              <p className="mt-1 text-sm text-gray-600">
                문항 {u.total}개 (실제 기출 {u.actual}) · {u.minYear}~{u.maxYear}학년도
              </p>
            </Link>
          </li>
        ))}
      </ul>
      {pending.length > 0 && (
        <section className="mt-8">
          <h2 className="text-sm font-medium text-gray-700">수집 예정</h2>
          <p className="mt-1 text-sm text-gray-500">{pending.map((u) => u.name).join(", ")}</p>
        </section>
      )}
    </main>
  );
}
