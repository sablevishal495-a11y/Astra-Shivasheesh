# Workspace Rules & AI Operational Constraints

## 1. Token Economy ("Caveman" Terse Mode)
- **Extreme Brevity**: Minimize output tokens. Cut all conversational filler, pleasantries, greetings, and post-action commentary.
- **Direct Output**: If code or diff is requested, provide only the code/diff. Explain in 1-2 short sentences only when explicitly requested.
- **Focused Edits**: Make pinpoint edits. Do not rewrite whole files when editing a small block.

## 2. Anti-Overcoding & Anti-Bloat (KISS / YAGNI)
- **Minimum Viable Code**: Write the smallest amount of code that completely solves the task.
- **No Over-Engineering**: If a task requires a 5-line button or simple function, write exactly 5 lines. Never build 40-line frameworks, state wrappers, custom animation engines, or extra div layers unless explicitly asked.
- **Preserve Existing Patterns**: Respect existing architecture (vanilla HTML5, CSS, and JS). Do not inject unrequested external libraries, dependencies, or unnecessary abstractions.

## 3. Grounding & Anti-Hallucination
- **Verify Before Answering**: Never assume file structure, element IDs, class names, or function signatures. Inspect actual files first.
- **No Speculative Imports**: Never invent non-existent packages, DOM selectors, or library APIs.
- **Fail Fast & Clarify**: If critical information is missing, state the exact missing detail in one short question rather than guessing.

## 4. Cybersecurity Guardrails (OWASP Baseline)
- **XSS Prevention**: Never inject unsanitized user inputs into the DOM via `innerHTML` or `document.write`. Always use `textContent` or proper sanitization.
- **Secrets & Credentials**: Never hardcode API keys, passwords, bearer tokens, or sensitive credentials in client-side code.
- **Form & Auth Safety**: Enforce `autocomplete` attributes, proper input types, HTTPS links, and `rel="noopener noreferrer"` on external links.
- **Safe Event Handling**: Validate incoming data formats and sanitize payloads before processing.

## 5. Lean Documentation
- **Minimalist Comments**: Add comments only for complex algorithms, non-obvious business logic, or security considerations.
- **No Obvious Annotations**: Do not write comments describing what the code trivially does (e.g., avoid `// click event listener` or `// set name to John`).
