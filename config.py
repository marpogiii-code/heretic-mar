"""Configuration for the Llama Heretic storyteller app.

All values can be overridden via environment variables so the same code runs
on a laptop (CPU), a workstation, or a GPU server without edits.
"""

import os


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return float(value)


# Hugging Face repo that hosts the GGUF weights and the quant we want.
MODEL_REPO = os.environ.get(
    "MODEL_REPO", "mradermacher/Llama-3.3-70B-Instruct-heretic-v2-i1-GGUF"
)
# Glob pattern selecting the quant file(s). Large quants are split by
# mradermacher into multiple parts; the wildcard downloads every part and
# llama.cpp stitches them back together.
MODEL_FILE_PATTERN = os.environ.get("MODEL_FILE_PATTERN", "*i1-Q5_K_M*.gguf")

# Where downloaded weights are cached. Defaults to the HF cache.
MODEL_CACHE_DIR = os.environ.get("MODEL_CACHE_DIR") or None

# Runtime tuning.
N_CTX = _env_int("N_CTX", 8192)
N_GPU_LAYERS = _env_int("N_GPU_LAYERS", -1)  # -1 = offload everything to GPU
N_THREADS = _env_int("N_THREADS", os.cpu_count() or 8)
N_BATCH = _env_int("N_BATCH", 512)

# Default sampling parameters (exposed as sliders in the UI).
DEFAULT_TEMPERATURE = _env_float("DEFAULT_TEMPERATURE", 0.9)
DEFAULT_TOP_P = _env_float("DEFAULT_TOP_P", 0.95)
DEFAULT_TOP_K = _env_int("DEFAULT_TOP_K", 60)
DEFAULT_MAX_TOKENS = _env_int("DEFAULT_MAX_TOKENS", 768)
DEFAULT_REPEAT_PENALTY = _env_float("DEFAULT_REPEAT_PENALTY", 1.1)

# Set to "1" to skip loading the real model and use a canned echo backend.
# Handy for developing/testing the UI without ~48 GB of weights.
MOCK_MODEL = os.environ.get("MOCK_MODEL", "0") == "1"

# Force the UI into dark mode on load (users can still switch via ?__theme=).
FORCE_DARK = os.environ.get("FORCE_DARK", "0") == "1"

# Gradio server settings.
SERVER_NAME = os.environ.get("SERVER_NAME", "0.0.0.0")
SERVER_PORT = _env_int("SERVER_PORT", 7860)
SHARE = os.environ.get("SHARE", "0") == "1"
