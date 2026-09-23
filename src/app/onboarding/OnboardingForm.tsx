"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

import { useTurnstile } from "@/components/Turnstile";
import type { ProfileCode } from "@/db/schema";
import { GenerateResponse } from "@/lib/llm/schemas";
import { setProfile, setQuestionSet } from "@/lib/local-store";
import type { SessionAuth } from "@/lib/session";

type Props = {
  profiles: { code: ProfileCode; label: string; description: string }[];
  universities: { code: string; name: string }[];
  session: SessionAuth;
  turnstileSiteKey?: string;
};

const NOTES_HINT: Record<ProfileCode, string> = {
  GENERAL: "특별히 강조하고 싶은 점 (선택)",
  VOCATIONAL: "고교 전공(학과), 취득 자격증, 현장실습 여부 등",
  GED: "학교를 그만둔(다니지 않은) 시기와 사유, 검정고시 합격 시기, 학교 밖에서 한 일",
  REPEAT: "N수 횟수, 작년 지원 대학·학과(있다면), 재수 기간에 한 일",
  OVERSEAS_3: "거주 국가, 이수 과정(IB/AP/현지 등), 해외 거주 기간, 한국어 수준",
  OVERSEAS_12: "거주 국가, 이수 과정, 한국어 학습 기간·TOPIK 등급, 한국 방문 경험",
  ALTERNATIVE: "대안학교 유형(인가/비인가), 검정고시 병행 여부, 대표 프로젝트",
};

const THIS_YEAR = new Date().getFullYear();

export function OnboardingForm({ profiles, universities, session, turnstileSiteKey }: Props) {
  const router = useRouter();
  const sp = useSearchParams();
  const [step, setStep] = useState(0);
  const [profileCode, setProfileCode] = useState<ProfileCode | "">((sp.get("type") as ProfileCode) || "");
  const [birthYear, setBirthYear] = useState("");
  const [consent, setConsent] = useState(false);
  const [univCode, setUnivCode] = useState("");
  const [admissionName, setAdmissionName] = useState("");
  const [unit, setUnit] = useState("");
  const [activities, setActivities] = useState<string[]>(["", "", ""]);
  const [notes, setNotes] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const turnstile = useTurnstile(turnstileSiteKey);

  const by = Number(birthYear);
  const age = by ? THIS_YEAR - by : 0;
  const under14 = by > 0 && age < 14;
  const step0Ok = profileCode !== "" && by >= THIS_YEAR - 60 && by <= THIS_YEAR - 10 && (!under14 || consent);
  const filledActivities = activities.map((a) => a.trim()).filter(Boolean);

  async function submit() {
    setBusy(true);
    setError(null);
    try {
      const payload = {
        ...session,
        turnstile: (await turnstile.getToken()) ?? undefined,
        profileCode,
        univCode: univCode || undefined,
        admissionName: admissionName || undefined,
        unit: unit || undefined,
        activities: filledActivities,
        notes,
      };
      const res = await fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      turnstile.consume();
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(res.status === 429 ? "요청이 너무 많습니다. 잠시 후 다시 시도해 주세요." : res.status === 503 ? "지금 생성 중인 요청이 많습니다. 몇 초 후 다시 눌러 주세요." : `생성 실패 (${j.error ?? res.status})`);
      }
      const data = GenerateResponse.parse(await res.json());
      await setProfile({
        profileCode: profileCode as ProfileCode,
        univCode: univCode || undefined,
        univName: universities.find((u) => u.code === univCode)?.name,
        admissionName: admissionName || undefined,
        unit: unit || undefined,
        activities: filledActivities,
        notes,
        birthYear: by,
        guardianConsent: consent,
        createdAt: new Date().toISOString(),
      });
      await setQuestionSet({ mode: data.mode, notice: data.notice, questions: data.questions, createdAt: new Date().toISOString() });
      router.push("/practice");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mt-6">
      <ol className="flex gap-2 text-xs text-gray-500">
        {["유형", "지원 대학", "내 활동", "생성"].map((s, i) => (
          <li key={s} className={`rounded-full border px-2 py-0.5 ${i === step ? "border-black text-black" : ""}`}>
            {i + 1}. {s}
          </li>
        ))}
      </ol>

      {step === 0 && (
        <section className="mt-6">
          <h2 className="font-medium">나는 어떤 지원자인가요?</h2>
          <ul className="mt-3 grid gap-2 sm:grid-cols-2">
            {profiles.map((p) => (
              <li key={p.code}>
                <button
                  type="button"
                  onClick={() => setProfileCode(p.code)}
                  className={`w-full rounded-lg border p-3 text-left ${profileCode === p.code ? "border-black bg-gray-50" : ""}`}
                >
                  <p className="font-medium">{p.label}</p>
                  <p className="mt-1 line-clamp-2 text-xs text-gray-600">{p.description}</p>
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <label className="text-sm">
              <span className="font-medium">출생 연도</span>
              <input value={birthYear} onChange={(e) => setBirthYear(e.target.value.replace(/\D/g, "").slice(0, 4))} inputMode="numeric" placeholder="예: 2008" className="mt-1 w-full rounded border px-3 py-2" />
              <span className="mt-1 block text-xs text-gray-500">연령 확인용. 서버에 보내지 않습니다.</span>
            </label>
            {under14 && (
              <label className="flex items-start gap-2 rounded border border-amber-300 bg-amber-50 p-3 text-sm">
                <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} className="mt-1" />
                <span>만 14세 미만입니다. 법정대리인(보호자)의 동의를 받았음을 확인합니다.</span>
              </label>
            )}
          </div>
          <button type="button" disabled={!step0Ok} onClick={() => setStep(1)} className="mt-6 rounded bg-black px-5 py-2 text-white disabled:opacity-40">
            다음
          </button>
        </section>
      )}

      {step === 1 && (
        <section className="mt-6 space-y-4">
          <h2 className="font-medium">지원 대학·전형·학과</h2>
          <label className="block text-sm">
            <span className="font-medium">대학</span>
            <select value={univCode} onChange={(e) => setUnivCode(e.target.value)} className="mt-1 w-full rounded border px-3 py-2">
              <option value="">아직 안 정했어요 / 목록에 없음</option>
              {universities.map((u) => (
                <option key={u.code} value={u.code}>
                  {u.name}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm">
            <span className="font-medium">전형</span>
            <input value={admissionName} onChange={(e) => setAdmissionName(e.target.value.slice(0, 60))} placeholder="예: 학생부종합 활동우수형, 특성화고졸업자전형, 재외국민 특별전형" className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <label className="block text-sm">
            <span className="font-medium">모집단위(학과·계열)</span>
            <input value={unit} onChange={(e) => setUnit(e.target.value.slice(0, 80))} placeholder="예: 컴퓨터공학과, 간호학과, 인문계열" className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <div className="flex gap-2">
            <button type="button" onClick={() => setStep(0)} className="rounded border px-4 py-2">
              이전
            </button>
            <button type="button" onClick={() => setStep(2)} className="rounded bg-black px-5 py-2 text-white">
              다음
            </button>
          </div>
        </section>
      )}

      {step === 2 && (
        <section className="mt-6 space-y-4">
          <h2 className="font-medium">내 활동·경험 (3~5개, 한 줄씩)</h2>
          <p className="text-sm text-gray-600">학생부가 없어도 괜찮습니다. 실습, 프로젝트, 독서, 아르바이트, 봉사, 자격증, 학교 밖 학습 등 무엇이든 한 줄로.</p>
          {activities.map((a, i) => (
            <input
              key={i}
              value={a}
              onChange={(e) => setActivities(activities.map((x, j) => (j === i ? e.target.value.slice(0, 300) : x)))}
              placeholder={`활동 ${i + 1}`}
              className="w-full rounded border px-3 py-2 text-sm"
            />
          ))}
          {activities.length < 5 && (
            <button type="button" onClick={() => setActivities([...activities, ""])} className="text-sm text-blue-700">
              + 활동 추가
            </button>
          )}
          <label className="block text-sm">
            <span className="font-medium">유형별 추가 정보</span>
            <textarea value={notes} onChange={(e) => setNotes(e.target.value.slice(0, 600))} rows={3} placeholder={profileCode ? NOTES_HINT[profileCode as ProfileCode] : ""} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <div className="flex gap-2">
            <button type="button" onClick={() => setStep(1)} className="rounded border px-4 py-2">
              이전
            </button>
            <button type="button" onClick={() => setStep(3)} className="rounded bg-black px-5 py-2 text-white">
              다음
            </button>
          </div>
        </section>
      )}

      {step === 3 && (
        <section className="mt-6 space-y-4">
          <h2 className="font-medium">예상질문 만들기</h2>
          <dl className="rounded border bg-gray-50 p-3 text-sm">
            <div className="flex gap-2">
              <dt className="w-24 text-gray-500">유형</dt>
              <dd>{profiles.find((p) => p.code === profileCode)?.label}</dd>
            </div>
            <div className="flex gap-2">
              <dt className="w-24 text-gray-500">대학·전형</dt>
              <dd>
                {universities.find((u) => u.code === univCode)?.name ?? "미정"} {admissionName} {unit}
              </dd>
            </div>
            <div className="flex gap-2">
              <dt className="w-24 text-gray-500">활동</dt>
              <dd>{filledActivities.length}개</dd>
            </div>
          </dl>
          <p className="text-xs text-gray-500">서버로 보내는 것: 유형, 대학·전형·학과, 활동 한 줄 요약, 추가 정보. 출생 연도는 보내지 않습니다.</p>
          {turnstile.element}
          {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}
          <div className="flex gap-2">
            <button type="button" onClick={() => setStep(2)} className="rounded border px-4 py-2" disabled={busy}>
              이전
            </button>
            <button type="button" onClick={submit} disabled={busy} className="rounded bg-black px-5 py-2 text-white disabled:opacity-40">
              {busy ? "만드는 중… (최대 1분)" : "예상질문 15개 만들기"}
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
