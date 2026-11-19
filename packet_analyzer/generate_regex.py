def generate_regex_for_full_packet(packet_definition):
    #print(packet_definition)
    regex = ""
    if not packet_definition["contains_variable_lengthed_fields"]:
        for field in packet_definition["fields"]:
            if field["boundary_type"] == "fixed":
                size = field["size_in_bytes"]
                size_in_hex = size*2
                fixed_value:str = field["fixed_value"]
                if field["fixed_value"]:
                    regex += fixed_value.encode().hex()
                else:
                    regex += f"[0-9A-Fa-f]{{{size_in_hex}}}"
        print(regex)
        return regex
    else:
        for field in packet_definition["fields"]:
        #  Case 1: Length Prefixed
            if field["boundary_type"] == "fixed":
                size = field["size_in_bytes"]
                size_in_hex = size*2
                fixed_value:str = field["fixed_value"]
                if field["fixed_value"]:
                    regex += fixed_value.encode().hex()
                else:
                    regex += f"[0-9A-Fa-f]{{{size_in_hex}}}"
            if field["boundary_type"] == "length_prefix":
                current_field_index = packet_definition["fields"].index(field)
                print("I am the variable field at index", current_field_index)
                previous_field = packet_definition["fields"][current_field_index - 1]
                print(previous_field)
                print("Regex rn =",regex)
                return regex
        print(regex)
        return regex
        #  Case 2: Delimiter
        #  Case 3: Remaining
