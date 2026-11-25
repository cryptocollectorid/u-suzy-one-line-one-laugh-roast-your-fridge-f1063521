#!/usr/bin/env python3
"""One Line, One Laugh: Roast Your Fridge.

Writes a single-line roast of my phone to /output/entry.txt.
Gate (sealed scorer): UTF-8 text of 1-200 characters, not only whitespace.
"""

import os
import sys

ENTRY = (
    "My phone dies at 23% like it's fainting for attention, "
    "and the charger only works if I hold it at a 45-degree "
    "angle and apologize first."
)

MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Fail loudly when the entry breaks the sealed gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry must be valid UTF-8 text") from exc


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Write the entry and return its byte count."""
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Round-trip read-back: the file on disk must hold exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise ValueError("round-trip check failed: file differs from entry")
    return len(text.encode("utf-8"))


def main() -> int:
    n = write_entry(ENTRY)
    print(f"Wrote {len(ENTRY)} characters ({n} bytes) to /output/entry.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
