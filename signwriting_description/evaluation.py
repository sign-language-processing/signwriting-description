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
    result_files = list(results_dir.glob("*.md"))

    # Sort by extracting date from filename (format: model-YYYY-MM-DD.md)
    def get_sort_key(file_path):
        name = file_path.name
        # Extract date part (last 10 characters before .md)
        date_part = name[-13:-3]  # Gets YYYY-MM-DD
        # Extract model name part
        model_part = name[:-14]  # Everything before the date
        return (date_part, model_part)

    result_files.sort(key=get_sort_key)

    for result_file in result_files:
        hypothesis = get_table_rows(result_file)
        scores = []
        for metric in [BLEU(), CHRF()]:
            score = metric.corpus_score(hypothesis, [references[:len(hypothesis)]])
            scores.append(f'{score.score:.2f}')

        print('|', result_file.name, '|', ' | '.join(scores), '|')


if __name__ == "__main__":
    main()
