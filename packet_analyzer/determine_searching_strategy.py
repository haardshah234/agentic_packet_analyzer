from logger.time_logger import time_log

def determine_searching_strategy(field) -> str:
    return field["boundary_type"]
    