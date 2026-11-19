from logger.time_logger import time_log
from logger.colors import *

def search_fixed_field(field,payload):
    fixed_value:str = field["fixed_value"]
    size = field["size_in_bytes"]
    is_header = field["is_packet_header"]
    if size:
        size_in_hex = size * 2
    if is_header:
        fixed_value_hex = fixed_value.encode().hex()
        start_index = payload.find(fixed_value_hex)
        if start_index < 0:
            return -1
        return start_index
    else:
        try:
            snippet = payload[size_in_hex-1]
            return 0
        except IndexError:
            print("Fixed field incomplete. Plausible snipping of packet.")
            return -1

def search_length_prefixed_field(field, payload):
    field_boundary_type = field["boundary_type"]
    

    

def implement_searching_strategy(searching_strategy,field,payload):
    field_name = field["field_name"]
    size = field["size_in_bytes"]
    print(f"Field name: {field_name} | Size = {size} | Strategy = {searching_strategy}")
    if size:
        size_in_hex = size * 2
    #print("Size =", size, payload)
    if searching_strategy == "fixed":
        print(f"Searching '{field_name}' over a fixed number of bytes...")
        index = search_fixed_field(field, payload)
        if index < 0:
            return False, payload
        else:
            print(f"{field_name} found at {index}")
            snippet_hex:str = payload[index:index+size_in_hex]
            snippet = bytes.fromhex(snippet_hex).decode()
            expected_fixed_value = field["fixed_value"]
            if expected_fixed_value:
                if snippet != expected_fixed_value:
                    print("Some bytes found, but they donot match the fixed value.")
                    return False, payload
            payload = payload[index+size_in_hex:]
            print(f"Snippet = {snippet_hex} = {snippet},\nSnipped payload = {payload} = {bytes.fromhex(payload).decode()}")
            return True, f"{payload}"
    if searching_strategy == "length_prefix":
        print(f"{orange}Perform Length-prefix analysis here.{reset}")

    return False,payload