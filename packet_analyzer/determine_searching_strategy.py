from logger.time_logger import time_log

def determine_searching_strategy(field) -> str:
    if field["boundary_type"] == "fixed":
        return "fixed"
    