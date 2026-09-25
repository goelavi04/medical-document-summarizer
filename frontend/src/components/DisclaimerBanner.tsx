export function DisclaimerBanner() {
  return (
    <div className="border-b border-caution-100 bg-caution-50 px-6 py-2.5">
      <div className="mx-auto flex max-w-7xl items-start gap-2 text-[13px] leading-snug text-caution-700">
        <svg className="mt-0.5 h-3.5 w-3.5 flex-none" viewBox="0 0 16 16" fill="currentColor" aria-hidden>
          <path d="M8 1.5 15 14H1L8 1.5Zm0 4.25a.75.75 0 0 0-.75.75v3a.75.75 0 0 0 1.5 0v-3A.75.75 0 0 0 8 5.75Zm0 6.25a.9.9 0 1 0 0-1.8.9.9 0 0 0 0 1.8Z" />
        </svg>
        <p>
          <strong className="font-semibold">Not a substitute for professional medical advice.</strong> This
          tool is a research prototype built for demonstration purposes. Both outputs are AI-generated —
          verify against the source document and clinical judgment before relying on them for any care
          decision.
        </p>
      </div>
    </div>
  );
}
