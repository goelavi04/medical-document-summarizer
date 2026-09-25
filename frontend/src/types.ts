export interface VerificationMetadata {
  passed: boolean;
  coverage: number;
  source_entity_count: number;
  matched_entities: string[];
  missing_entities: string[];
  threshold: number;
}

export interface PatientExplanation {
  text: string;
  backend: "groq" | "ollama" | "fake" | "none" | string;
  error: string | null;
}

export interface SummarizeResponse {
  doc_type: string;
  token_count: number;
  chunked: boolean;
  technical_summary: string;
  verification: VerificationMetadata;
  regeneration_count: number;
  patient_explanation: PatientExplanation;
  latency_seconds: number;
}

export interface ApiError {
  detail: string;
}
