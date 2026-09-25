import os
from dotenv import load_dotenv

load_dotenv()

# --- Summarizer model ---
BASE_MODEL = os.environ.get("BASE_MODEL", "microsoft/Phi-3-mini-4k-instruct")
# Either a local path (e.g. "models/adapter") or a Hugging Face Hub repo id
# (e.g. "yourname/phi3-mini-pubmed-qlora-adapter"). Must exist — there is no
# silent fallback to the un-adapted base model at request time.
ADAPTER_PATH = os.environ.get("ADAPTER_PATH", "models/adapter")

MAX_SOURCE_TOKENS = int(os.environ.get("MAX_SOURCE_TOKENS", 1200))
MAX_TARGET_TOKENS = int(os.environ.get("MAX_TARGET_TOKENS", 300))
MAX_SEQ_LEN = int(os.environ.get("MAX_SEQ_LEN", 1792))

SUMMARIZER_SYSTEM_PROMPT = (
    "You are a clinical documentation assistant. Read the biomedical article and write a "
    "precise, technical summary suitable for a clinician: preserve key diagnoses, procedures, "
    "medications, dosages, and findings. Do not add information that is not in the source."
)

SUMMARIZER_SYSTEM_PROMPT_STRICT = (
    SUMMARIZER_SYSTEM_PROMPT
    + " Your previous attempt omitted important named entities (diagnoses, medications, "
    "procedures, or findings) that appear in the source. Be exhaustive: explicitly name every "
    "diagnosis, medication (with dosage if given), procedure, and key finding mentioned in the "
    "source text."
)

# --- Verification agent ---
NER_MODEL = os.environ.get("NER_MODEL", "d4data/biomedical-ner-all")
VERIFICATION_COVERAGE_THRESHOLD = float(os.environ.get("VERIFICATION_COVERAGE_THRESHOLD", 0.5))
VERIFICATION_MAX_ENTITY_CHARS = int(os.environ.get("VERIFICATION_MAX_ENTITY_CHARS", 4000))
MAX_REGENERATION_ATTEMPTS = int(os.environ.get("MAX_REGENERATION_ATTEMPTS", 1))

# --- Patient explainer agent ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

EXPLAINER_SYSTEM_PROMPT = (
    "You explain medical summaries to patients and family members with no medical background. "
    "Rewrite the technical summary in plain, everyday language at roughly a 7th-8th grade "
    "reading level. Define any medical term you must use, in parentheses, the first time it "
    "appears. Keep the same facts as the technical summary — do not add, remove, or soften "
    "any diagnosis, medication, or instruction. Do not give new medical advice. Write 3-6 short "
    "sentences or a short bulleted list, whichever reads more clearly for this content."
)
