from logger.colors import *

def validate_testcases_datatypes(testcases,packet_definitions):
    try:
        for defin in packet_definitions:
            packet_name = defin["name"]
            current_testcase = testcases[packet_name]
            for field in defin["fields"]:
                field_name = field["field_name"]
                data_type_str = field["data_type"]
                if data_type_str == "str":
                    data_type = str
                elif data_type_str == "int":
                    data_type = int
                elif data_type_str == "float":
                    data_type = float
                testcase_value = current_testcase[field_name]
                assert isinstance(testcase_value,data_type) == True, f"Packet: {packet_name}, Field: {field_name}, Value: {testcase_value}"
                
    except AssertionError as e:
        print(f"\n{red}You have provided the following testcase with the wrong datatype:{reset}")
        print(f"{orange}{e}{reset}")