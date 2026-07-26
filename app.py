"""Gradio app: roleplay / story generator / storyteller powered by
mradermacher/Llama-3.3-70B-Instruct-heretic-v2-i1-GGUF (Q5_K_M)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr

import config
from model_backend import MODEL
from prompts import GENRE_HINTS, MODES, build_system_prompt


def _to_llama_messages(system_prompt: str, history: list[dict]) -> list[dict]:
    messages = [{"role": "system", "content": system_prompt}]
    for turn in history:
        role = turn.get("role")
        content = turn.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    return messages


def respond(
    message: str,
    history: list[dict],
    mode: str,
    genre: str,
    custom_system: str,
    temperature: float,
    top_p: float,
    top_k: float,
    max_tokens: float,
    repeat_penalty: float,
):
    """Streaming chat handler for the Gradio ChatInterface."""
    if not message or not message.strip():
        yield ""
        return

    system_prompt = build_system_prompt(mode, genre, custom_system)
    convo = _to_llama_messages(system_prompt, history)
    convo.append({"role": "user", "content": message})

    partial = ""
    for piece in MODEL.stream_chat(
        convo,
        temperature=temperature,
        top_p=top_p,
        top_k=int(top_k),
        max_tokens=int(max_tokens),
        repeat_penalty=repeat_penalty,
    ):
        partial += piece
        yield partial


def build_demo() -> gr.Blocks:
    mode = gr.Radio(
        choices=list(MODES.keys()),
        value=next(iter(MODES.keys())),
        label="Storytelling mode",
    )
    genre = gr.Dropdown(
        choices=list(GENRE_HINTS.keys()),
        value="(none)",
        label="Genre",
    )
    custom_system = gr.Textbox(
        label="Extra instructions / character brief (optional)",
        placeholder="e.g. Play a cunning rogue named Sable in a rain-soaked port city.",
        lines=3,
    )
    temperature = gr.Slider(
        0.0, 2.0, value=config.DEFAULT_TEMPERATURE, step=0.05, label="Temperature"
    )
    top_p = gr.Slider(0.0, 1.0, value=config.DEFAULT_TOP_P, step=0.01, label="Top-p")
    top_k = gr.Slider(0, 200, value=config.DEFAULT_TOP_K, step=1, label="Top-k")
    max_tokens = gr.Slider(
        64, 4096, value=config.DEFAULT_MAX_TOKENS, step=32, label="Max new tokens"
    )
    repeat_penalty = gr.Slider(
        1.0, 1.5, value=config.DEFAULT_REPEAT_PENALTY, step=0.01, label="Repeat penalty"
    )

    description = (
        "Roleplay, generate stories, and play interactive branching tales, "
        "powered by **Llama-3.3-70B-Instruct-heretic-v2** (Q5_K_M GGUF). "
        "Open **Additional Inputs** below to pick a mode, genre, and tune sampling."
    )

    def _example(message: str, ex_mode: str, ex_genre: str) -> list:
        return [
            message,
            ex_mode,
            ex_genre,
            "",
            config.DEFAULT_TEMPERATURE,
            config.DEFAULT_TOP_P,
            config.DEFAULT_TOP_K,
            config.DEFAULT_MAX_TOKENS,
            config.DEFAULT_REPEAT_PENALTY,
        ]

    # When FORCE_DARK is set, redirect to the dark theme on first load.
    force_dark_js = """
    () => {
        const url = new URL(window.location);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.replace(url.href);
        }
    }
    """

    demo = gr.ChatInterface(
        fn=respond,
        type="messages",
        title="\U0001F4D6 Llama Heretic Storyteller",
        description=description,
        theme=gr.themes.Soft(primary_hue="purple"),
        js=force_dark_js if config.FORCE_DARK else None,
        chatbot=gr.Chatbot(type="messages", height=560, show_copy_button=True),
        additional_inputs=[
            mode,
            genre,
            custom_system,
            temperature,
            top_p,
            top_k,
            max_tokens,
            repeat_penalty,
        ],
        examples=[
            _example("You push open the tavern door. Describe what I see.", "Interactive Roleplay", "High Fantasy"),
            _example("Write a short story about a lighthouse keeper who finds a door in the sea.", "Story Generator", "Mystery / Noir"),
            _example("Begin an adventure where I wake up on a derelict spaceship.", "Interactive Storyteller", "Science Fiction"),
            _example("Help me design a rain-soaked cyberpunk port city and its factions.", "Worldbuilding Assistant", "Cyberpunk"),
        ],
    )
    return demo


def main() -> None:
    if not config.MOCK_MODEL:
        print("Loading model (this downloads ~48 GB on first run)...")
        MODEL.load()
        print("Model ready.")
    demo = build_demo()
    demo.queue().launch(
        server_name=config.SERVER_NAME,
        server_port=config.SERVER_PORT,
        share=config.SHARE,
    )


if __name__ == "__main__":
    main()
