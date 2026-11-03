import re

# Ordered list of (pattern, replacement). Applied top-to-bottom to un-defang
# obfuscated IOCs (e.g. "hxxps://evil[.]com" -> "https://evil.com").
_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"hxxps://", re.IGNORECASE), "https://"),
    (re.compile(r"hxxp://", re.IGNORECASE), "http://"),
    (re.compile(r"http\[s\]://", re.IGNORECASE), "https://"),
    (re.compile(r"http\[:\]//", re.IGNORECASE), "http://"),
    (re.compile(r"\[\.\]|\(\.\)|\{\.\}"), "."),
    (re.compile(r"\[dot\]|\(dot\)|\{dot\}", re.IGNORECASE), "."),
    (re.compile(r"\[:\]|\(:\)"), ":"),
    (re.compile(r"\[/\]"), "/"),
    (re.compile(r"\[@\]"), "@"),
]


def defang(raw: str) -> str:
    result = raw.strip()
    for pattern, replacement in _PATTERNS:
        result = pattern.sub(replacement, result)
    return result
