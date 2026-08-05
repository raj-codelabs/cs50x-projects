"""AI communication for the AI Study Notes Summarizer.

This is the ONLY module that talks to the outside world.  Every API
request, response check, and error mapping lives here so that app.py
stays focused on web handling.

Supported providers:
    - openai         : OpenAI chat completions API
    - openrouter     : OpenAI-compatible chat completions API
    - gemini         : Google Gemini generateContent API
    - google-ai-studio : Google AI Studio (Gemini API)
    - claude         : Anthropic Claude API
    - mistral        : Mistral AI API
    - grok           : xAI Grok API
"""

import requests

import prompts

# How long to wait for a response before giving up (seconds).
REQUEST_TIMEOUT = 90

# OpenAI-compatible providers share this model.
CHAT_MODEL = "gpt-4o-mini"

# Provider configuration: endpoint, model, auth style, extractor.
# auth_style: "bearer" (Authorization header), "query" (key in query string), "x-api-key" (Claude header)
PROVIDERS = {
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": CHAT_MODEL,
        "auth_style": "bearer",
        "extractor": "_extract_openai_text",
    },
    "openrouter": {
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "model": CHAT_MODEL,
        "auth_style": "bearer",
        "extractor": "_extract_openai_text",
    },
    "mistral": {
        "endpoint": "https://api.mistral.ai/v1/chat/completions",
        "model": "mistral-small-latest",
        "auth_style": "bearer",
        "extractor": "_extract_openai_text",
    },
    "grok": {
        "endpoint": "https://api.x.ai/v1/chat/completions",
        "model": "grok-4.3",
        "auth_style": "bearer",
        "extractor": "_extract_openai_text",
    },
    "gemini": {
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
        "model": "gemini-3.5-flash",
        "auth_style": "query",
        "extractor": "_extract_gemini_text",
    },
    "google-ai-studio": {
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
        "model": "gemini-3.5-flash",
        "auth_style": "query",
        "extractor": "_extract_gemini_text",
    },
    "claude": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "model": "claude-haiku-4-5-20251001",
        "auth_style": "x-api-key",
        "extractor": "_extract_claude_text",
    },
}


class SummarizerError(Exception):
    """Raised when the AI provider cannot produce a summary.

    The message is always safe to show to the user; it never contains
    the API key or other secrets.
    """


def summarize(notes, length, provider, api_key):
    """Produce a summary of the given notes.

    Parameters
    ----------
    notes : str
        Cleaned study notes.
    length : str
        One of "short", "medium", or "detailed".
    provider : str
        One of "openai", "openrouter", "gemini", "google-ai-studio",
        "claude", "mistral", or "grok".
    api_key : str
        The user's API key for the chosen provider.

    Returns
    -------
    str
        The summary text returned by the AI provider.

    Raises
    ------
    SummarizerError
        If the provider rejects the request, the network fails, the
        response is invalid, or the summary is empty.
    """
    if provider not in PROVIDERS:
        raise SummarizerError(f"Unsupported provider: {provider}")

    prompt = prompts.build_prompt(notes, length)
    config = PROVIDERS[provider]

    if config["auth_style"] == "query":
        text = _request_gemini_style(config, prompt, api_key)
    elif config["auth_style"] == "x-api-key":
        text = _request_claude_style(config, prompt, api_key)
    else:
        text = _request_openai_compatible(config, prompt, api_key)

    text = (text or "").strip()
    if not text:
        raise SummarizerError(
            "The AI returned an empty summary. Please try again."
        )
    return text


def _request_openai_compatible(config, prompt, api_key):
    """Ask an OpenAI-compatible provider (OpenAI, OpenRouter, Mistral, Grok)."""
    payload = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = _post_json(config["endpoint"], payload, headers)
    extractor = globals()[config["extractor"]]
    return extractor(data)


def _request_gemini_style(config, prompt, api_key):
    """Ask Google Gemini or Google AI Studio to summarize the prompt."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    headers = {"Content-Type": "application/json"}
    data = _post_json(config["endpoint"], payload, headers, api_key)
    extractor = globals()[config["extractor"]]
    return extractor(data)


def _request_claude_style(config, prompt, api_key):
    """Ask Anthropic Claude to summarize the prompt."""
    payload = {
        "model": config["model"],
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    data = _post_json(config["endpoint"], payload, headers)
    extractor = globals()[config["extractor"]]
    return extractor(data)


def _post_json(url, payload, headers, api_key=None):
    """Send a JSON POST request and return the parsed JSON response.

    Handles the auth key for providers (like Gemini) that expect the
    key in the query string instead of the Authorization header.

    Raises SummarizerError for any failure.
    """
    params = {"key": api_key} if api_key is not None else None

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.Timeout:
        raise SummarizerError(
            "The AI provider took too long to respond. Please try again."
        )
    except requests.exceptions.RequestException:
        raise SummarizerError(
            "Could not reach the AI provider. "
            "Please check your internet connection and try again."
        )

    if response.status_code in (401, 403):
        raise SummarizerError(
            "Your API key was rejected by the provider. "
            "Please check the key and try again."
        )

    if response.status_code == 429:
        raise SummarizerError(
            "The AI provider is rate limiting requests. "
            "Please wait a moment and try again."
        )

    if response.status_code != 200:
        raise SummarizerError(
            f"The AI provider returned an error "
            f"(HTTP {response.status_code}). Please try again."
        )

    try:
        return response.json()
    except ValueError:
        raise SummarizerError(
            "The AI provider returned an unreadable response. "
            "Please try again."
        )


def _extract_openai_text(data):
    """Pull the summary text out of an OpenAI-style response."""
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise SummarizerError(
            "The AI provider returned an unexpected response. "
            "Please try again."
        )


def _extract_gemini_text(data):
    """Pull the summary text out of a Gemini response."""
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise SummarizerError(
            "The AI provider returned an unexpected response. "
            "Please try again."
        )


def _extract_claude_text(data):
    """Pull the summary text out of a Claude response."""
    try:
        return data["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise SummarizerError(
            "The AI provider returned an unexpected response. "
            "Please try again."
        )