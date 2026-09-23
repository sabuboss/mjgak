import { guarded, json } from "@/lib/security/guard";
import { generateQuestions } from "@/lib/llm/generate";
import { ApplicantInput } from "@/lib/llm/schemas";

export const runtime = "nodejs";
export const maxDuration = 90; // 생성 30~60초 × 1.5 (A8)

export async function POST(req: Request) {
  return guarded(req, "generate", ApplicantInput, async (input) => {
    try {
      const out = await generateQuestions(input);
      return json(out);
    } catch (e) {
      console.error("[generate]", (e as Error).message); // 입력 내용은 로그에 남기지 않는다 (F1)
      return json({ error: "generation_failed" }, 502);
    }
  });
}
