import json
from functools import lru_cache

from pathlib import Path

from signwriting.formats.fsw_to_sign import fsw_to_sign
from signwriting.types import SignSymbol


@lru_cache(maxsize=1)
def get_symbol_names():
    current_directory = Path(__file__).parent
    with open(current_directory / "symbols.json", "r", encoding="utf-8") as f:
        return json.load(f)


def describe_symbol(symbol: SignSymbol):
    symbol_names = get_symbol_names()

    # Parse symbol parts
    base_symbol = symbol["symbol"][:4]
    # mod1 = int(symbol["symbol"][4], 16)
    # mod2 = int(symbol["symbol"][5], 16)

    # Get names
    base_name = symbol_names[f"base_{base_symbol}"]
    uni_name = symbol_names[f"uni_{base_symbol}"]

    # pylint: disable=fixme
    # TODO additional modifiers based on category mod1, mod2
    symbol_id = int(base_symbol[1:], 16)
    if symbol_id in range(0x100, 0x205):  # Hand shapes
        pass
    elif symbol_id in range(0x205, 0x221):  # Contact symbols
        pass
    elif symbol_id in range(0x221, 0x2F7):  # Movement paths
        pass
    elif symbol_id in range(0x2F7, 0x2FF):  # Dynamics
        pass
    elif symbol_id in range(0x2FF, 0x30A):  # Head movement
        pass
    elif symbol_id in range(0x30A, 0x36A):  # Facial expressions
        pass
    elif symbol_id in range(0x36A, 0x38C):  # Etc: Limbs, Shoulders, Unique symbols
        pass

    x, y = symbol['position']
    return f"{uni_name} ({base_name}) at x: {x}, y: {y}"


def describe_sign_symbols(fsw: str):
    sign = fsw_to_sign(fsw)

    descriptions = [describe_symbol(symbol) for symbol in sign["symbols"]]
    return "\n".join(descriptions)


if __name__ == '__main__':
    print(describe_sign_symbols("M546x518S2ff00482x483S22f07525x467S15a2f516x482S2fb03506x485"))
