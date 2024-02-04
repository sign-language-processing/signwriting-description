import re
from pathlib import Path
from sacrebleu.metrics import BLEU, CHRF


def main():
    readme_path = Path(__file__).parent.parent / "README.md"

    table_rows = re.findall(r"\|.*\|", readme_path.read_text())
    table_rows = [row.split("|")[1:-1] for row in table_rows]
    table_rows = [[col.strip() for col in row] for row in table_rows]

    references = [description for _, _, description in table_rows[:len(table_rows) // 2][2:]]
    hypothesis = [description for _, _, description in table_rows[len(table_rows) // 2:][2:]]

    for metric in [BLEU(), CHRF()]:
        score = metric.corpus_score(hypothesis, [references])
        print(metric.get_signature(), score)


if __name__ == "__main__":
    main()
