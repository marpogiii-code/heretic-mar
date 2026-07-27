# Llama Heretic Storyteller

A Gradio web app for **roleplay, story generation, and interactive storytelling**,
powered by [`mradermacher/Llama-3.3-70B-Instruct-heretic-v2-i1-GGUF`](https://huggingface.co/mradermacher/Llama-3.3-70B-Instruct-heretic-v2-i1-GGUF)
(the `i1-Q5_K_M` quant) running locally via [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python).

## Features

- **Four modes** (selectable in *Additional Inputs*):
  - **Interactive Roleplay** – stay-in-character GM/roleplay partner.
  - **Story Generator** – writes a complete, structured short story from a premise.
  - **Interactive Storyteller** – branching narration with numbered choices each turn.
  - **Worldbuilding Assistant** – invent settings, cultures, characters, and lore.
- **Genre presets** (High Fantasy, Sci-Fi, Cyberpunk, Horror, Noir, Romance, Historical, Grimdark).
- **Custom character/scene brief** free-text box.
- **Streaming responses** with live token-by-token output.
- **Sampling controls**: temperature, top-p, top-k, max tokens, repeat penalty.

## Requirements

- Python 3.10+
- Enough RAM/VRAM for the `Q5_K_M` quant of a 70B model (**~48 GB**). A GPU with
  offload (`N_GPU_LAYERS=-1`) is strongly recommended; CPU-only works but is slow.

## Install

```bash
pip install -r requirements.txt
```

### GPU (CUDA) acceleration

Install a GPU build of `llama-cpp-python` **before** `requirements.txt`. The
simplest, most reliable way is a **prebuilt CUDA wheel** (no local compile):

```bash
# Check your CUDA version first (top-right of `nvidia-smi`), then pick a tag <= it.
pip install llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
# tags: cu121 / cu122 / cu123 / cu124
pip install -r requirements.txt
```

The prebuilt wheel bundles its own CUDA runtime, so `nvcc`/host-compiler
versions don't matter.

<details>
<summary>Building from source instead</summary>

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
```

If the CUDA compile fails with `parameter packs not expanded with '...'` in
`std_function.h`, your `nvcc` (CUDA 11.x) is incompatible with GCC 11 — point it
at an older host compiler:

```bash
sudo apt-get install -y g++-10
CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_HOST_COMPILER=/usr/bin/g++-10" \
  pip install llama-cpp-python --force-reinstall --no-cache-dir
```
</details>

## Run

```bash
python app.py
```
## Hint
```
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
pip install -r requirements.txt
```
Then open http://localhost:7860. On first launch the model weights (~48 GB) are
downloaded from Hugging Face and cached.

### Develop the UI without the weights

```bash
MOCK_MODEL=1 python app.py
```

Mock mode skips the download/load and uses a canned echo backend so you can work
on the interface instantly.

### Dark mode

Append `?__theme=dark` to the URL (e.g. `http://localhost:7860/?__theme=dark`),
or launch with `FORCE_DARK=1` to default to dark mode.

## Configuration (environment variables)

| Variable | Default | Description |
| --- | --- | --- |
| `MODEL_REPO` | `mradermacher/Llama-3.3-70B-Instruct-heretic-v2-i1-GGUF` | HF repo with the GGUF weights |
| `MODEL_FILE_PATTERN` | `*i1-Q5_K_M*.gguf` | Glob for the quant file(s); split parts are downloaded automatically |
| `MODEL_CACHE_DIR` | HF default | Where weights are cached |
| `N_CTX` | `8192` | Context window |
| `N_GPU_LAYERS` | `-1` | Layers to offload to GPU (`-1` = all) |
| `N_THREADS` | CPU count | CPU threads |
| `N_BATCH` | `512` | Batch size |
| `MOCK_MODEL` | `0` | `1` = skip model, use echo backend |
| `FORCE_DARK` | `0` | `1` = launch the UI in dark mode |
| `SERVER_NAME` / `SERVER_PORT` | `0.0.0.0` / `7860` | Gradio bind address/port |
| `SHARE` | `0` | `1` = create a public Gradio share link |

Plus `DEFAULT_TEMPERATURE`, `DEFAULT_TOP_P`, `DEFAULT_TOP_K`, `DEFAULT_MAX_TOKENS`,
`DEFAULT_REPEAT_PENALTY` to change the initial slider values.

## Notes

This model is an "abliterated"/uncensored fine-tune. Use responsibly and in
accordance with the base model's license and your local laws.
