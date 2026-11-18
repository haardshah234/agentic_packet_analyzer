import ijson
from pathlib import Path
from logger.time_logger import time_log
from result_generators.clean_json_generator import clean_packets_relative_path

project_root = Path(__file__).parent.parent
clean_packets_path = project_root / clean_packets_relative_path

@time_log
def fetch_clean_packets():
    with open(clean_packets_path, "rb") as f:
        for item in ijson.items(f, "item"):
            yield item