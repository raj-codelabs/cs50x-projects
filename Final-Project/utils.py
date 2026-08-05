"""Utility functions for the AI Study Notes Summarizer.

This module holds all the pure helper logic: constants, text cleaning,
input validation, and uploaded-file handling.  Keeping this code in one
module (instead of inside app.py) makes it easy to read and easy to test.
"""

import re

# Maximum number of characters accepted for pasted notes.
MAX_NOTES_LENGTH = 50_000

# Maximum uploaded file size in bytes (1 MB).
MAX_FILE_SIZE = 1_000_000

# Only plain-text files may be uploaded.
ALLOWED_EXTENSIONS = {".txt"}

# Providers shown in the form's dropdown.
PROVIDERS = [
    {"id": "openai", "label": "OpenAI"},
    {"id": "gemini", "label": "Google Gemini"},
    {"id": "google-ai-studio", "label": "Google AI Studio"},
    {"id": "openrouter", "label": "OpenRouter"},
    {"id": "claude", "label": "Claude (Anthropic)"},
    {"id": "mistral", "label": "Mistral"},
    {"id": "grok", "label": "Grok (xAI)"},
]

# Summary lengths shown as radio buttons.
SUMMARY_LENGTHS = [
    {"id": "short", "label": "Short"},
    {"id": "medium", "label": "Medium"},
    {"id": "detailed", "label": "Detailed"},
]

# Fallback characters used when a file cannot be decoded as UTF-8.
FALLBACK_ENCODING = "latin-1"


def clean_text(text):
    """Normalize raw text for summarization.

    Removes leading/trailing whitespace, converts Windows-style line
    endings to Unix, and collapses runs of blank lines into a single one.

    Parameters
    ----------
    text : str
        The raw text entered by the user or read from a file.

    Returns
    -------
    str
        The cleaned text.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip()
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def validate_notes(notes):
    """Check that pasted notes are usable.

    Parameters
    ----------
    notes : str
        The notes text supplied by the user.

    Returns
    -------
    tuple
        (True, "") when the notes are valid, otherwise (False, message)
        describing the problem.
    """
    if not notes or not notes.strip():
        return False, "Please enter some study notes."
    if len(notes) > MAX_NOTES_LENGTH:
        return (
            False,
            f"Your notes are too long ({len(notes):,} characters). "
            f"The maximum is {MAX_NOTES_LENGTH:,} characters.",
        )
    return True, ""


def validate_api_key(api_key):
    """Check that an API key looks plausible.

    Parameters
    ----------
    api_key : str
        The API key supplied by the user.

    Returns
    -------
    tuple
        (True, "") when valid, otherwise (False, message).
    """
    if not api_key or not api_key.strip():
        return False, "Please enter your API key."
    if len(api_key.strip()) < 10:
        return False, "That API key looks too short to be valid."
    return True, ""


def validate_provider(provider):
    """Check that a provider id is one we support."""
    ids = [p["id"] for p in PROVIDERS]
    if provider not in ids:
        return False, "Please choose a supported AI provider."
    return True, ""


def validate_length(length):
    """Check that a summary length is one we support."""
    ids = [l["id"] for l in SUMMARY_LENGTHS]
    if length not in ids:
        return False, "Please choose a valid summary length."
    return True, ""


def is_allowed_file(filename):
    """Return True if the filename ends in an allowed extension."""
    name = (filename or "").lower()
    return name.endswith(tuple(ALLOWED_EXTENSIONS))


def read_uploaded_file(file_storage):
    """Read and validate an uploaded file.

    Parameters
    ----------
    file_storage : werkzeug.datastructures.FileStorage
        The uploaded file from the request.

    Returns
    -------
    tuple
        (True, text) when the file is valid, otherwise
        (False, error_message).
    """
    if file_storage is None or not file_storage.filename:
        return False, "No file was uploaded."

    if not is_allowed_file(file_storage.filename):
        return (
            False,
            "Unsupported file type. Please upload a .txt file.",
        )

    file_storage.stream.seek(0, 2)  # Move to the end to measure size.
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)     # Move back to the start to read.

    if size == 0:
        return False, "The uploaded file is empty."
    if size > MAX_FILE_SIZE:
        return (
            False,
            "The uploaded file is too large (over 1 MB). "
            "Please upload a smaller file or paste your notes.",
        )

    try:
        raw = file_storage.read()
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        # Fall back to latin-1 so any byte sequence can be decoded.
        text = raw.decode(FALLBACK_ENCODING)

    text = clean_text(text)
    if not text:
        return False, "The uploaded file does not contain any text."

    return True, text
