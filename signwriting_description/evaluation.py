import argparse
import re
from pathlib import Path

from sacrebleu.metrics import BLEU, CHRF


def get_table_rows(file_path: Path):
    table_rows = re.findall(r"\|.*\|", file_path.read_text())
    table_rows = [row.split("|")[1:-1] for row in table_rows]
    table_rows = [[col.strip() for col in row] for row in table_rows]
    return [row[2] for row in table_rows[2:]]


def main():
    parser = argparse.ArgumentParser(description="Evaluate SignWriting descriptions")
    parser.add_argument("--judge-model", default="gpt-5.2-2025-12-11", help="LLM judge model")
    args = parser.parse_args()

    readme_path = Path(__file__).parent.parent / "README.md"
    references = get_table_rows(readme_path)

    print("| Model | BLEU | chrF2 | Judge |")
    print("|-------|------|-------|-------|")

    results_dir = Path(__file__).parent / "results"
    result_files = list(results_dir.glob("*.md"))

    def get_sort_key(file_path):
        name = file_path.name
        date_part = name[-13:-3]
        model_part = name[:-14]
        return (date_part, model_part)

    result_files.sort(key=get_sort_key)

    for result_file in result_files:
        hypothesis = get_table_rows(result_file)

        scores = []
        for metric in [BLEU(), CHRF()]:
            score = metric.corpus_score(hypothesis, [references[:len(hypothesis)]])
            scores.append(f"{score.score:.2f}")

        from signwriting_description.llm_as_judge import judge_description

        judge_scores = []
        for ref, cand in zip(references, hypothesis):
            result = judge_description(ref, cand, model=args.judge_model)
            judge_scores.append(result.score)
        avg_judge = sum(judge_scores) / len(judge_scores)
        scores.append(f"{avg_judge:.1f}")

        print(f"| {result_file.name} | {' | '.join(scores)} |")


if __name__ == "__main__":
    main()
