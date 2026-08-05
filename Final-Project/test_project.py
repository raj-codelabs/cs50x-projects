"""Automated tests for the AI Study Notes Summarizer.

Run with:  pytest

The AI provider calls are mocked, so no network access or real API key
is needed to run this suite.
"""

import io

import pytest

import app as app_module
import prompts
import summarizer
import utils
from summarizer import SummarizerError
from werkzeug.datastructures import FileStorage


# ----------------------------------------------------------------------
# utils.py - clean_text
# ----------------------------------------------------------------------


def test_clean_text_strips_whitespace():
    assert utils.clean_text("   hello   ") == "hello"


def test_clean_text_normalizes_line_endings():
    assert utils.clean_text("a\r\nb\rc") == "a\nb\nc"


def test_clean_text_collapses_blank_lines():
    assert utils.clean_text("a\n\n\n\nb") == "a\n\nb"


# ----------------------------------------------------------------------
# utils.py - validate_notes
# ----------------------------------------------------------------------


def test_validate_notes_empty():
    ok, message = utils.validate_notes("")
    assert not ok
    assert "notes" in message.lower()


def test_validate_notes_too_long():
    ok, message = utils.validate_notes("x" * (utils.MAX_NOTES_LENGTH + 1))
    assert not ok
    assert "too long" in message


def test_validate_notes_valid():
    ok, message = utils.validate_notes("Some valid notes.")
    assert ok
    assert message == ""


# ----------------------------------------------------------------------
# utils.py - validate_api_key / validate_provider / validate_length
# ----------------------------------------------------------------------


def test_validate_api_key_empty():
    ok, message = utils.validate_api_key("")
    assert not ok


def test_validate_api_key_too_short():
    ok, message = utils.validate_api_key("short")
    assert not ok


def test_validate_api_key_valid():
    ok, message = utils.validate_api_key("sk-1234567890123456")
    assert ok


def test_validate_provider():
    assert utils.validate_provider("openai")[0]
    assert utils.validate_provider("bogus")[0] is False


def test_validate_length():
    assert utils.validate_length("medium")[0]
    assert utils.validate_length("bogus")[0] is False


# ----------------------------------------------------------------------
# utils.py - is_allowed_file / read_uploaded_file
# ----------------------------------------------------------------------


def test_is_allowed_file():
    assert utils.is_allowed_file("notes.txt")
    assert not utils.is_allowed_file("notes.pdf")
    assert not utils.is_allowed_file("")


def _make_file_storage(content, filename="notes.txt"):
    return FileStorage(
        stream=io.BytesIO(content),
        filename=filename,
    )


def test_read_uploaded_file_valid_utf8():
    ok, text = utils.read_uploaded_file(
        _make_file_storage("line one\nline two\n".encode("utf-8"))
    )
    assert ok
    assert text == "line one\nline two"


def test_read_uploaded_file_invalid_extension():
    ok, message = utils.read_uploaded_file(
        _make_file_storage(b"data", filename="notes.pdf")
    )
    assert not ok
    assert ".txt" in message


def test_read_uploaded_file_empty():
    ok, message = utils.read_uploaded_file(_make_file_storage(b""))
    assert not ok
    assert "empty" in message


def test_read_uploaded_file_too_large():
    big = b"x" * (utils.MAX_FILE_SIZE + 1)
    ok, message = utils.read_uploaded_file(_make_file_storage(big))
    assert not ok
    assert "too large" in message


def test_read_uploaded_file_no_file():
    ok, message = utils.read_uploaded_file(None)
    assert not ok


# ----------------------------------------------------------------------
# prompts.py - build_prompt
# ----------------------------------------------------------------------


def test_build_prompt_includes_notes():
    prompt = prompts.build_prompt("Photosynthesis is key.", "short")
    assert "Photosynthesis is key." in prompt


def test_build_prompt_lengths_differ():
    short_prompt = prompts.build_prompt("some notes", "short")
    detailed_prompt = prompts.build_prompt("some notes", "detailed")
    assert short_prompt != detailed_prompt


def test_build_prompt_unknown_length_defaults():
    prompt = prompts.build_prompt("some notes", "unknown")
    assert "MEDIUM" in prompt


# ----------------------------------------------------------------------
# summarizer.py - mocked API calls
# ----------------------------------------------------------------------


class FakeResponse:
    """Stand-in for a requests.Response object."""

    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def _openai_payload(text="Mocked summary."):
    return {"choices": [{"message": {"content": text}}]}


def _gemini_payload(text="Mocked summary."):
    return {"candidates": [{"content": {"parts": [{"text": text}]}}]}


def _claude_payload(text="Mocked summary."):
    return {"content": [{"text": text}]}


def test_summarize_openai_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["json"]["model"] == summarizer.CHAT_MODEL
        return FakeResponse(200, _openai_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "openai", "fake-key")
    assert result == "Mocked summary."


def test_summarize_openrouter_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["headers"]["Authorization"] == "Bearer fake-key"
        return FakeResponse(200, _openai_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "openrouter", "fake-key")
    assert result == "Mocked summary."


def test_summarize_gemini_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["params"]["key"] == "fake-key"
        return FakeResponse(200, _gemini_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "gemini", "fake-key")
    assert result == "Mocked summary."


def test_summarize_google_ai_studio_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["params"]["key"] == "fake-key"
        return FakeResponse(200, _gemini_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "google-ai-studio", "fake-key")
    assert result == "Mocked summary."


def test_summarize_claude_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["headers"]["x-api-key"] == "fake-key"
        assert kwargs["headers"]["anthropic-version"] == "2023-06-01"
        return FakeResponse(200, _claude_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "claude", "fake-key")
    assert result == "Mocked summary."


def test_summarize_mistral_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["headers"]["Authorization"] == "Bearer fake-key"
        assert kwargs["json"]["model"] == "mistral-small-latest"
        return FakeResponse(200, _openai_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "mistral", "fake-key")
    assert result == "Mocked summary."


def test_summarize_grok_success(monkeypatch):
    def fake_post(*args, **kwargs):
        assert kwargs["headers"]["Authorization"] == "Bearer fake-key"
        assert kwargs["json"]["model"] == "grok-4.3"
        return FakeResponse(200, _openai_payload())

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    result = summarizer.summarize("notes", "short", "grok", "fake-key")
    assert result == "Mocked summary."


def test_summarize_unauthorized(monkeypatch):
    monkeypatch.setattr(
        summarizer.requests,
        "post",
        lambda *a, **k: FakeResponse(401, {"error": "nope"}),
    )
    with pytest.raises(SummarizerError, match="API key"):
        summarizer.summarize("notes", "short", "openai", "bad-key")


def test_summarize_timeout(monkeypatch):
    def fake_post(*args, **kwargs):
        raise summarizer.requests.exceptions.Timeout()

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    with pytest.raises(SummarizerError, match="too long"):
        summarizer.summarize("notes", "short", "openai", "fake-key")


def test_summarize_malformed_json(monkeypatch):
    monkeypatch.setattr(
        summarizer.requests,
        "post",
        lambda *a, **k: FakeResponse(200, ValueError("no json")),
    )
    with pytest.raises(SummarizerError, match="unreadable"):
        summarizer.summarize("notes", "short", "openai", "fake-key")


def test_summarize_empty_result(monkeypatch):
    monkeypatch.setattr(
        summarizer.requests,
        "post",
        lambda *a, **k: FakeResponse(200, _openai_payload("   ")),
    )
    with pytest.raises(SummarizerError, match="empty"):
        summarizer.summarize("notes", "short", "openai", "fake-key")


# ----------------------------------------------------------------------
# summarizer.py - provider config sanity
# ----------------------------------------------------------------------


def test_provider_config_is_complete():
    """Every provider advertised in the form is fully configured."""
    for provider in utils.PROVIDERS:
        config = summarizer.PROVIDERS[provider["id"]]
        assert callable(getattr(summarizer, config["extractor"]))
        assert config["endpoint"].startswith("https://")
        assert config["model"]
        assert config["auth_style"] in ("bearer", "query", "x-api-key")


def test_provider_models_are_current():
    """Canary: model IDs must be deliberately bumped when a provider
    retires a model, or every user of that provider gets an error."""
    current_models = {
        "openai": "gpt-4o-mini",
        "openrouter": "gpt-4o-mini",
        "gemini": "gemini-3.5-flash",
        "google-ai-studio": "gemini-3.5-flash",
        "claude": "claude-haiku-4-5-20251001",
        "mistral": "mistral-small-latest",
        "grok": "grok-4.3",
    }
    for provider, model in current_models.items():
        assert summarizer.PROVIDERS[provider]["model"] == model, (
            f"{provider} model changed; confirm it is not retired "
            "before updating this test."
        )


# ----------------------------------------------------------------------
# app.py - Flask routes (API calls mocked)
# ----------------------------------------------------------------------


@pytest.fixture()
def client(monkeypatch):
    """Flask test client with the AI call stubbed out."""
    app_module.app.config.update(TESTING=True)

    def fake_summarize(notes, length, provider, api_key):
        return f"Summary for {length} using {provider}."

    monkeypatch.setattr(summarizer, "summarize", fake_summarize)
    return app_module.app.test_client()


def test_index_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI Study Notes Summarizer" in response.data


def test_security_headers(client):
    response = client.get("/")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert "default-src 'self'" in response.headers.get(
        "Content-Security-Policy", ""
    )
    assert response.headers.get("Referrer-Policy") == "no-referrer"


def test_secret_key_not_hardcoded():
    # The app must never fall back to a fixed dev secret that ships in
    # the source tree.  It is either an env-supplied key or an ephemeral
    # random one (>= 32 hex chars).
    secret = app_module.app.secret_key
    assert secret != "dev-only-insecure-secret-change-me"
    assert len(secret) >= 32


def test_index_rejects_empty_notes(client):
    response = client.post(
        "/",
        data={"notes": "", "provider": "openai",
              "length": "short", "api_key": "key-1234567890"},
        follow_redirects=True,
    )
    assert b"Please enter some study notes" in response.data


def test_index_rejects_missing_api_key(client):
    response = client.post(
        "/",
        data={"notes": "some notes", "provider": "openai",
              "length": "short", "api_key": ""},
        follow_redirects=True,
    )
    assert b"API key" in response.data


def test_happy_path_generates_and_downloads(client):
    post_response = client.post(
        "/",
        data={"notes": "Important study notes here.",
              "provider": "openai",
              "length": "short",
              "api_key": "key-1234567890"},
    )
    assert post_response.status_code == 302

    result_page = client.get("/result")
    assert result_page.status_code == 200
    assert b"Summary for short using openai." in result_page.data

    download = client.get("/download")
    assert download.status_code == 200
    assert download.mimetype == "text/plain"
    assert download.data == b"Summary for short using openai."


def test_result_redirects_without_summary(client):
    response = client.get("/result")
    assert response.status_code == 302


def test_download_redirects_without_summary(client):
    response = client.get("/download")
    assert response.status_code == 302


def test_clear_resets_session(client):
    client.post(
        "/",
        data={"notes": "notes", "provider": "openai",
              "length": "short", "api_key": "key-1234567890"},
    )
    assert client.get("/result").status_code == 200

    response = client.post("/clear")
    assert response.status_code == 302
    assert client.get("/result").status_code == 302


def test_file_upload_happy_path(client):
    response = client.post(
        "/",
        data={
            "notes": "",
            "provider": "openai",
            "length": "medium",
            "api_key": "key-1234567890",
            "notes_file": (io.BytesIO(b"uploaded notes content"),
                           "uploaded.txt"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    assert client.get("/result").status_code == 200


def test_file_upload_over_char_cap_rejected(client):
    content = b"x" * (utils.MAX_NOTES_LENGTH + 1)
    response = client.post(
        "/",
        data={
            "notes": "",
            "provider": "openai",
            "length": "short",
            "api_key": "key-1234567890",
            "notes_file": (io.BytesIO(content), "big.txt"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert b"too long" in response.data
    assert client.get("/result").status_code == 302
