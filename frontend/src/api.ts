import type { SummarizeResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class ApiRequestError extends Error {}

export async function summarizeDocument(document: string): Promise<SummarizeResponse> {
  const response = await fetch(`${API_BASE_URL}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document }),
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (body?.detail) {
        detail = Array.isArray(body.detail)
          ? body.detail.map((d: { msg?: string }) => d.msg).join("; ")
          : String(body.detail);
      }
    } catch {
      // response body wasn't JSON; keep the generic message
    }
    throw new ApiRequestError(detail);
  }

  return response.json();
}
