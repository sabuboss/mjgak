import type { QuestionKind } from "@/db/schema";

import { KindBadge } from "./KindBadge";

export type QuestionCardData = {
  id: number;
  year: number;
  kind: QuestionKind;
  unit: string;
  text: string;
  presentedMaterial: string;
  intent: string;
  rubric: string;
  modelAnswerHint: string;
  verified: boolean;
  sourceUrl: string;
  sourcePage: number | null;
  admissionName: string | null;
};

/** 문항 1개. 제시문·해설은 접어 두고, 출처 링크는 항상 노출한다 (원문 PDF 재배포 대신). */
export function QuestionCard({ q, showAdmission = true }: { q: QuestionCardData; showAdmission?: boolean }) {
  const material = q.presentedMaterial.length > 1500 ? q.presentedMaterial.slice(0, 1500) + " …(이하 생략, 출처에서 확인)" : q.presentedMaterial;
  return (
    <article className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-center gap-2 text-xs text-gray-600">
        <KindBadge kind={q.kind} />
        <span>{q.year}학년도</span>
        {showAdmission && q.admissionName && <span>· {q.admissionName}</span>}
        {!q.verified && <span className="rounded bg-amber-50 px-1.5 py-0.5 text-amber-800">검수 전 · 원문과 대조 필요</span>}
      </div>
      <p className="mt-2 whitespace-pre-line text-[15px] leading-relaxed">{q.text}</p>
      {q.unit && (
        <p className="mt-2 text-xs text-gray-500" title={q.unit}>
          모집단위: {q.unit.length > 120 ? q.unit.slice(0, 120) + "…" : q.unit}
        </p>
      )}
      {material && (
        <details className="mt-2">
          <summary className="cursor-pointer text-sm text-gray-700">제시문 보기</summary>
          <pre className="mt-2 max-h-96 overflow-auto whitespace-pre-wrap rounded bg-gray-50 p-3 font-sans text-sm leading-relaxed">{material}</pre>
        </details>
      )}
      {(q.intent || q.rubric || q.modelAnswerHint) && (
        <details className="mt-2">
          <summary className="cursor-pointer text-sm text-gray-700">출제 의도 · 평가 요소 · 해설</summary>
          <div className="mt-2 space-y-2 text-sm">
            {q.intent && (
              <p>
                <span className="font-medium">출제 의도</span> {q.intent}
              </p>
            )}
            {q.rubric && (
              <p className="whitespace-pre-line">
                <span className="font-medium">평가 요소</span> {q.rubric}
              </p>
            )}
            {q.modelAnswerHint && (
              <p className="whitespace-pre-line">
                <span className="font-medium">해설</span> {q.modelAnswerHint}
              </p>
            )}
          </div>
        </details>
      )}
      <p className="mt-3 text-xs">
        <a href={q.sourceUrl} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline">
          출처: 대학 입학처 공개자료{q.sourcePage ? ` (p.${q.sourcePage})` : ""} ↗
        </a>
      </p>
    </article>
  );
}
