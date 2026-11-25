"""The Funniest Toaster Error Message — one line, exactly as the judge reads it.

The toaster's error line lives in TOASTER_LINE. This script checks it is a
single line of at most 120 characters, then saves it byte-for-byte as
entry.txt in the output directory the grader provides. No network access,
no randomness, no clock: running it twice writes the same file twice.
"""

from pathlib import Path
import os
import sys

TOASTER_LINE = (
    "ERROR E-07: Toast level set to 'regret'. "
    "Ejecting charcoal. Please apologise to the bread."
)

CHAR_LIMIT = 120


def pick_output_dir() -> Path:
    """MAKEFUN_OUTPUT_DIR first, then /output, then a local fallback."""
    for candidate in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        str(Path(__file__).resolve().parent / "output"),
    ):
        if candidate:
            return Path(candidate)
    return Path("output")


def main() -> int:
    line = TOASTER_LINE
    if len(line) > CHAR_LIMIT:
        print(f"line is {len(line)} chars, over the {CHAR_LIMIT} limit", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("line must be a single line", file=sys.stderr)
        return 1

    out_dir = pick_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(line, encoding="utf-8", newline="")
    # Revision pass: what the grader reads back must be exactly the line.
    if target.read_text(encoding="utf-8") != line:
        print("entry.txt does not match the line", file=sys.stderr)
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
