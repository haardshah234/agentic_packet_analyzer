def generate_regex_for_full_packet(packet_definition, variable_field_size_in_bytes=None) -> str:
    #print(packet_definition)
    regex = ""
    if not packet_definition["contains_variable_lengthed_fields"]:
        for field in packet_definition["fields"]:
            if field["boundary_type"] == "fixed":
                size = field["size_in_bytes"]
                size_in_hex = size*2
                fixed_value:str = field["fixed_value"]
                if field["fixed_value"]:
                    regex += f"({fixed_value.encode().hex()})"
                else:
                    regex += f"([0-9A-Fa-f]{{{size_in_hex}}})"
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
                    regex += f"({fixed_value.encode().hex()})"
                else:
                    regex += f"([0-9A-Fa-f]{{{size_in_hex}}})"
            if field["boundary_type"] == "length_prefix":
                if variable_field_size_in_bytes:
                    prefix_size_in_bytes = field["length_prefix_bytes"]
                    include_prefix = field["length_include_prefix"]
                    if include_prefix:
                        print("Subtracting the size of prefix length...")
                        variable_field_size_in_bytes = variable_field_size_in_bytes - prefix_size_in_bytes
                    variable_field_size_in_hex = variable_field_size_in_bytes * 2
                    regex += f"([0-9A-Fa-f]{{{variable_field_size_in_hex}}})"
                else:
                    print("Regex rn =",regex)
                    return regex
            #  Case 2: Delimiter
            if field["boundary_type"] == "delimiter":
                delimiter = field["delimiter"]
                regex += r"([0-9A-Fa-f]+)"
            
            #  Case 3: Remaining
            if field["boundary_type"] == "remaining":
                regex += r"([0-9A-Fa-f]+)"
        print("This Regex", regex)
        return regex
