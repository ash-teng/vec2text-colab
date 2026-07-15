import json
import random
import re
from collections import Counter
from pathlib import Path


DATASET_DIR = Path(__file__).parent
SOURCE_PATH = DATASET_DIR / "500_python_code_alpaca_references.json"
SEED = 42
OUTPUT_PATHS = {
    "prefix": DATASET_DIR / "500_python_code_alpaca_number_prefix_seed42.json",
    "middle": DATASET_DIR / "500_python_code_alpaca_number_middle_seed42.json",
    "suffix": DATASET_DIR / "500_python_code_alpaca_number_suffix_seed42.json",
}


def insert_at_middle(text, number):
    """Insert before the middle whitespace-delimited token without changing the text."""
    tokens = list(re.finditer(r"\S+", text))
    if not tokens:
        return str(number)

    insertion_point = tokens[len(tokens) // 2].start()
    return f"{text[:insertion_point]}{number} {text[insertion_point:]}"


def main():
    references = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    assert isinstance(references, list), "source dataset must be a JSON list"
    assert len(references) == 500, len(references)
    assert all(isinstance(text, str) and text.strip() for text in references)
    assert len(set(references)) == len(references), "duplicate source questions found"

    rng = random.Random(SEED)
    numbers = [rng.randint(1, 10) for _ in references]

    datasets = {
        "prefix": [f"{number} {text}" for text, number in zip(references, numbers)],
        "middle": [insert_at_middle(text, number) for text, number in zip(references, numbers)],
        "suffix": [f"{text} {number}" for text, number in zip(references, numbers)],
    }

    for position, questions in datasets.items():
        assert len(questions) == len(references)
        assert len(set(questions)) == len(questions), f"duplicates found in {position} dataset"
        OUTPUT_PATHS[position].write_text(
            json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"Source questions: {len(references)}")
    print(f"Random seed: {SEED}")
    print(f"Number counts: {dict(sorted(Counter(numbers).items()))}")
    for position, path in OUTPUT_PATHS.items():
        print(f"{position}: {path.name}")
        print(f"  first: {datasets[position][0]}")


if __name__ == "__main__":
    main()
