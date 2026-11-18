from logger.time_logger import time_log

#@time_log
def fetch_expected_footer(packet_definition:dict) -> str:
    expected_footer:str = packet_definition["fields"][-1]["fixed_value"]
    return expected_footer