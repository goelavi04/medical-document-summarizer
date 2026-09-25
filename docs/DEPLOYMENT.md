# Deployment

## Frontend — Vercel

Plan: standard Vite/React static deployment. **Free tier is sufficient** — no paid Vercel plan
required for this project's traffic/build needs.

Blocker: this environment has no authenticated Vercel session and the Vercel CLI isn't
installed, and Vercel's OAuth login flow can't run in a non-interactive session. To finish this
step, either:
- Run it yourself: `npm i -g vercel && cd frontend && vercel login && vercel --prod`, or
- Give me a Vercel token (`vercel login` locally, then `vercel whoami --token=<token>` to
  confirm) and I'll run the deploy non-interactively.

Set `VITE_API_BASE_URL` as a Vercel project environment variable pointing at wherever the
backend ends up (see below) before the production build.

## Backend — Hugging Face Spaces (Docker SDK)

**Recommended over Render/Railway.** Reasoning: the backend needs to hold a ~7.6GB model in
memory and do CPU inference; Render's and Railway's free tiers cap around 512MB-1GB RAM, which
is not enough. HF Spaces' free CPU tier gives 16GB RAM / 2 vCPU, which fits (slowly — see
below).

**Free tier works, with a real caveat: CPU inference on a 3.8B model is slow.** Expect roughly
tens of seconds to a few minutes per `/summarize` call on the free CPU tier, depending on
document length and chunking. If you want production-realistic latency, HF Spaces' paid GPU
tiers (T4 small starts around $0.40/hr, billed while the Space is running) would cut this to
seconds — **flagging this before committing to it, since it's a paid tier**; I have not enabled
this and won't without you confirming.

Steps (needs your HF account):
1. Create a Space (Docker SDK) at huggingface.co/new-space.
2. Either push the adapter to a separate HF model repo and set `ADAPTER_PATH` to that repo id
   (recommended — keeps the Space's own git repo small), or bundle it into the Space via the
   commented-out `COPY models ./models` line in `backend/Dockerfile`.
3. Push `backend/` (the Dockerfile, `app/`, `requirements.txt`) to the Space's git remote, or
   connect the Space to this GitHub repo's `backend/` subfolder.
4. Set Space secrets: `GROQ_API_KEY`, `ADAPTER_PATH`.

I can't do this from here — it needs your Hugging Face account. Give me a HF write token
(`huggingface-cli login` locally, or a token from huggingface.co/settings/tokens) if you'd like
me to run the `huggingface_hub` Space-creation/push calls non-interactively instead.

## GitHub

Repo: created via the already-authenticated `gh` CLI (account `goelavi04`), public, named
`medical-document-summarizer`. No blocker here.

## What actually needs a paid tier, summarized

| Component | Free tier viable? | Note |
|---|---|---|
| Frontend (Vercel) | Yes | No paid plan needed |
| Backend (HF Spaces, CPU) | Yes | Works, but slow per-request (CPU inference on a 3.8B model) |
| Backend (HF Spaces, GPU) | **No — paid** | Would need explicit confirmation before enabling |
| Training (Colab/Kaggle free GPU) | Yes | Session time limits mean the notebook uses a deliberately small data subset |
