from logger.colors import *
import re

def extract_each_field(match, packet_definition):
    #match = re.match(regex,payload)
    #print(f"{cyan}Extraction:\nFields = {packet_definition["fields"]}\nPayload = {payload}\nRegex={regex}{reset}")
    field_wise_extraction = {}
    for field_number,field in enumerate(packet_definition["fields"], start=1):
        extracted_field = match.group(field_number)
        field_data_type = field["data_type"]
        if field_data_type == "str":
            extracted_field_value = bytes.fromhex(extracted_field).decode()
        elif field_data_type == "float":
            extracted_field_value = float.fromhex(extracted_field)
        elif field_data_type == "int":
            extracted_field_value = int(extracted_field,16)
        else:
            print(f"{red}Unknown datatype found, assuming str...{reset}")
            extracted_field_value = bytes.fromhex(extracted_field).decode()
        field_wise_extraction[field["field_name"]] = extracted_field_value
        #print(coral,field_number, extracted_field, extracted_field_value, field["field_name"], field_data_type ,reset, sep=" = ")
    
    print(lime,packet_definition["name"],reset,sep="",end="\n\n")
    for name,value in field_wise_extraction.items():
        print(f"{lime}{name} = {value}{reset}")
    return field_wise_extraction