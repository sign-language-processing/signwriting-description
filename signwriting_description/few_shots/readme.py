import json
from pathlib import Path

if __name__ == "__main__":
    # Load JSON data from the file
    json_file = Path(__file__).parent / "data.json"
    with open(json_file, 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Start the markdown table
    print("| SignWriting | Translation | Description |")
    print("|-------------|-------------|-------------|")

    # Loop through each entry and add to the table
    for entry in data:
        fsw = entry['fsw']
        image_path = entry['image']
        translation = entry['translation']
        description = entry['description']

        # Format the row
        print(f"| ![FSW: {fsw}]({image_path}) | {translation} | {description} |")
