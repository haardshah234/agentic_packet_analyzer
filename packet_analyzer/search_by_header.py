
# def


#         payload:str = pac["tcp.payload"].replace(":","")
#         print(payload) # Hi -> 48:69 -> 4869
#         start_index = payload.find(expected_header_hex)
#         stop_index = payload.find(expected_footer_hex)
#         if start_index < 0:
#             print("Header Not found in payload, skipping to next captured packet...\n...\n\n")
#             continue
#         if stop_index < 0:
#             print("Packet header was observed, but footer was not observed. Plausible snipping of packet.")
#             continue
#         print("Entire Packet was found.")
#         print("Fields:")
        
#         index = 0
#         for field in defin["fields"]:
#             if field["is_variable_length"] == False:
#                 field_size_in_hex_string = field["size_in_bytes"]*2
#                 if field["data_type"] == "str":
#                     print(f"{field["field_name"]} = 0x{payload[:field_size_in_hex_string]} = {bytes.fromhex(payload[:field_size_in_hex_string]).decode()}")
#                 if field["data_type"] == "int":
#                     print(f"{field["field_name"]} = 0x{payload[:field_size_in_hex_string]} = {int(f"0x{payload[:field_size_in_hex_string]}",16)}")
                                    
#                 payload = payload[field_size_in_hex_string:]
#         print("\n\n")
