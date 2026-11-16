#  TODO after getting wireshark captures JSON
#  Fetch payload from packet <-- I can modularise this out :)
import json
from pathlib import Path

project_root = Path(__file__).parent.parent

with open(project_root / "jsons/clean_packets.json","r") as f:
    packets = json.load(f)

for pac in packets:
    print(pac)
    print("\n\n\n")

with open(project_root / "jsons/packet_definitions.json", "r") as f:
    definitions = json.load(f)["packets"]

for pac in definitions:
    print(pac)
    print("\n\n\n")
    #print(pac["fields"][0]["field_name"])



#  For every packet, Loop through every field
for defin in definitions:
    #  For every field, if any field's boundary_type is length_prefix, try to parse packet, otherwise suggest to use a different strategy.
    correct_boundary_type = any([field["boundary_type"] == "length_prefix" for field in defin["fields"]])
    if correct_boundary_type:
        print(f"\n{defin["name"]}:")
        #  Parse Header and Footer to chip off excessive bytes.
        expected_header:str = defin["fields"][0]["fixed_value"]
        expected_footer:str = defin["fields"][-1]["fixed_value"]
        if not expected_header:
            print("This packet doesn't contain a header. Cannot match.")
            continue
        else:
            print("Expceted header:", expected_header)
            print("Expceted header in hex:", expected_header.encode().hex())
        if not expected_footer:
            print("This packet doesn't contain a footer. Cannot match.")
            continue
        else:
            print("Expected footer:", expected_footer)
            print("Expected footer in hex:", expected_footer.encode().hex())

        expected_header_hex = expected_header.encode().hex()
        expected_footer_hex = expected_footer.encode().hex()
        for pac in packets:
            payload:str = pac["tcp.payload"].replace(":","")
            print("Payload:",payload)
            start_index = payload.find(expected_header_hex)
            stop_index  = payload.find(expected_footer_hex)
            if start_index < 0:
                print("Header not found in payload, skipping to next catured packet...\n...\n\n")
                continue
            if stop_index < 0:
                print("Packet header was observed, but footer was not observed. Plausible snipping of packet.")
                continue
            print("Entire packet was found.")

            # stripped_payload = payload[start_index+len(expected_header_hex):stop_index]
            # print("Stripped Payload =", stripped_payload)
            #print(defin["fields"][1:-1])
            for field in defin["fields"]:#[1:-1]:
                #  Now, parse every fixed length field bw Hdr and Ftr
                if field["is_variable_length"] == False:
                    field_size_in_hex_string = field["size_in_bytes"] * 2
                    if field["data_type"] == "str":
                        print(f"{field["field_name"]} = 0x{payload[:field_size_in_hex_string]} = {bytes.fromhex(payload[:field_size_in_hex_string]).decode()}")
                    if field["data_type"] == "int":
                        print(f"{field["field_name"]} = 0x{payload[:field_size_in_hex_string]} = {int(f"0x{payload[:field_size_in_hex_string]}",16)}")
                    payload = payload[field_size_in_hex_string:]
                
                #  When a variable length field is encountered, check its prefix bytes.
                else:
                    print("This is a variable lengthed field.")
                    prefix_bytes = field["length_prefix_bytes"]
                    print("Length of prefix bytes =", prefix_bytes)
                    payload = payload[20:]
            print("\n\n")
        #  Jump back those many bytes, read those many bytes and typecast the length into int.
        #  If prefix bytes are included, jump those bytes before reading.
        #  Continue parsing other fixed bytes until footer.
        #  If everything goes right, print Packet found! and display all fields.
    else:
        print(f"\nThis packet namely '{defin["name"]}' is not defined to have a length-prefixed field. Please use a different startegy.\n")    

    #print(f"{defin["name"]}: {correct_boundary_type}")