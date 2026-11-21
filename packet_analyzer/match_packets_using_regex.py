import re
from logger.colors import *
from packet_analyzer.fetch_payloads import clean_payload
from packet_analyzer.extract_each_field import extract_each_field
from packet_analyzer.fetch_clean_packets import fetch_clean_packets
from packet_analyzer.fetch_testcases import fetch_testcases
from packet_analyzer.generate_regex import generate_regex_for_full_packet

def match_packets_using_regex_and_extract_fields(packet_definitions,stop_after_first_match):
    for defin in packet_definitions:
            #  2nd file: Cleaned Wireshark Packets
            matches = []
            clean_packet_generator = fetch_clean_packets()
            regex = generate_regex_for_full_packet(defin)
            current_packet_name = defin["name"]
            print("Current packet definition being analysed:", current_packet_name)

            contains_lp = sum(field["boundary_type"] == "length_prefix" for field in defin["fields"])
            print(f"{current_packet_name} contains lp: {contains_lp}")
            #print("REGEX =",regex)
            #  Fetch payloads with yield.
            regex_copy = regex
            payload_number = 0
            for clean_packet in clean_packet_generator:
                unclean_payload = clean_packet["tcp.payload"]
                payload = clean_payload(unclean_payload)
                payload_number += 1
                print(f"{pink}{payload_number}) Payload = {payload}{reset}")
                if contains_lp:
                    # for i in range(contains_lp):
                    regex = regex_copy
                    if re.search(regex,payload):

                        print(regex)
                        lp_size_in_hex = int(re.findall(r"\{(\d+)\}", regex)[-1])
                        print("Size of LP:",lp_size_in_hex)
                        index = re.search(regex,payload).end()
                        value = payload[index-lp_size_in_hex:index]
                        value_in_bytes = int(value,16)
                        print("Value of lp = 0x", value, " = ",value_in_bytes, sep="")
                        #print("Regex before variable field:",regex)
                        regex = generate_regex_for_full_packet(defin,value_in_bytes)
                        #print("Regex after variable field:",regex)
                    else:
                        print("REG EX=",regex)
                        print("Partial Packet wasn't found")
                        continue
                #  For every payload, start searching for every field.
                match = re.search(regex,payload)
                if not match:
                    print(f"{red}Packet wasn't found.{reset}")
                    continue

                matches.append(clean_packet["frame.number"])
                print(f"{green}Packet found.\nDetected fields:{reset}")
                field_wise_extraction = extract_each_field(match, defin)
                print(lavender, field_wise_extraction, reset)
                
                if stop_after_first_match:
                    break
                    #regex = regex_copy
            print("Found in frame numbers:", matches)