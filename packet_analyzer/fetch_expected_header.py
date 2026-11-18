from logger.time_logger import time_log

#@time_log
def fetch_expected_header(packet_definition:dict) -> str:
    expected_header:str = packet_definition["fields"][0]["fixed_value"]
    return expected_header