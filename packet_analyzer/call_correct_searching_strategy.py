from logger.time_logger import time_log
from packet_analyzer import search_by_header

def call_correct_searching_strategy(searching_strategy, **kwargs):
    if searching_strategy == "parse_all_fixed_length_fields":
        pass