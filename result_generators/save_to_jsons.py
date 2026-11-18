from structure_models.packet_structure_required import PacketCollection
from pathlib import Path

project_root = Path(__file__).parent.parent
packet_definitions_relative_path = "jsons/packet_definitions.json"

def save_packets_as_json(response_packets_list: PacketCollection):
    with open(project_root/packet_definitions_relative_path, "w", encoding="utf-8") as file:
        file.write(response_packets_list.model_dump_json(indent=4))
        print(f"\x1b[38;2;0;255;64mWritten to packet_definitions.json in 'jsons' folder of project root.\x1b[0m\n\n")