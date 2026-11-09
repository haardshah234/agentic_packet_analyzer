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


# Seach every definition on by one
 # Search every packet for matching definiton

print("\nheaders:")
for defin in definitions:
    header = defin["fields"][0]["field_name"]
    expected_header:str = defin["fields"][0]["fixed_value"]
    expected_footer:str = defin["fields"][-1]["fixed_value"]
    print()
    print(defin)
    print()
    #print(header)
    print()
    if not expected_header:
        print("Packet doesn't contain a header, cannot match.")
        continue
    else:
        print(f"Expected header found: {expected_header}\n{expected_header.encode().hex()}")
    if not expected_footer:
        print("Packet doesn't contain a footer, cannot match.")
        continue
    else:
        print(f"Expected footer found: {expected_footer}\n{expected_footer.encode().hex()}")
    expected_header_hex = expected_header.encode().hex()
    expected_footer_hex = expected_footer.encode().hex()
    print("payloads:")
    for pac in packets:
        payload:str = pac["tcp.payload"].replace(":","")
        print(payload) # Hi -> 48:69 -> 4869
        start_index = payload.find(expected_header_hex)
        stop_index = payload.find(expected_footer_hex)
        if start_index < 0:
            print("Header Not found in payload, skipping to next captured packet...")
            continue
        if stop_index < 0:
            print("Packet header was observed, but footer was not observed. Plausible snipping of packet.")
            continue
        print("Entire Packet was found.")
        print("Fields:")
        
        index = 0
        for field in defin["fields"]:
            if field["is_variable_length"] == False:
                field_size_in_hex_string = field["size_in_bytes"]*2
                if field["data_type"] == "str":
                    print(f"{field["field_name"]} = 0x{payload[:field_size_in_hex_string]} = {bytes.fromhex(payload[:field_size_in_hex_string]).decode()}")
                payload = payload[field_size_in_hex_string:]
        print("\n\n")
