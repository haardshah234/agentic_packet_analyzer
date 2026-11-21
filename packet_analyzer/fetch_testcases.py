import json
from pathlib import Path

testcases_relative_filepath = "jsons/testcases.json"
project_root = Path(__file__).parent.parent

testcases_filepath = project_root / testcases_relative_filepath

def fetch_testcases() -> dict:

    with open(testcases_filepath, "r", encoding="utf-8") as file:
        expected_fields = json.load(file)

    return expected_fields