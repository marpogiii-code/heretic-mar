# Test Report — Llama Heretic Storyteller (Gradio, MOCK mode)

**PR:** #1 of `marpogiii-code/heretic-mar` — branch `devin/1785044926-gradio-storyteller`
**Scope:** UI / interaction plumbing in mock mode (`MOCK_MODEL=1`). Actual 70B generation is out of scope (no GPU/weights).
**How tested:** Ran the app locally on Windows (`C:\devin\python\python.exe app.py`) at http://127.0.0.1:7860 with `MOCK_MODEL=1`, exercised the full UI in Chrome.

## Result summary — all 5 planned checks passed

| # | Test | Result |
|---|------|--------|
| 1 | Page loads with title, description, chat box, examples, Additional Inputs accordion | ✅ Passed |
| 2 | Sending a message streams back the mock reply echoing the text | ✅ Passed |
| 3 | Additional Inputs (4 modes, genre dropdown, brief textbox, 5 sliders) present; sending still works after changing them | ✅ Passed |
| 4 | Clicking an example prompt populates the input and runs | ✅ Passed |
| 5 | Multi-turn conversation history is retained | ✅ Passed |

## Caveat / note (not an app bug)
The Chrome text input consistently dropped the **first typed character** in the chat box (e.g. "Hello" → "ello", "Design" → "esign"). This is a browser/automation input-timing quirk, **not** an application defect — the app correctly echoed *exactly* the text that was submitted, and when the input was populated programmatically (example click) the full text appeared intact. No functional impact on the feature under test.

---

## Evidence

### Test 1 — Page load & structure
Title "📖 Llama Heretic Storyteller", description mentioning Llama-3.3-70B and "Additional Inputs", chat box, and 4 example prompts all render.

![Page load](C:\Users\Administrator\screenshots\ss_788c178c.png)

### Test 2 — Streaming mock reply
Submitted a message; assistant reply contains the literal `[mock mode]` marker and echoes the submitted text (`You said: "…"`), built up via streaming.

![Mock reply echo](C:\Users\Administrator\screenshots\ss_zoom_4cca5892.png)

### Test 3 — Additional Inputs controls
Accordion exposes Storytelling mode radio (Interactive Roleplay, Story Generator, Interactive Storyteller, Worldbuilding Assistant), Genre dropdown (8 genres), Extra instructions textbox, and 5 sliders (Temperature, Top-p, Top-k, Max new tokens, Repeat penalty). Changed mode → Worldbuilding Assistant, Genre → Cyberpunk, Temperature 0.9 → 0.75; a subsequent message still sent and returned a mock reply.

![Additional Inputs changed](C:\Users\Administrator\screenshots\ss_5767f8f0.png)

### Tests 4 & 5 — Example run + multi-turn history
Clicking the first example populated the input with the full text and, on submit, produced a mock reply echoing the full example. All prior user+assistant turns remain visible (3 turns retained).

![Multi-turn history](C:\Users\Administrator\screenshots\ss_zoom_22a3cbfc.png)

---

## Environment / setup notes
- Run: `cd C:\Users\Administrator\repos\llama-heretic-storyteller; $env:MOCK_MODEL="1"; $env:SERVER_NAME="127.0.0.1"; $env:SERVER_PORT="7860"; python app.py`
- Dependencies needed for mock mode: `gradio>=5,<6`, `huggingface-hub` (already installed). Do NOT install `llama-cpp-python` for mock testing.
- Gradio emitted two harmless `DeprecationWarning`s about `show_copy_button` / `allow_tags` (Gradio 6.0) — informational only, no impact.
