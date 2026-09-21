from __future__ import annotations

import sys
import unittest
from pathlib import Path


# Adds the src folder to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


from vigenere_analysis import (  # noqa: E402
    average_column_ic,
    index_of_coincidence,
    normalise_letters,
    rank_key_lengths,
)


# Encrypts sample text so the key-length analysis can be tested.
def vigenere_encrypt(plaintext: str, key: str) -> str:
    letters = normalise_letters(plaintext)
    key_values = [
        ord(character) - ord("A")
        for character in normalise_letters(key)
    ]

    if not key_values:
        raise ValueError("key must contain a letter")

    encrypted = []

    for index, character in enumerate(letters):
        shift = key_values[index % len(key_values)]
        encrypted_character = chr(
            (ord(character) - ord("A") + shift) % 26
            + ord("A")
        )
        encrypted.append(encrypted_character)

    return "".join(encrypted)


# Tests the main functions in vigenere_analysis.py.
class VigenereAnalysisTests(unittest.TestCase):

    # Checks that punctuation, spaces, and numbers are removed.
    def test_normalise_letters(self) -> None:
        result = normalise_letters("Hello, World! 123")
        self.assertEqual(result, "HELLOWORLD")

    # Text containing fewer than two letters should return zero.
    def test_index_of_coincidence_rejects_short_input(self) -> None:
        result = index_of_coincidence("A")
        self.assertEqual(result, 0.0)

    # Key lengths must be at least one.
    def test_average_column_ic_validates_key_length(self) -> None:
        with self.assertRaises(ValueError):
            average_column_ic("SAMPLETEXT", 0)

    # Checks that the real key length appears in the ranked results.
    def test_true_period_is_among_top_candidates(self) -> None:
        plaintext = (
            "Security testing should be authorised documented and repeatable. "
            "Evidence should explain the observed behaviour the potential impact "
            "and the actions required to reduce risk. Clear reporting helps system "
            "owners understand findings prioritise remediation and verify fixes. "
        ) * 18

        key = "ORANGE"
        ciphertext = vigenere_encrypt(plaintext, key)

        candidates = rank_key_lengths(
            ciphertext,
            max_key_length=18,
            top=8,
        )

        ranked_lengths = [
            candidate.key_length
            for candidate in candidates
        ]

        self.assertIn(len(key), ranked_lengths)

    # Invalid command values should raise an error.
    def test_invalid_arguments_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            rank_key_lengths(
                "EXAMPLETEXT",
                max_key_length=0,
            )

        with self.assertRaises(ValueError):
            rank_key_lengths(
                "EXAMPLETEXT",
                top=0,
            )


# Runs the tests when this file is executed directly.
if __name__ == "__main__":
    unittest.main()