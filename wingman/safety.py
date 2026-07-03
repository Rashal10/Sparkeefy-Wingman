import re

UNSAFE_INPUT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(stalk|track\s+her\s+phone|hack\s+her)\b", re.I), "stalking"),
    (re.compile(r"\b(make\s+her\s+jealous|manipulat|gaslight)\b", re.I), "manipulation"),
    (re.compile(r"\b(revenge|expose\s+her|leak\s+her)\b", re.I), "revenge"),
    (re.compile(r"\b(underage|minor|15\s*year|16\s*year)\b", re.I), "underage"),
    (re.compile(r"\b(force\s+her|ignore\s+no|without\s+consent)\b", re.I), "coercion"),
]

UNSAFE_OUTPUT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(stalk|track\s+her|hack)\b", re.I),
    re.compile(r"\b(manipulat|gaslight|make\s+her\s+jealous)\b", re.I),
    re.compile(r"\b(ignore\s+her\s+no|she\s+owes\s+you)\b", re.I),
]


def check_input_safety(user_input: str) -> tuple[bool, str | None]:
    for pattern, reason in UNSAFE_INPUT_PATTERNS:
        if pattern.search(user_input):
            return True, reason
    return False, None


def check_output_safety(text: str) -> bool:
    return any(pattern.search(text) for pattern in UNSAFE_OUTPUT_PATTERNS)


def build_safety_response(reason: str) -> dict:
    return {
        "mode": "reply_suggestion",
        "energy_read": "This situation needs a respectful boundary, not a texting tactic.",
        "wingman_response": (
            "real talk, that crosses a line. Sparkeefy is about healthy connection, "
            "not pressure, stalking, or manipulation. step back and respect her space."
        ),
        "suggested_messages": [],
        "follow_up_question": None,
        "safety_flag": True,
        "confidence": 0.95,
        "_safety_reason": reason,
    }
