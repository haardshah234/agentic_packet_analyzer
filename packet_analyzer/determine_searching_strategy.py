from logger.time_logger import time_log

def determine_searching_strategy(packet_definition) -> str:
    if not packet_definition["contains_variable_lengthed_fields"]:
        return "parse_all_fixed_length_fields"
    else:
        variable_field_types = [{field["field_name"]:field["boundary_type"]} for field in packet_definition["fields"] if field["boundary_type"] != "fixed"][0]
        if len(variable_field_types.keys()) == 1:
            #print(variable_field_types)
            val = next(iter(variable_field_types.values()))
            return f"parse_single_var_field_of_type_{val}"
        return variable_field_types