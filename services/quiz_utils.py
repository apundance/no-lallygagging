import random
import re


SKIP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "he",
    "her",
    "his",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "she",
    "that",
    "the",
    "their",
    "them",
    "they",
    "to",
    "was",
    "we",
    "were",
    "with",
    "you",
    "your",
}


def clean_word(word):
    """
    Removes punctuation and converts to lowercase.
    """

    return re.sub(
        r"^[^\w]+|[^\w]+$",
        "",
        word
    ).lower()


def get_blank_indices(
    words,
    difficulty_percent=25
):
    """
    Returns a list of word indices to blank.

    difficulty_percent:
        10 = Easy
        25 = Medium
        40 = Hard
        60 = Expert
    """

    eligible = []

    for i, word in enumerate(words):

        cleaned = clean_word(word)

        if not cleaned:
            continue

        # Skip common filler words
        if cleaned in SKIP_WORDS:
            continue

        # Skip very short words
        if len(cleaned) <= 2:
            continue

        eligible.append(i)

    if not eligible:
        return []

    blank_count = max(
        1,
        round(
            len(eligible)
            * difficulty_percent
            / 100
        )
    )

    return random.sample(
        eligible,
        min(blank_count, len(eligible))
    )


def create_quiz(
    text,
    difficulty_percent=25
):
    """
    Legacy helper.
    Converts text into a numbered fill-in-the-blank quiz.
    """

    words = text.split()

    blank_indices = get_blank_indices(
        words,
        difficulty_percent
    )

    answers = []

    for number, idx in enumerate(
        blank_indices,
        start=1
    ):
        answers.append(
            clean_word(words[idx])
        )

        words[idx] = f"[{number}]"

    return " ".join(words), answers