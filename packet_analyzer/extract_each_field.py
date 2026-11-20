from logger.colors import *
import re

def extract_each_field(regex, payload, packet_definition):
    match = re.match(regex,payload)
    #print(f"{cyan}Extraction:\nFields = {packet_definition["fields"]}\nPayload = {payload}\nRegex={regex}{reset}")
    for field_number,field in enumerate(packet_definition["fields"], start=1):
        extracted_field = match.group(field_number)
        print(coral,field_number, extracted_field, bytes.fromhex(extracted_field).decode(), field["field_name"],reset, sep=" = ")