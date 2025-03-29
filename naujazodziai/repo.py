import os, json, datetime
from typing import Dict, Any

OUTPUT_DIR = "output"

def save_to_file(data: Dict[str, Any], filename: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Writing {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

def get_filename(irasas: Dict[str, Any]) -> str:
    """Generate a filename based on the publication date and UUID."""
    timestamp = irasas['publishedDate'] / 1000
    date_str = datetime.datetime.fromtimestamp(timestamp, datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    return os.path.join(OUTPUT_DIR, f"{date_str}-{irasas['uuid']}.json")

def load_json_dir(directory: str):
    """
    Reads all JSON files in the specified directory.
    """
    data_list = []
    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            data_list.append(data)
    return data_list
