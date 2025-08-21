import json
from functools import lru_cache
from pathlib import Path

from signwriting.formats.fsw_to_sign import fsw_to_sign
from signwriting.types import SignSymbol


@lru_cache(maxsize=1)
def get_symbol_names():
    current_directory = Path(__file__).parent
    with open(current_directory / "symbols.json", encoding="utf-8") as f:
        return json.load(f)


def describe_symbol(symbol: SignSymbol): # noqa: C901
    symbol_names = get_symbol_names()

    # Parse symbol parts
    base_symbol = symbol["symbol"][:4]
    mod1 = int(symbol["symbol"][4], 16)
    mod2 = int(symbol["symbol"][5], 16)

    # Get names
    base_name = symbol_names[f"base_{base_symbol}"]
    uni_name = symbol_names[f"uni_{base_symbol}"]

    modifier_text = ""

    # pylint: disable=fixme
    # TODO additional modifiers based on category mod1, mod2
    symbol_id = int(base_symbol[1:], 16)
    if symbol_id in range(0x100, 0x205):  # Hand shapes
        directions = {
            0: "palm facing inwards, parallel to the wall",
            1: "palm facing sideways, parallel to the wall",
            2: "palm facing outwards, parallel to the wall",
            3: "palm facing upwards, parallel to the floor",
            4: "palm facing sideways, parallel to the floor",
            5: "palm facing downwards, parallel to the floor",
        }
        handedness = "dominant" if mod2 < 8 else "non-dominant"

        modifier_text = f"{handedness} hand {directions[mod1]}"
    elif symbol_id in range(0x205, 0x221):  # Contact symbols
        if mod1 == 0:
            modifier_text = "few"
        else:
            modifier_text = "many"
    elif symbol_id in range(0x221, 0x2F7):  # Movement paths
        if mod1 == 0:
            modifier_text = "dominant hand"
        elif mod1 == 1:
            modifier_text = "non-dominant hand"
        # Unknwon mod1 in {2,3}
    elif symbol_id in range(0x2F7, 0x2FF):  # Dynamics
        pass
    elif symbol_id in range(0x2FF, 0x30A):  # Head movement
        if symbol_id == 0x300:
            rims = {
                0: "top of the face",
                1: "top left of the face",
                2: "left of the face",
                3: "bottom left of the face",
                4: "bottom of the face",
                5: "bottom right of the face",
                6: "right of the face",
                7: "top right of the face",
            }
            modifier_text = rims[mod2]
    elif symbol_id in range(0x30A, 0x36A):  # Facial expressions
        pass
    elif symbol_id in range(0x36A, 0x38C):  # Etc: Limbs, Shoulders, Unique symbols
        pass

    if symbol_id in range(0x100, 0x2FF):
        rotation = (mod2 % 8) * 45
        if 0 < rotation <= 180:
            modifier_text += f" rotated {rotation} degrees"
        elif 180 < rotation:
            modifier_text += f" rotated {360 - rotation} degrees"

        if mod2 > 0:
            if mod2 < 4 or 12 <= mod2:
                modifier_text += " counter-clockwise"
            else:
                modifier_text += " clockwise"

    x, y = symbol['position']
    description = f"{uni_name} ({base_name})"
    if len(modifier_text) > 0:
        description += f" {modifier_text.strip()}"
    return f"{description} at x: {x}, y: {y}"


def describe_sign_symbols(fsw: str):
    sign = fsw_to_sign(fsw)

    descriptions = [describe_symbol(symbol) for symbol in sign["symbols"]]
    return "\n".join(descriptions)


if __name__ == '__main__':
    print(describe_sign_symbols("M546x518S30007482x483S22f07525x467S15a2f516x482"))
