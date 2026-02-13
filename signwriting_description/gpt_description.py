import argparse
import base64
import json
import os
from functools import cache, lru_cache
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from signwriting.visualizer.visualize import signwriting_to_image

from signwriting_description.naive_description import describe_sign_symbols

# Load environment variables from .env file
load_dotenv()

SYSTEM_PROMPT_INTRO = (
    "You are a SignWriting expert. "
    "Given a SignWriting image and its naive technical description "
    "(symbol names, positions, movements, rotations), "
    "write a concise, paragraph-style English description of the sign. "
    "Your response must be continuous prose, not a list or bullet points."
)


def _load_conventions() -> str:
    conventions_path = Path(__file__).parent / "CONVENTIONS.md"
    return conventions_path.read_text(encoding="utf-8")


@cache
def system_prompt() -> str:
    return f"{SYSTEM_PROMPT_INTRO}\n\n{_load_conventions()}"


def image_base64(fsw: str):
    rgba_image = signwriting_to_image(fsw)
    # Add at least 5 pixels padding on all sides
    width = rgba_image.width + 10
    height = rgba_image.height + 10
    # make sure image dimensions are even
    width += width % 2
    height += height % 2
    # While 68x68 is the minimum size, GPT rescales images.
    # For consistent images sizes, we use a 256x256 minimum, at the same cost
    width = max(width, 256)
    height = max(height, 256)
    # Create the new image
    rgb_image = Image.new("RGB", (width, height), (255, 255, 255))
    box = ((width - rgba_image.width) // 2, (height - rgba_image.height) // 2)
    rgb_image.paste(rgba_image, box, rgba_image)

    buffered = BytesIO()
    rgb_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


@cache
def create_user_message(fsw: str):
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": describe_sign_symbols(fsw)},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64(fsw)}", "detail": "low"}},
        ],
    }


@lru_cache(maxsize=1)
def few_shots():
    data_path = Path(__file__).parent / "few_shots/data.json"
    with open(data_path, encoding="utf-8") as file:
        return json.load(file)


def few_shot_messages(exclude=None):
    messages = []
    for entry in few_shots():
        if exclude is not None and entry['fsw'] == exclude:
            continue
        messages.append(create_user_message(entry['fsw']))
        messages.append({"role": "assistant", "content": entry['description']})

    return messages


@lru_cache(maxsize=1)
def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY", None)
    return OpenAI(api_key=api_key)


def describe_sign(fsw: str, model="gpt-4o-2024-08-06"):
    messages = [{"role": "developer", "content": system_prompt()}] + few_shot_messages(exclude=fsw)

    # Add the specific sign
    messages.append(create_user_message(fsw))

    # Call OpenAI GPT-4 for image caption
    response = get_openai_client().chat.completions.create(
        model=model,
        temperature=0 if model.startswith("gpt-4") else 1,
        seed=42,
        messages=messages
    )

    return response.choices[0].message.content.replace('\n', ' ').strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate descriptions for SignWriting')
    parser.add_argument('--model', default='gpt-4o-2024-08-06', help='OpenAI model to use')
    args = parser.parse_args()

    print("| SignWriting | Translation | Description |")
    print("|-------------|-------------|-------------|")

    for shot in few_shots():
        print(f"| ![FSW: {shot['fsw']}]({shot['image']}) | "
              f"{shot['translation']} | {describe_sign(shot['fsw'], model=args.model)} |")
