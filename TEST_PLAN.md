# Test Plan — Llama Heretic Storyteller (MOCK mode)

App: Gradio ChatInterface at http://127.0.0.1:7860 (running with MOCK_MODEL=1).
Mock backend (model_backend.py:80-91) echoes: `*[mock mode]* The tavern falls silent as your words hang in the air. You said: "<your text>". The story continues...`, streamed word-by-word.

## Test 1 — Page load & structure
- Load http://127.0.0.1:7860.
- PASS if: title "📖 Llama Heretic Storyteller" visible; description mentioning Llama-3.3-70B; chat message box + textbox present; 4 example prompts visible; "Additional Inputs" accordion present (collapsed by default).
- FAIL if: any of the above missing or page errors.

## Test 2 — Send message streams mock reply
- Type `Hello there, storyteller` in the input, press Enter/Submit.
- PASS if: assistant reply appears containing literal `[mock mode]` AND echoes `You said: "Hello there, storyteller"`. Observe streaming (text builds up word-by-word).
- FAIL if: no reply, no `[mock mode]`, wrong echo, or error.

## Test 3 — Additional Inputs controls & don't break sending
- Expand "Additional Inputs" accordion.
- PASS if visible: Storytelling mode radio with 4 options (Interactive Roleplay, Story Generator, Interactive Storyteller, Worldbuilding Assistant); Genre dropdown; "Extra instructions / character brief" textbox; sliders Temperature, Top-p, Top-k, Max new tokens, Repeat penalty.
- Change mode to "Worldbuilding Assistant", pick a Genre (e.g. Cyberpunk), drag Temperature slider.
- Send a new message `Design a neon city`.
- PASS if: reply still returns with `[mock mode]` and echoes `You said: "Design a neon city"` (no error after changing inputs).

## Test 4 — Example prompt populates/runs
- Click the first example ("You push open the tavern door...").
- PASS if: the example text populates the input and/or runs, producing a mock reply echoing the example text.
- FAIL if: nothing happens or error.

## Test 5 — Multi-turn history retained
- After Test 4 (or Test 2/3), send another message `What happens next?`.
- PASS if: chat retains all prior user+assistant turns AND new reply echoes `You said: "What happens next?"`. Prior turns still visible above.
- FAIL if: history cleared or prior turns lost.
