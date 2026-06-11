import random


def create_quiz(text, blank_count=5):

    words = text.split()

    valid_indices = []

    for i, word in enumerate(words):

        cleaned = word.strip(".,;:!?\"'()[]")

        if len(cleaned) > 2:
            valid_indices.append(i)

    if not valid_indices:
        return text, []

    blank_indices = random.sample(
        valid_indices,
        min(blank_count, len(valid_indices))
    )

    answers = []

    for number, idx in enumerate(blank_indices, start=1):

        answers.append(
            words[idx].strip(".,;:!?\"'()[]")
        )

        words[idx] = f"[{number}]"

    return " ".join(words), answers