import re
from logger.colors import *
from logger.time_logger import time_log
from packet_analyzer.fetch_payloads import fetch_payloads
from packet_analyzer.fetch_clean_packets import fetch_clean_packets
from packet_analyzer.generate_regex import generate_regex_for_full_packet
from packet_analyzer.fetch_packet_definitions import fetch_packet_definitions

@time_log
def analyze_packets():
    #  Open 2 files
    #  1st file: Paacket Definitions
    packet_definitions = fetch_packet_definitions()

    #  Fetch packet definition information and expected headers, footers
    for defin in packet_definitions:
        #  2nd file: Cleaned Wireshark Packets
        clean_packet_generator = fetch_clean_packets()
        regex = generate_regex_for_full_packet(defin)
        #print (defin)
        print("Current packet definition being analysed:", defin["name"])

        contains_lp = sum(field["boundary_type"] == "length_prefix" for field in defin["fields"])
        print(f"{defin["name"]} contains lp: {contains_lp}")
        #print("REGEX =",regex)
        #  Fetch payloads with yield.
        regex_copy = regex
        payload_number = 0
        for payload in fetch_payloads(clean_packet_generator):
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
            if re.search(regex, payload):
                print(f"{green}Packet found.{reset}")
            else:
                print(f"{red}Packet wasn't found.{reset}")
                #regex = regex_copy
            #  For every payload, start searching for every field.
    pass

if __name__ == "__main__":
    analyze_packets()