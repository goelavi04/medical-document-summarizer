import { SAMPLE_DOCUMENTS } from "../sampleDocuments";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

export function DocumentInputPanel({ value, onChange, onSubmit, isLoading }: Props) {
  const wordCount = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <section className="flex h-full flex-col rounded-md border border-ink-200 bg-white shadow-panel">
      <div className="flex items-center justify-between border-b border-ink-100 px-4 py-3">
        <h2 className="text-[13px] font-semibold uppercase tracking-wide text-ink-600">Source Document</h2>
        <div className="flex gap-1.5">
          {SAMPLE_DOCUMENTS.map((sample) => (
            <button
              key={sample.label}
              type="button"
              onClick={() => onChange(sample.text)}
              className="rounded border border-ink-200 px-2 py-1 text-xs text-ink-600 transition hover:border-accent-500 hover:text-accent-700"
            >
              {sample.label}
            </button>
          ))}
        </div>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste a clinical note, discharge summary, or research abstract…"
        className="min-h-[320px] flex-1 resize-none border-0 px-4 py-3 font-mono text-[13px] leading-relaxed text-ink-800 outline-none placeholder:text-ink-400 placeholder:font-sans"
        spellCheck={false}
      />

      <div className="flex items-center justify-between border-t border-ink-100 px-4 py-3">
        <span className="text-xs text-ink-500">
          {wordCount.toLocaleString()} word{wordCount === 1 ? "" : "s"}
        </span>
        <button
          type="button"
          onClick={onSubmit}
          disabled={isLoading || value.trim().length < 20}
          className="inline-flex items-center gap-2 rounded bg-accent-700 px-4 py-2 text-sm font-medium text-white transition hover:bg-accent-800 disabled:cursor-not-allowed disabled:bg-ink-300"
        >
          {isLoading ? (
            <>
              <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              Processing…
            </>
          ) : (
            "Summarize document"
          )}
        </button>
      </div>
    </section>
  );
}
