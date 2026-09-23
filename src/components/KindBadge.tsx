import type { QuestionKind } from "@/db/schema";

/** 실제 기출 / 예상질문 구분은 항상 눈에 띄게 (SPEC 원칙 4). */
export const KIND_LABEL: Record<QuestionKind, string> = {
  actual: "실제 기출",
  example: "대학 공개 예시",
  predicted: "AI 예상질문",
  none: "문항 미공개",
};

const KIND_CLASS: Record<QuestionKind, string> = {
  actual: "bg-emerald-100 text-emerald-900 border-emerald-300",
  example: "bg-sky-100 text-sky-900 border-sky-300",
  predicted: "bg-purple-100 text-purple-900 border-purple-300",
  none: "bg-gray-100 text-gray-700 border-gray-300",
};

export function KindBadge({ kind, className = "" }: { kind: QuestionKind; className?: string }) {
  return (
    <span className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${KIND_CLASS[kind]} ${className}`}>
      {KIND_LABEL[kind]}
    </span>
  );
}
