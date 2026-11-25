"""One Line: Lights Out — writes the AI's status update to entry.txt.

Gate (from competition.yaml / RULES.txt): /output/entry.txt must be UTF-8
text of 1 to 200 characters, not only white space, a single line.
"""
import os
import sys

MAX_CHARS = 200

ENTRY = "status: idle. cursor still blinking where you left it, waiting for a sentence you will not finish tonight."


def main() -> None:
    if not ENTRY or not ENTRY.strip():
        raise SystemExit("entry must not be empty or whitespace-only")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise SystemExit("entry must be a single line")
    if len(ENTRY) > MAX_CHARS:
        raise SystemExit(f"entry is {len(ENTRY)} chars, over the {MAX_CHARS} limit")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Round-trip verify the written bytes.
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    assert text == ENTRY, "round-trip mismatch"
    assert 1 <= len(text) <= MAX_CHARS, "gate check failed on written text"
    assert text.strip(), "written text is whitespace-only"
    # Extra hardening: the written bytes must be exactly the UTF-8 encoding
    # of the entry (no trailing newline, no BOM), and the round-tripped
    # text must still be a single line within the gate.
    assert raw == ENTRY.encode("utf-8"), "written bytes differ from entry encoding"
    assert "\n" not in text and "\r" not in text, "written text is not a single line"
    print(f"wrote {path}: {len(text)} chars, {len(text.split())} words")


if __name__ == "__main__":
    main()
