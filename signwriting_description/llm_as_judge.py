import argparse
from enum import Enum
from functools import cache
from pathlib import Path

from pydantic import BaseModel

from signwriting_description.evaluation import get_table_rows
from signwriting_description.gpt_description import _load_conventions, get_openai_client


class ErrorCategory(str, Enum):
    HANDSHAPE = "Handshape"
    PALM_ORIENTATION = "Palm Orientation"
    FINGER_DIRECTION = "Finger Direction"
    LOCATION = "Location"
    CONTACT_GEOMETRY = "Contact Geometry"
    HAND_ROLES = "Hand Roles"
    MOVEMENT_PATH = "Movement Path"
    MOVEMENT_MANNER = "Movement Manner"
    REPETITION = "Repetition"
    NON_MANUAL_SIGNALS = "Non-Manual Signals"
    COMPLETENESS = "Completeness"
    FLUENCY = "Fluency"
    VIEWPOINT = "Viewpoint"


class Severity(str, Enum):
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"


SEVERITY_PENALTIES = {
    Severity.CRITICAL: -15,
    Severity.MAJOR: -10,
    Severity.MINOR: -5,
}


class ErrorAnnotation(BaseModel):
    category: ErrorCategory
    severity: Severity
    explanation: str


class JudgmentResult(BaseModel):
    errors: list[ErrorAnnotation]
    score: int
    reasoning: str


@cache
def judge_prompt() -> str:
    return (
        "You are a SignWriting description evaluator. "
        "Given a reference description and a candidate description of the same sign, "
        "identify errors in the candidate using MQM-style error annotations.\n\n"
        "## Scoring Rubric\n"
        "Start from a base score of 100 and apply penalties:\n"
        "- Critical (-15): Wrong handshape, wrong location, missing hand, inverted viewpoint\n"
        "- Major (-10): Wrong orientation, wrong movement path, missing contact detail\n"
        "- Minor (-5): Slightly imprecise wording, minor fluency issues, unnecessary detail\n\n"
        "The minimum score is 0.\n\n"
        "## Error Categories\n"
        "Handshape, Palm Orientation, Finger Direction, Location, Contact Geometry, "
        "Hand Roles, Movement Path, Movement Manner, Repetition, Non-Manual Signals, "
        "Completeness, Fluency, Viewpoint\n\n"
        f"## Sign Description Conventions\n\n{_load_conventions()}"
    )


def judge_description(reference: str, candidate: str, model: str = "gpt-5.2-2025-12-11") -> JudgmentResult:
    client = get_openai_client()
    response = client.beta.chat.completions.parse(
        model=model,
        temperature=0,
        messages=[
            {"role": "developer", "content": judge_prompt()},
            {"role": "user", "content": f"**Reference:**\n{reference}\n\n**Candidate:**\n{candidate}"},
        ],
        response_format=JudgmentResult,
    )
    result = response.choices[0].message.parsed

    computed_score = 100 + sum(SEVERITY_PENALTIES[e.severity] for e in result.errors)
    result.score = max(0, computed_score)

    return result


def main():
    parser = argparse.ArgumentParser(description="LLM-as-judge evaluation for SignWriting descriptions")
    parser.add_argument("--model", default="gpt-5.2-2025-12-11", help="Judge model to use")
    args = parser.parse_args()

    readme_path = Path(__file__).parent.parent / "README.md"
    references = get_table_rows(readme_path)

    print("| Model | Avg Score | Min | Max |")
    print("|-------|-----------|-----|-----|")

    results_dir = Path(__file__).parent / "results"
    result_files = sorted(results_dir.glob("*.md"))

    for result_file in result_files:
        candidates = get_table_rows(result_file)
        scores = []
        for ref, cand in zip(references, candidates):
            result = judge_description(ref, cand, model=args.model)
            scores.append(result.score)

        avg = sum(scores) / len(scores)
        print(f"| {result_file.name} | {avg:.1f} | {min(scores)} | {max(scores)} |")


if __name__ == "__main__":
    main()
