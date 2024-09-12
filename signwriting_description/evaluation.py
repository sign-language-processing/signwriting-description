import re
from pathlib import Path
from sacrebleu.metrics import BLEU, CHRF

def get_table_rows(file_path: Path):
    table_rows = re.findall(r"\|.*\|", file_path.read_text())
    table_rows = [row.split("|")[1:-1] for row in table_rows]
    table_rows = [[col.strip() for col in row] for row in table_rows]
    return [row[2] for row in table_rows[2:]]


def main():
    readme_path = Path(__file__).parent.parent / "README.md"
    references = get_table_rows(readme_path)

    print('| Model                        | BLEU | chrF2 |')
    print('|------------------------------|------|-------|')

    results_dir = Path(__file__).parent / "results"
    for result_file in results_dir.glob("*.md"):
        hypothesis = get_table_rows(result_file)
        scores = []
        for metric in [BLEU(), CHRF()]:
            score = metric.corpus_score(hypothesis, [references[:len(hypothesis)]])
            scores.append(f'{score.score:.2f}')

        print('|', result_file.name, '|', ' | '.join(scores), '|')


if __name__ == "__main__":
    main()
