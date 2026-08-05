"""Prompt templates for the AI Study Notes Summarizer.

This module keeps every prompt template in one place.  Building the
prompt text lives here so that the rest of the application never has
to know what the AI is being told.
"""

# Instruction used when the user picks the "Short" summary length.
SHORT_INSTRUCTION = (
    "You are a helpful study assistant. Create a SHORT revision summary of "
    "the notes below. Use exactly 3 to 5 bullet points, each one line long, "
    "covering only the most exam-critical ideas — the points a student would "
    "want to see in the last five minutes before a test. Skip minor details "
    "and examples. Use only information found in the notes; do not add "
    "outside facts or opinions."
)

# Instruction used when the user picks the "Medium" summary length.
MEDIUM_INSTRUCTION = (
    "You are a helpful study assistant. Create a MEDIUM-length revision "
    "summary of the notes below. Group the material under short topic "
    "headings, and under each heading use bullet points for key concepts, "
    "important definitions, and main takeaways. Keep each bullet point to "
    "one or two sentences. Use only information found in the notes; do not "
    "add outside facts or opinions."
)

# Instruction used when the user picks the "Detailed" summary length.
DETAILED_INSTRUCTION = (
    "You are a helpful study assistant. Create a DETAILED study summary of "
    "the notes below. Organize the material into clearly labeled sections "
    "with bullet points, including key definitions, explanations, worked "
    "examples, and any important details or exceptions. Where the notes "
    "distinguish easily confused ideas or list common mistakes, call those "
    "out explicitly. Be thorough, but use only information found in the "
    "notes; do not add outside facts or opinions."
)

# Maps each supported summary length to its prompt instruction.
PROMPT_TEMPLATES = {
    "short": SHORT_INSTRUCTION,
    "medium": MEDIUM_INSTRUCTION,
    "detailed": DETAILED_INSTRUCTION,
}


def build_prompt(notes, length):
    """Build the complete prompt sent to the AI.

    Parameters
    ----------
    notes : str
        The study notes supplied by the user.
    length : str
        One of "short", "medium", or "detailed".

    Returns
    -------
    str
        The finished prompt combining the instruction and the notes.
    """
    instruction = PROMPT_TEMPLATES.get(
        length, MEDIUM_INSTRUCTION
    )
    return f"{instruction}\n\n--- BEGIN NOTES ---\n{notes}\n--- END NOTES ---"