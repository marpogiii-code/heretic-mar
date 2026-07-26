"""Model backend: loads the GGUF Llama model and streams chat completions.

The heavy `llama_cpp` import is deferred until the model is actually loaded so
that the module can be imported (for tests / mock mode) on machines without the
native library or the weights.
"""

from __future__ import annotations

import threading
from typing import Iterator

import config


class StorytellerModel:
    """Thin wrapper around a llama.cpp model exposing a streaming chat API."""

    def __init__(self) -> None:
        self._llm = None
        self._lock = threading.Lock()

    @property
    def loaded(self) -> bool:
        return self._llm is not None

    def load(self) -> None:
        """Download (if needed) and load the GGUF weights."""
        if config.MOCK_MODEL:
            return
        if self._llm is not None:
            return

        from llama_cpp import Llama

        self._llm = Llama.from_pretrained(
            repo_id=config.MODEL_REPO,
            filename=config.MODEL_FILE_PATTERN,
            cache_dir=config.MODEL_CACHE_DIR,
            n_ctx=config.N_CTX,
            n_gpu_layers=config.N_GPU_LAYERS,
            n_threads=config.N_THREADS,
            n_batch=config.N_BATCH,
            verbose=False,
        )

    def stream_chat(
        self,
        messages: list[dict],
        temperature: float,
        top_p: float,
        top_k: int,
        max_tokens: int,
        repeat_penalty: float,
    ) -> Iterator[str]:
        """Yield generated text deltas for the given chat `messages`."""
        if config.MOCK_MODEL:
            yield from self._mock_stream(messages)
            return

        if self._llm is None:
            self.load()

        with self._lock:
            stream = self._llm.create_chat_completion(
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_tokens=max_tokens,
                repeat_penalty=repeat_penalty,
                stream=True,
            )
            for chunk in stream:
                delta = chunk["choices"][0]["delta"]
                piece = delta.get("content")
                if piece:
                    yield piece

    @staticmethod
    def _mock_stream(messages: list[dict]) -> Iterator[str]:
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        reply = (
            "*[mock mode]* The tavern falls silent as your words hang in the "
            f"air. You said: \u201c{last_user}\u201d. The story continues..."
        )
        for word in reply.split(" "):
            yield word + " "


# Single shared instance for the app.
MODEL = StorytellerModel()
