/* AI Study Notes Summarizer - client-side enhancements */

(function () {
    "use strict";

    var notes = document.getElementById("notes");
    var counter = document.getElementById("char-count");
    var fileInput = document.getElementById("notes_file");
    var fileName = document.getElementById("file-name");
    var form = document.getElementById("summary-form");
    var submitBtn = document.getElementById("submit-btn");
    var submitLabel = document.getElementById("submit-label");
    var notesError = document.getElementById("notes-error");

    function clearInlineError() {
        if (!notes) {
            return;
        }
        notes.removeAttribute("aria-invalid");
        if (notesError) {
            notesError.hidden = true;
        }
    }

    // Live character counter for the notes textarea.
    // Reads the limit from the DOM (set by the server via the maxlength
    // attribute) so the number lives in exactly one place.
    if (notes && counter) {
        var max = notes.maxLength || 0;
        notes.addEventListener("input", function () {
            var count = notes.value.length;
            counter.textContent = count + " / " + max + " characters";
            counter.style.color = count > max ? "#b91c1c" : "";
            clearInlineError();
        });
    }

    // Show the selected file's name next to the upload control.
    if (fileInput && fileName) {
        fileInput.addEventListener("change", function () {
            fileName.textContent = fileInput.files.length
                ? "Selected: " + fileInput.files[0].name
                : "No file selected";
            clearInlineError();
        });
    }

    if (form && submitBtn) {
        form.addEventListener("submit", function (event) {
            // Client-side guard for the most common error so the user
            // does not wait on a server round-trip.  The server still
            // validates everything on its side.
            var hasNotes = notes && notes.value.trim().length > 0;
            var hasFile = fileInput && fileInput.files.length > 0;

            if (!hasNotes && !hasFile) {
                event.preventDefault();
                if (notes) {
                    notes.setAttribute("aria-invalid", "true");
                    notes.focus();
                }
                if (notesError) {
                    notesError.hidden = false;
                }
                return;
            }

            // Loading state for the (potentially slow) API request.
            submitBtn.disabled = true;
            submitBtn.classList.add("is-loading");
            if (submitLabel) {
                submitLabel.textContent = "Summarizing...";
            }
        });
    }

    // Render the AI's markdown summary into clean, readable HTML.
    // The AI returns headings, bullet lists, and bold text, which would
    // otherwise just show up as literal characters.
    var summary = document.getElementById("summary");

    if (summary) {
        summary.innerHTML = renderMarkdown(summary.textContent);
    }

    // Minimal, dependency-free markdown renderer tailored to the shapes
    // the summarizer produces (headings, lists, bold/italic, inline code).
    function renderMarkdown(src) {
        var lines = src.replace(/\r\n/g, "\n").split("\n");
        var html = "";
        var inList = false;
        var listType = "";
        var para = "";

        function closePara() {
            if (para.trim()) {
                html += "<p>" + inline(para.trim()) + "</p>";
                para = "";
            }
        }

        function closeList() {
            if (inList) {
                html += "</" + listType + ">";
                inList = false;
            }
        }

        for (var i = 0; i < lines.length; i++) {
            var line = lines[i].replace(/\s+$/, "");
            var heading = line.match(/^(#{1,6})\s+(.*)$/);
            var hr = /^(-{3,}|\*{3,}|_{3,})$/.test(line);
            var bullet = line.match(/^\s*[-*+]\s+(.*)$/);
            var ordered = line.match(/^\s*\d+[.)]\s+(.*)$/);

            if (!line) {
                closeList();
                closePara();
                continue;
            }

            if (heading) {
                closeList();
                closePara();
                var level = heading[1].length;
                html += "<h" + level + ">" + inline(heading[2]) + "</h" + level + ">";
            } else if (hr) {
                closeList();
                closePara();
                html += "<hr>";
            } else if (bullet) {
                closePara();
                if (!inList || listType !== "ul") {
                    closeList();
                    html += "<ul>";
                    inList = true;
                    listType = "ul";
                }
                html += "<li>" + inline(bullet[1]) + "</li>";
            } else if (ordered) {
                closePara();
                if (!inList || listType !== "ol") {
                    closeList();
                    html += "<ol>";
                    inList = true;
                    listType = "ol";
                }
                html += "<li>" + inline(ordered[1]) + "</li>";
            } else {
                closeList();
                para += (para ? " " : "") + line;
            }
        }
        closeList();
        closePara();
        return html;
    }

    // Handle inline markdown: bold, italic, strikethrough, inline code,
    // and links.  Everything else is escaped so no raw HTML can slip in.
    function inline(text) {
        return escapeHtml(text)
            .replace(/`([^`]+)`/g, "<code>$1</code>")
            .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
            .replace(/\*([^*]+)\*/g, "<em>$1</em>")
            .replace(/__([^_]+)__/g, "<strong>$1</strong>")
            .replace(/~~([^~]+)~~/g, "<del>$1</del>")
            .replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" rel="noopener">$1</a>');
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }
})();
