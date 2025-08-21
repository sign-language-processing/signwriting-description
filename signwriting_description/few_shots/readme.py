import json
from pathlib import Path

from signwriting.visualizer.visualize import signwriting_to_image

if __name__ == "__main__":
    # Load JSON data from the file
    current_dir = Path(__file__).parent
    json_file = current_dir / "data.json"
    with open(json_file, encoding="utf-8") as file:
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

        image = signwriting_to_image(fsw)
        image.save(current_dir.parent.parent / image_path)
