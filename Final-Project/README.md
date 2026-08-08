# AI Study Notes Summarizer

**Author:** Raj Golder ([raj-codelabs](https://github.com/raj-codelabs) on GitHub, `rajgolder` on edX)

#### Video Demo: https://youtu.be/cSR-vhMtHsI

#### Description:

The AI Study Notes Summarizer is a Flask web application that turns long, unstructured study notes into concise, revision-ready summaries using a large language model. The workflow is intentionally simple: a student pastes their notes into a text area (or uploads a `.txt` file), selects one of seven AI providers, pastes their own API key, chooses a summary length — Short, Medium, or Detailed — and clicks Generate. The application validates every field, builds a provider-specific request, calls the provider's REST API, and presents the result on a dedicated page where it can be downloaded as `summary.txt` or discarded with a Start Over button.

The application was built as my Harvard CS50x final project and is designed to demonstrate the course's curriculum end to end: variables, conditionals, loops, functions, file I/O, lists, dictionaries, strings, exceptions, modules, Flask, HTML/CSS, and third-party REST API integration. It is deliberately narrow in scope — a single, well-defined job performed well — and every module exists to serve that job. Allowing users to bring their own API key was a deliberate choice: it avoids server-side key management, billing, and storage, and it makes the project instantly usable by anyone with a key from a supported provider.

### File-by-file breakdown

- `app.py` — the Flask application. Defines every route (`GET /`, `POST /`, `/result`, `/download`, `/clear`), validates submitted data, and stores the generated summary server-side.
- `summarizer.py` — the only module that communicates with the outside world. Contains the provider configuration table (endpoint, model, auth style, response extractor), builds the request body for each API style, and maps network and HTTP errors to user-friendly messages.
- `prompts.py` — holds the instruction template for each summary length in one place, so the rest of the application never has to know what the AI is being told.
- `utils.py` — pure helper logic: shared constants, text cleaning, input validation, and uploaded-file reading and decoding.
- `templates/index.html` — the input form (notes, file, provider, key, length). `templates/result.html` — displays the summary with download and restart controls.
- `static/style.css` — responsive styling. `static/script.js` — a live character counter, selected-file display, and a client-side guard against empty submissions.
- `test_project.py` — the pytest suite: validation functions, prompt building, mocked provider calls, and every route.
- `requirements.txt` — Flask, requests, and pytest.

### Technical design decisions

The most important decision was to keep the application stateless and free of a database. A summary only needs to exist between generation and the user moving on, so summaries are held in a small in-memory dictionary keyed by a random identifier. Choosing the server-side store over the session cookie mattered: Flask's default client-side cookie is capped at roughly 4 KB, which a Detailed summary can easily exceed and silently lose.

Modularity was chosen for testability. `summarizer.py`, `prompts.py`, and `utils.py` carry no Flask imports, so all non-routing behavior is testable in isolation; the test suite mocks the provider calls, meaning `pytest` runs with no network access or real API key. Providers are described declaratively in one table (endpoint, model, auth style, extractor) — a pattern I lean on outside this project too, when switching between OpenAI-compatible endpoints in my own local tooling — so adding a provider here is a data-only change, not new logic. Plain `requests` was used instead of provider SDKs to avoid new dependencies and to keep all network behavior in one auditable place.

Security received unusual attention for a course project: API keys are never stored or logged, uploads are restricted to `.txt` files under 1 MB with content capped at 50,000 characters, session cookies are hardened (HttpOnly, SameSite, optional Secure), and every response carries nosniff, X-Frame-Options, and a strict Content-Security-Policy. The interactive debugger is off by default.

### Installation and execution

Requires Python 3.10 or newer. From the project directory:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in a browser. Run the test suite with:

```bash
pytest
```
