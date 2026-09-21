from __future__ import annotations

import argparse
import string
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ASCII_LETTERS = frozenset(string.ascii_uppercase)


# Stores a possible key length and its average IC score.
@dataclass(frozen=True)
class KeyLengthCandidate:
    key_length: int
    average_ic: float


# Removes spaces, numbers, and punctuation from the text.
def normalise_letters(text: str) -> str:
    return "".join(
        character
        for character in text.upper()
        if character in ASCII_LETTERS
    )


# Calculates how often letters are likely to repeat in the text.
def index_of_coincidence(text: str) -> float:
    letters = normalise_letters(text)
    length = len(letters)

    if length < 2:
        return 0.0

    counts = Counter(letters)
    matching_pairs = sum(
        count * (count - 1)
        for count in counts.values()
    )

    return matching_pairs / (length * (length - 1))


# Tests one possible key length by splitting the ciphertext into columns.
def average_column_ic(ciphertext: str, key_length: int) -> float:
    if key_length < 1:
        raise ValueError("key_length must be at least 1")

    letters = normalise_letters(ciphertext)

    if len(letters) < key_length * 2:
        raise ValueError("ciphertext is too short for this key length")

    # Characters in each column were encrypted by the same key position.
    columns = [
        letters[offset::key_length]
        for offset in range(key_length)
    ]

    total_ic = sum(
        index_of_coincidence(column)
        for column in columns
    )

    return total_ic / key_length


# Tests each possible key length and returns the highest-scoring results.
def rank_key_lengths(
    ciphertext: str,
    max_key_length: int = 30,
    top: int = 5,
) -> list[KeyLengthCandidate]:
    if max_key_length < 1:
        raise ValueError("max_key_length must be at least 1")

    if top < 1:
        raise ValueError("top must be at least 1")

    letters = normalise_letters(ciphertext)

    if len(letters) < 4:
        raise ValueError("ciphertext must contain at least 4 letters")

    largest_candidate = min(max_key_length, len(letters) // 2)

    candidates = [
        KeyLengthCandidate(
            key_length=key_length,
            average_ic=average_column_ic(letters, key_length),
        )
        for key_length in range(1, largest_candidate + 1)
    ]

    # Higher IC scores are displayed first.
    candidates.sort(
        key=lambda candidate: (
            -candidate.average_ic,
            candidate.key_length,
        )
    )

    return candidates[:top]


# Defines the command-line options accepted by the program.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate likely Vigenere key lengths."
    )

    parser.add_argument(
        "ciphertext_file",
        type=Path,
        help="UTF-8 file containing the ciphertext",
    )

    parser.add_argument(
        "--max-key-length",
        type=int,
        default=30,
        help="largest key length to test (default: 30)",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="number of results to display (default: 5)",
    )

    return parser


# Reads the ciphertext file and displays the ranked results.
def main() -> None:
    args = build_parser().parse_args()

    ciphertext = args.ciphertext_file.read_text(
        encoding="utf-8"
    )

    candidates = rank_key_lengths(
        ciphertext,
        max_key_length=args.max_key_length,
        top=args.top,
    )

    print("Likely key lengths")
    print("------------------")

    for candidate in candidates:
        print(
            f"{candidate.key_length:>3}  "
            f"average IC = {candidate.average_ic:.5f}"
        )


# Runs main only when this file is executed directly.
if __name__ == "__main__":
    main()