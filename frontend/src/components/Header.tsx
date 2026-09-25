export function Header() {
  return (
    <header className="border-b border-ink-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3.5">
        <div className="flex items-baseline gap-3">
          <span className="text-[17px] font-semibold tracking-tight text-ink-900">Synopsis</span>
          <span className="hidden text-sm text-ink-500 sm:inline">Clinical Document Summarization</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-ink-500">
          <span className="inline-flex h-1.5 w-1.5 rounded-full bg-accent-500" aria-hidden />
          Research prototype
        </div>
      </div>
    </header>
  );
}
