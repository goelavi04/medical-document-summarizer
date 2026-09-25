# Frontend — Synopsis UI

React + TypeScript + Tailwind. Talks to the FastAPI backend's `POST /summarize`.

## Setup

```bash
npm install
cp .env.example .env   # VITE_API_BASE_URL, defaults to http://localhost:8000
npm run dev
```

## Structure

- `src/App.tsx` — page layout and request state
- `src/api.ts` — typed fetch wrapper for the backend
- `src/types.ts` — response types matching the backend's Pydantic models
- `src/components/` — `DocumentInputPanel`, `TechnicalSummaryCard`, `VerificationPanel`,
  `PatientExplanationCard`, `DisclaimerBanner`, `Header`
- `src/sampleDocuments.ts` — synthetic example documents for the sample-document buttons (not
  real patient data)

## Build

```bash
npm run build
```

## Deploy

See [`../docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md).
