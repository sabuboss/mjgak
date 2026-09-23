import { guarded, json } from "@/lib/security/guard";
import { giveFeedback } from "@/lib/llm/feedback";
import { FeedbackInput } from "@/lib/llm/schemas";

export const runtime = "nodejs";
export const maxDuration = 60;

export async function POST(req: Request) {
  return guarded(req, "feedback", FeedbackInput, async (input) => {
    try {
      const out = await giveFeedback(input);
      return json(out);
    } catch (e) {
      console.error("[feedback]", (e as Error).message); // 답변 원문은 로그에 남기지 않는다 (F1)
      return json({ error: "feedback_failed" }, 502);
    }
  });
}
