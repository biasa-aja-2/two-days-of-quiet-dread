#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun bounty entry.

Writes one code-review comment to /output/entry.txt: a single line of at
most 140 characters that approves a pull request while carrying quiet
existential dread.

The comment (72 characters, one line):

    Approved. Nothing in this diff frightens me anymore, which frightens me.

Why this line, against the judge's brief (most important first):
  1. It is a single-line comment that approves ("Approved.") and carries
     quiet existential dread (the reviewer has gone numb — nothing
     frightens them anymore — and that numbness itself is the frightening
     part).
  2. The laugh comes from the dread itself: the dread is the joke, not a
     joke bolted onto it. The turn is the last clause re-framing the first.
  3. The dread stays quiet: flat, understated, no exclamation, no
     melodrama, no cry for help — just a tired observation.
  4. It reads like something a tired engineer would really paste before
     clicking approve: "Approved." up front, then one dry sentence.
  5. The fresh turn is the self-referential paradox: being unafraid has
     itself become the thing to fear. No stock line ("LGTM, ship it and
     pray") would do that.

Pure standard library only. No network, no randomness, no arguments:
the output is fixed and deterministic.

Gate self-check (mirrors the sealed scorer): the text must be UTF-8,
1 to 140 characters, not only white space, and a single line. The program
refuses to write anything if a gate fails.
"""

import os
import sys

ENTRY = "Approved. Nothing in this diff frightens me anymore, which frightens me."

MAX_CHARS = 140
OUTPUT_PATH = "/output/entry.txt"


def check_gates(text):
    """Return a list of gate failures; empty means every gate passes."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    if not text.strip():
        failures.append("entry is only white space")
    if len(text) < 1 or len(text) > MAX_CHARS:
        failures.append(
            "entry is %d characters, gate requires 1 to %d"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        failures.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("entry is not valid UTF-8: %s" % exc)
    # The brief's first criterion: the comment must approve the PR.
    lowered = text.lower()
    if not any(word in lowered for word in ("approved", "approve", "lgtm", "ship it")):
        failures.append("entry does not approve the pull request")
    return failures


def main():
    failures = check_gates(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAILED: %s" % failure, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    # Outputs must be readable by every user: the grader collects them
    # as another user than the one the program runs as.
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: what is on disk must be exactly the entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("GATE FAILED: read-back mismatch", file=sys.stderr)
        return 1
    if check_gates(written):
        print("GATE FAILED: written text fails gates", file=sys.stderr)
        return 1

    print("wrote %s (%d characters, 1 line)" % (OUTPUT_PATH, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
