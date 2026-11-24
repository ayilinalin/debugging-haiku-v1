#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — make.fun entry.

Writes one haiku about debugging (3 lines, 5-7-5 syllables, <=200 chars)
to /output/entry.txt. Fully deterministic: the same haiku every run.

The program keeps a small hand-written candidate list, scores each one
against the judge's brief (form first, then concrete image, then a turn
in the last line, then economy of words), and writes the winner.
"""

import os

# Syllable counts for every word used by the candidates below,
# hand-counted (no heuristic counter — the counts are the point).
SYLLABLES = {
    "the": 1, "duck": 1, "says": 1, "nothing": 2,
    "while": 1, "red": 1, "dot": 1, "holds": 1, "its": 1, "breath": 1,
    "git": 1, "blame": 1, "still": 1, "names": 1, "me": 1,
    "stares": 1, "at": 1, "screen": 1, "cold": 1,
    "log": 1, "line": 1, "tells": 1, "no": 1, "lies": 1,
    "bug": 1, "sleeps": 1, "in": 1, "my": 1, "own": 1, "code": 1,
    "cursor": 2, "blinks": 1, "three": 1, "am": 1,
    "stack": 1, "trace": 1, "ends": 1, "where": 1, "it": 1, "began": 2,
    "i": 1, "wrote": 1, "this": 1, "years": 1, "ago": 2,
    "one": 1, "back": 1, "yet": 1, "starts": 1,
}

CANDIDATES = [
    # A: rubber duck, breakpoint, git blame — the bug's author is past-me.
    ("The duck says nothing",
     "while the red dot holds its breath",
     "git blame still names me"),
    # B: cold screen, honest log line, the bug lives in my own code.
    ("The cold screen stares back",
     "one log line tells no lies yet",
     "the bug sleeps in code"),
    # C: cursor at 3am, stack trace circles home, I wrote it years ago.
    ("Cursor blinks at three",
     "the stack trace ends where it starts",
     "wrote this years ago"),
]


def count_line(line: str) -> int:
    total = 0
    for word in line.lower().replace(",", "").split():
        total += SYLLABLES[word]
    return total


def valid(haiku) -> bool:
    if [count_line(line) for line in haiku] != [5, 7, 5]:
        return False
    text = "\n".join(haiku)
    return 1 <= len(text) <= 200


def score(haiku) -> int:
    """Form is pass/fail; among valid ones prefer the concrete image
    (duck / breakpoint / blame) and the sharpest last-line turn."""
    text = " ".join(haiku).lower()
    points = 0
    if "duck" in text:
        points += 3  # concrete, uncommon debugging image
    if "red dot" in text:
        points += 3  # the breakpoint, seen not stated
    if "git blame" in text:
        points += 4  # the turn: the culprit is named, and it is me
    if "cursor" in text and "three" in text:
        points -= 5  # overused image in this field
    return points


def pick() -> tuple:
    ranked = sorted(
        (c for c in CANDIDATES if valid(c)),
        key=score,
        reverse=True,
    )
    return ranked[0]


def main() -> None:
    haiku = pick()
    text = "\n".join(haiku) + "\n"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
