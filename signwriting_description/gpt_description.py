import os
from functools import lru_cache
from io import BytesIO
import json
import base64
from pathlib import Path

from openai import OpenAI
from PIL import Image

from signwriting.visualizer.visualize import signwriting_to_image

from signwriting_description.naive_description import describe_sign_symbols

SYSTEM_PROMPT = """
This tool automatically describes SignWriting images in spoken languages.
The description is sign language agnostic, making it useful for teaching SignWriting to learners.
You are a SignWriting expert, and you will be asked to describe a SignWriting image in English.

Input:
- A SignWriting image.
- A naive description of the sign, outlining the different symbols.

Output:
- A brief description of the sign, outlining the hand movements, facial expressions, and body language involved.
""".strip()


def image_base64(fsw: str):
    rgba_image = signwriting_to_image(fsw)
    rgb_image = Image.new("RGB", (128, 128), (255, 255, 255))
    rgb_image.paste(rgba_image, (0, 0), rgba_image)

    buffered = BytesIO()
    rgb_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


@lru_cache(maxsize=None)
def create_user_message(fsw: str):
    return {
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64(fsw)}"}},
            {"type": "text", "text": describe_sign_symbols(fsw)},
        ],
    }


@lru_cache(maxsize=1)
def few_shots():
    data_path = Path(__file__).parent / "few_shots/data.json"
    with open(data_path, 'r', encoding="utf-8") as file:
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


def describe_sign(fsw: str):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + few_shot_messages(exclude=fsw)

    # Add the specific sign
    messages.append(create_user_message(fsw))

    # Call OpenAI GPT-4 for image caption
    response = get_openai_client().chat.completions.create(
        model="gpt-4-vision-preview",
        temperature=0,
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    for shot in few_shots():
        print(shot['translation'] + ' | ' + describe_sign(shot['fsw']))
