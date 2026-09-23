"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { clearAll, getProfile, getQuestionSet, listAnswers, type StoredProfile } from "@/lib/local-store";

export function MyClient() {
  const [profile, setProfile] = useState<StoredProfile | null | undefined>(undefined);
  const [counts, setCounts] = useState({ questions: 0, answers: 0 });
  const [done, setDone] = useState(false);

  useEffect(() => {
    (async () => {
      const [p, s, a] = await Promise.all([getProfile(), getQuestionSet(), listAnswers()]);
      setProfile(p ?? null);
      setCounts({ questions: s?.questions.length ?? 0, answers: a.length });
    })();
  }, []);

  async function wipe() {
    if (!confirm("내 브라우저에 저장된 프로필·예상질문·답변·피드백을 모두 삭제합니다. 되돌릴 수 없습니다.")) return;
    await clearAll();
    // 서버 저장(옵트인)은 아직 없음. 도입 시 여기서 DELETE /api/me 도 함께 호출한다.
    setProfile(null);
    setCounts({ questions: 0, answers: 0 });
    setDone(true);
  }

  if (profile === undefined) return <main className="p-8 text-sm text-gray-500">불러오는 중…</main>;

  return (
    <main className="mx-auto max-w-xl px-4 py-10">
      <h1 className="text-2xl font-semibold">내 정보</h1>
      {done && <p className="mt-3 rounded bg-green-50 p-2 text-sm text-green-800">모두 삭제했습니다.</p>}
      {!profile ? (
        <p className="mt-4 text-sm text-gray-600">
          저장된 정보가 없습니다.{" "}
          <Link href="/onboarding" className="underline">
            시작하기
          </Link>
        </p>
      ) : (
        <dl className="mt-4 space-y-2 rounded border p-4 text-sm">
          <Row k="유형" v={profile.profileCode} />
          <Row k="대학·전형" v={`${profile.univName ?? "미정"} ${profile.admissionName ?? ""} ${profile.unit ?? ""}`} />
          <Row k="활동" v={profile.activities.join(" / ") || "-"} />
          <Row k="추가 정보" v={profile.notes || "-"} />
          <Row k="예상질문" v={`${counts.questions}개`} />
          <Row k="답변·피드백" v={`${counts.answers}건`} />
          <Row k="저장 위치" v="내 브라우저(IndexedDB)만. 서버에는 저장되지 않음" />
        </dl>
      )}
      <div className="mt-6 flex gap-2">
        <Link href="/practice" className="rounded border px-4 py-2 text-sm">
          연습으로
        </Link>
        <Link href="/onboarding" className="rounded border px-4 py-2 text-sm">
          다시 설정
        </Link>
        <button type="button" onClick={wipe} className="rounded border border-red-300 px-4 py-2 text-sm text-red-700">
          모든 데이터 삭제
        </button>
      </div>
    </main>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex gap-3">
      <dt className="w-24 shrink-0 text-gray-500">{k}</dt>
      <dd className="break-words">{v}</dd>
    </div>
  );
}
