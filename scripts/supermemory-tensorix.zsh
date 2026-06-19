#!/usr/bin/env zsh
set -euo pipefail

# Launcher for the self-hosted supermemory-server.
#
# Storage, embeddings, and the graph engine all run locally
# (data -> ~/.supermemory/data). The ONLY thing that leaves the machine is
# the memory-extraction LLM call, which we point at Tensorix (OpenAI-compatible).
# Swap OPENAI_* below to an Ollama endpoint for a fully offline setup.

ENV_FILE="/Users/adityakharbanda/blood_test_analysis/.env.local"

if [[ ! -f "${ENV_FILE}" ]]; then
  print -u2 ".env.local not found at ${ENV_FILE}"
  exit 1
fi

set -a
source "${ENV_FILE}"
set +a

if [[ -z "${TENSORIX_API_KEY:-}" ]]; then
  print -u2 "TENSORIX_API_KEY is not set in ${ENV_FILE}"
  exit 1
fi

# Point supermemory's extraction LLM at Tensorix (OpenAI-compatible /v1).
export OPENAI_BASE_URL="https://api.tensorix.ai/v1"
export OPENAI_API_KEY="${TENSORIX_API_KEY}"
export OPENAI_MODEL="deepseek/deepseek-v4-flash"

# Stable data dir: graph engine + generated sm_ API key + embedding cache.
export SUPERMEMORY_DATA_DIR="${HOME}/.supermemory/data"

# Disable AI SDK instrumentation telemetry (self-hosted binary sends no
# analytics otherwise; this is belt-and-suspenders for sensitive data).
export SUPERMEMORY_DISABLE_TELEMETRY=1

exec "${HOME}/.local/bin/supermemory-server"
