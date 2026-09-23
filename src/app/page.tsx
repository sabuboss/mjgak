import Link from "next/link";

import { WaitlistForm } from "@/components/WaitlistForm";

const TYPES = [
  { code: "VOCATIONAL", label: "특성화고·마이스터고", hint: "진학을 택한 이유, 실습 경험, 기초학력 질문" },
  { code: "GED", label: "검정고시", hint: "자퇴 사유, 자기주도 학습, 학생부 없이 증명하기" },
  { code: "REPEAT", label: "재수·N수", hint: "재도전 이유, 지난 1년의 변화, 성숙도" },
  { code: "OVERSEAS_3", label: "재외국민 3년 특례", hint: "해외 학교 경험, 한국어·적응, 정체성" },
  { code: "OVERSEAS_12", label: "12년 특례·외국인", hint: "한국어 능력, 한국 진학 동기, 영어 면접" },
  { code: "ALTERNATIVE", label: "대안학교", hint: "대안교육의 의미, 교과 보완, 자기주도 프로젝트" },
  { code: "GENERAL", label: "일반고", hint: "학생부 활동 기반 질문과 꼬리질문" },
];

export default function Home() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-14">
      <p className="text-sm font-medium text-emerald-700">면접각 · 무료 베타</p>
      <h1 className="mt-2 text-3xl font-bold leading-tight sm:text-4xl">
        특성화고·검정고시·재수생·해외 출신도
        <br />
        <span className="text-emerald-700">나에게 맞는</span> 면접 준비
      </h1>
      <p className="mt-4 max-w-2xl text-gray-700">
        대학이 공개한 면접 기출문항을 대학·전형·연도별로 정리하고, 지원자 유형에 맞춘 예상질문과 답변 코칭을 제공합니다. 실제 기출과 예상질문은 항상 구분해서
        보여 드리고, 모든 문항에는 대학 입학처 출처 링크가 있습니다.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        <Link href="/onboarding" className="rounded-lg bg-black px-5 py-3 text-white">
          내 유형으로 시작하기
        </Link>
        <Link href="/univ" className="rounded-lg border px-5 py-3">
          대학별 기출 보기
        </Link>
      </div>

      <section className="mt-14">
        <h2 className="text-lg font-semibold">지원자 유형별 준비</h2>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          {TYPES.map((t) => (
            <li key={t.code}>
              <Link href={`/onboarding?type=${t.code}`} className="block rounded-lg border p-4 hover:border-black">
                <p className="font-medium">{t.label}</p>
                <p className="mt-1 text-sm text-gray-600">{t.hint}</p>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-14 rounded-lg border bg-gray-50 p-5 text-sm text-gray-700">
        <h2 className="font-semibold">생기부는 서버에 올라가지 않습니다</h2>
        <p className="mt-2">
          생기부 PDF를 올리더라도 브라우저 안에서만 읽어 활동 요약을 만들고, 원문은 서버로 보내지 않습니다. 답변과 진행 상황도 기본적으로 내 브라우저에만 저장됩니다.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="text-lg font-semibold">정식 오픈 알림</h2>
        <p className="mt-1 text-sm text-gray-600">베타 기간에는 무료입니다. 더 많은 대학과 AI 코칭이 열리면 이메일로 알려 드립니다.</p>
        <div className="mt-3 max-w-md">
          <WaitlistForm />
        </div>
      </section>
    </main>
  );
}
