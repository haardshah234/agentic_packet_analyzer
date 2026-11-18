import json

from pathlib import Path
from result_generators.save_to_jsons import packet_definitions_relative_path

project_root = Path(__file__).parent.parent
packet_definitions_path = project_root / packet_definitions_relative_path

def fetch_packet_definitions():
    with open(packet_definitions_path) as f:
        definitions = json.load(f)["packets"]
    return definitions