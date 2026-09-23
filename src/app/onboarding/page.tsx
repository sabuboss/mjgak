import type { Metadata } from "next";
import { Suspense } from "react";

import { db, schema } from "@/db";
import { listUniversities } from "@/lib/questions";
import { issueSession } from "@/lib/session";

import { OnboardingForm } from "./OnboardingForm";

export const metadata: Metadata = { title: "시작하기", robots: { index: false } };
export const dynamic = "force-dynamic";

export default function OnboardingPage() {
  const session = issueSession();
  const profiles = db.select({ code: schema.applicantProfiles.code, label: schema.applicantProfiles.label, description: schema.applicantProfiles.description }).from(schema.applicantProfiles).all();
  const order = ["VOCATIONAL", "GED", "REPEAT", "OVERSEAS_3", "OVERSEAS_12", "ALTERNATIVE", "GENERAL"];
  profiles.sort((a, b) => order.indexOf(a.code) - order.indexOf(b.code));
  const univs = listUniversities().map((u) => ({ code: u.code, name: u.name }));
  return (
    <main className="mx-auto max-w-2xl px-4 py-10">
      <h1 className="text-2xl font-semibold">내 유형으로 시작하기</h1>
      <p className="mt-1 text-sm text-gray-600">입력한 내용은 내 브라우저에만 저장되고, 예상질문 생성에 필요한 요약만 서버로 보냅니다.</p>
      <Suspense fallback={null}>
        <OnboardingForm profiles={profiles} universities={univs} session={session} turnstileSiteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY} />
      </Suspense>
    </main>
  );
}
