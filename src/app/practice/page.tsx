import type { Metadata } from "next";

import { issueSession } from "@/lib/session";

import { PracticeClient } from "./PracticeClient";

export const metadata: Metadata = { title: "연습", robots: { index: false } };
export const dynamic = "force-dynamic";

export default function PracticePage() {
  return <PracticeClient session={issueSession()} turnstileSiteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY} />;
}
