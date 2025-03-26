import requests
import json
import os
from typing import Dict, Any
from bs4 import BeautifulSoup
import datetime

# Constants
BASE_URL = "https://ekalba.lt"
USER_ENDPOINT = f"{BASE_URL}/action/user"
VOCABULARY_RECORDS_ENDPOINT = f"{BASE_URL}/action/vocabulary/records/public"
OUTPUT_DIR = "output"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_user_data() -> Dict[str, str]:
    """Fetch user cookies from the API."""
    try:
        response = requests.get(USER_ENDPOINT)
        response.raise_for_status()
        return {key: value for key, value in response.cookies.items()}
    except requests.RequestException as e:
        print(f"Error fetching user data: {e}")
        return {}

def fetch_irasai() -> Any:
    """Fetch vocabulary records using cookies."""
    cookies = fetch_user_data()
    if not cookies:
        print("No cookies available. Exiting.")
        return {}

    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "X-XSRF-TOKEN": cookies.get("XSRF-TOKEN", ""),
        "Content-Type": "application/json;charset=utf-8",
    }

    body = {
        "page": 1,
        "pageSize": 25,
        "vocabularyUuid": "0a6409e6-701f-18ab-8170-20311eed0056",
        "viewTypeEnum": 1,
        "orderBy": "publishedDate",
        "sortingOrder": "desc",
    }

    try:
        response = requests.post(VOCABULARY_RECORDS_ENDPOINT, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching vocabulary records: {e}")
        return {}

def parse_html_details(view_html: str) -> Dict[str, Any]:
    """Parse the HTML content and extract details into a dictionary."""
    soup = BeautifulSoup(view_html, "html.parser")
    details = {}

    def parse_section(section_title: str) -> Dict[str, str]:
        section_details = {}
        section = soup.find("h2", string=section_title)
        if section:
            info_section = section.find_next("ul")
            for item in info_section.find_all("li", class_="description_list__items"):
                key = item.find("div", class_="description_list__dt") or item.find("span", class_="description_list__dt")
                value = item.find("div", class_="description_list__dd") or item.find("span", class_="description_list__dd")
                if key and value:
                    section_details[key.text.strip().strip(":")] = value.text.strip()
        return section_details

    # Parse both sections
    details["Bendroji informacija"] = parse_section("Bendroji informacija")
    details["Reikšmė ir vartosena"] = parse_section("Reikšmė ir vartosena")

    return details

def fetch_details(item: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch detailed information for a specific vocabulary item."""
    try:
        response = requests.get(f"{BASE_URL}/action/vocabulary/record/{item['uuid']}?viewType=64")
        response.raise_for_status()
        view_html = response.json()["details"]["viewHtml"]
        return parse_html_details(view_html)
    except requests.RequestException as e:
        print(f"Error fetching details for {item['uuid']}: {e}")
        return {}

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

if __name__ == "__main__":
    irasai = fetch_irasai().get('details', {}).get('list', [])

    for irasas in irasai:
        contents = {
            'uuid': irasas['uuid'],
            'header': irasas['header'],
            'publishedDate': irasas['publishedDate']
        }

        filename = get_filename(irasas)

        if os.path.exists(filename):
            print(f"File {filename} already exists")
            continue

        details = fetch_details(irasas)
        if not details:
            print(f"Failed to fetch details for {contents['header']}")
            continue

        contents['details'] = details
        save_to_file(contents, filename)
