"""AI Study Notes Summarizer - Flask web application.

The application lets a student paste study notes (or upload a .txt
file), pick an AI provider, provide their own API key, choose a summary
length, and receive a downloadable AI summary.

Routes
------
    GET  /         Display the input form.
    POST /         Validate input and generate the summary.
    GET  /result   Display the generated summary.
    GET  /download Download the summary as summary.txt.
    POST /clear    Forget the current summary (start over).
"""

import io
import os
import secrets

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

import summarizer
import utils

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = utils.MAX_FILE_SIZE

# Session signing secret.  Never ship a hardcoded key: when the
# SECRET_KEY environment variable is unset we generate an ephemeral
# random one, so sessions simply reset on restart (fine for local dev).
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", secrets.token_hex(32)
)

# Hardened session cookies.  Secure is only valid over HTTPS, so it is
# opt-in via the SECURE_COOKIES environment variable for production.
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SECURE_COOKIES") == "1"


@app.after_request
def set_security_headers(response):
    """Apply conservative security headers to every response."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    # The app has no inline scripts or styles, so 'self' is sufficient.
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'")
    return response


# Server-side summary store.  The summary can exceed the ~4 KB browser
# cookie limit, so only a short random id goes in the session and the
# text lives here.
# ponytail: in-memory dict grows with every summary; fine for a
# single-user local app.  Upgrade to a TTL cache or DB if deployed.
_summaries = {}


@app.route("/", methods=["GET"])
def index():
    """Display the input form."""
    return render_template(
        "index.html",
        providers=utils.PROVIDERS,
        lengths=utils.SUMMARY_LENGTHS,
        max_length=utils.MAX_NOTES_LENGTH,
    )


@app.route("/", methods=["POST"])
def summarize():
    """Validate the form and generate a summary."""
    notes = request.form.get("notes", "")
    api_key = request.form.get("api_key", "")
    provider = request.form.get("provider", "")
    length = request.form.get("length", "")

    # Prefer pasted notes, but fall back to an uploaded file.
    uploaded = request.files.get("notes_file")
    if not notes.strip() and (uploaded is None or not uploaded.filename):
        flash("Please enter some study notes or upload a .txt file.", "error")
        return _redirect_back()

    if not notes.strip():
        ok, notes_or_error = utils.read_uploaded_file(uploaded)
        if not ok:
            flash(notes_or_error, "error")
            return _redirect_back()
        notes = notes_or_error
    else:
        notes = utils.clean_text(notes)

    # The length cap applies to pasted notes and uploaded files alike.
    ok, message = utils.validate_notes(notes)
    if not ok:
        flash(message, "error")
        return _redirect_back()

    # Validate the remaining fields one at a time so the user sees
    # a clear, friendly message for each problem.
    for validator, value, label in (
        (utils.validate_api_key, api_key, "API key"),
        (utils.validate_provider, provider, "provider"),
        (utils.validate_length, length, "summary length"),
    ):
        ok, message = validator(value)
        if not ok:
            flash(f"Missing or invalid {label}: {message}", "error")
            return _redirect_back()

    try:
        summary = summarizer.summarize(notes, length, provider, api_key)
    except summarizer.SummarizerError as exc:
        flash(str(exc), "error")
        return _redirect_back()

    # Keep only a short id in the session: the summary text can exceed
    # the ~4 KB browser cookie limit, so it lives in the server-side
    # store instead of the cookie.
    summary_id = secrets.token_urlsafe(16)
    _summaries[summary_id] = summary
    session["summary_id"] = summary_id

    return redirect(url_for("result"))


@app.route("/result")
def result():
    """Display the generated summary."""
    summary = _summaries.get(session.get("summary_id"))
    if not summary:
        return redirect(url_for("index"))
    return render_template(
        "result.html",
        summary=summary,
        word_count=len(summary.split()),
    )


@app.route("/download")
def download():
    """Download the current summary as a text file."""
    summary = _summaries.get(session.get("summary_id"))
    if not summary:
        return redirect(url_for("index"))
    return send_file(
        _summary_bytes_io(summary),
        as_attachment=True,
        download_name="summary.txt",
        mimetype="text/plain",
    )


@app.route("/clear", methods=["POST"])
def clear():
    """Forget the current summary and return to the homepage."""
    summary_id = session.pop("summary_id", None)
    if summary_id:
        _summaries.pop(summary_id, None)
    return redirect(url_for("index"))


@app.errorhandler(413)
def too_large(error):
    """Show a friendly message when an upload exceeds the size limit."""
    return (
        "Your upload is too large (over 1 MB). "
        "Please upload a smaller file or paste your notes.",
        413,
    )


@app.errorhandler(500)
def server_error(error):
    """Never let an unexpected error crash the app visibly."""
    app.logger.exception("Unhandled error: %s", error)
    return (
        "Sorry, something went wrong on our end. "
        "Please go back and try again.",
        500,
    )


def _redirect_back():
    """Redirect back to the homepage after an error."""
    return redirect(url_for("index"))


def _summary_bytes_io(summary):
    """Wrap the summary text as a BytesIO so send_file can serve it."""
    stream = io.BytesIO(summary.encode("utf-8"))
    stream.seek(0)
    return stream


if __name__ == "__main__":
    # Debug mode turns on the interactive Werkzeug debugger (a remote
    # code execution risk if exposed), so it is opt-in via FLASK_DEBUG.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
