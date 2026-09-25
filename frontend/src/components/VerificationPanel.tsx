import type { VerificationMetadata } from "../types";

interface Props {
  verification: VerificationMetadata;
  regenerationCount: number;
}

export function VerificationPanel({ verification, regenerationCount }: Props) {
  const { passed, coverage, source_entity_count, matched_entities, missing_entities, threshold } = verification;
  const pct = Math.round(coverage * 100);

  return (
    <div className="rounded-md border border-ink-200 bg-white shadow-panel">
      <div className="flex items-center justify-between border-b border-ink-100 px-4 py-3">
        <h3 className="text-[13px] font-semibold uppercase tracking-wide text-ink-600">Entity Coverage Check</h3>
        <StatusPill passed={passed} />
      </div>

      <div className="space-y-3 px-4 py-3.5">
        {source_entity_count === 0 ? (
          <p className="text-sm text-ink-500">No clinical entities were detected in the source document to check against.</p>
        ) : (
          <>
            <div>
              <div className="mb-1 flex items-center justify-between text-xs text-ink-500">
                <span>
                  {matched_entities.length} of {source_entity_count} source entities found in summary
                </span>
                <span className="font-mono">
                  {pct}% <span className="text-ink-400">(threshold {Math.round(threshold * 100)}%)</span>
                </span>
              </div>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-ink-100">
                <div
                  className={`h-full rounded-full ${passed ? "bg-accent-500" : "bg-critical-500"}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>

            {missing_entities.length > 0 && (
              <div>
                <p className="mb-1.5 text-xs font-medium text-ink-500">Not found in summary</p>
                <div className="flex flex-wrap gap-1.5">
                  {missing_entities.map((ent) => (
                    <span
                      key={ent}
                      className="rounded border border-critical-100 bg-critical-50 px-1.5 py-0.5 text-xs text-critical-700"
                    >
                      {ent}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {matched_entities.length > 0 && (
              <div>
                <p className="mb-1.5 text-xs font-medium text-ink-500">Confirmed in summary</p>
                <div className="flex flex-wrap gap-1.5">
                  {matched_entities.map((ent) => (
                    <span
                      key={ent}
                      className="rounded border border-accent-100 bg-accent-50 px-1.5 py-0.5 text-xs text-accent-800"
                    >
                      {ent}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {regenerationCount > 0 && (
          <p className="border-t border-ink-100 pt-2.5 text-xs text-ink-500">
            Summary was regenerated {regenerationCount}× after initial coverage came in below threshold.
          </p>
        )}
      </div>
    </div>
  );
}

function StatusPill({ passed }: { passed: boolean }) {
  return (
    <span
      className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${
        passed ? "bg-accent-100 text-accent-800" : "bg-critical-100 text-critical-700"
      }`}
    >
      {passed ? "Passed" : "Flagged"}
    </span>
  );
}
