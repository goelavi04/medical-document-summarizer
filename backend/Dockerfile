# Backend image for Hugging Face Spaces (Docker SDK) or any other container host
# (Render, Railway, etc.). Spaces expects the app to listen on port 7860.
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install the CPU-only torch wheel first (the default PyPI wheel bundles CUDA runtime
# libraries that are dead weight — and a multi-GB image bloat — on a CPU-only host like a
# free HF Spaces / Render / Railway tier). Everything else then installs against it.
RUN pip install --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
# If you're bundling the adapter into the image instead of pulling it from the HF Hub at
# runtime, uncomment the next line and set ADAPTER_PATH=models/adapter in your env.
# COPY models ./models

ENV HOST=0.0.0.0
ENV PORT=7860
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
