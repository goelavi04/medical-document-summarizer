import type { PatientExplanation } from "../types";

interface Props {
  explanation: PatientExplanation;
}

export function PatientExplanationCard({ explanation }: Props) {
  const hasError = Boolean(explanation.error);

  return (
    <div className="rounded-md border border-ink-200 bg-white shadow-panel">
      <div className="flex items-center justify-between border-b border-ink-100 px-4 py-3">
        <h3 className="text-[13px] font-semibold uppercase tracking-wide text-ink-600">Patient-Friendly Explanation</h3>
        <span className="rounded-full bg-ink-800 px-2 py-0.5 text-[11px] font-medium text-white">AI-generated</span>
      </div>
      <div className="px-4 py-3.5">
        {hasError ? (
          <p className="text-sm text-caution-700">{explanation.error}</p>
        ) : (
          <p className="whitespace-pre-wrap text-[14px] leading-relaxed text-ink-800">{explanation.text}</p>
        )}
      </div>
      <div className="border-t border-ink-100 bg-ink-50 px-4 py-2">
        <span className="text-[11px] font-medium text-ink-500">
          Generated via prompt-based generation ({explanation.backend}) — not a substitute for talking to your
          care team.
        </span>
      </div>
    </div>
  );
}
