from logger.time_logger import time_log
from packet_analyzer.fetch_payloads import fetch_payloads
from packet_analyzer.fetch_clean_packets import fetch_clean_packets
from packet_analyzer.fetch_expected_header import fetch_expected_header
from packet_analyzer.fetch_expected_footer import fetch_expected_footer
from packet_analyzer.fetch_packet_definitions import fetch_packet_definitions
from packet_analyzer.determine_searching_strategy import determine_searching_strategy
from packet_analyzer.implement_searching_strategy import implement_searching_strategy

@time_log
def analyze_packets():
    #  Open 2 files
    #  1st file: Paacket Definitions
    packet_definitions = fetch_packet_definitions()

    #  Fetch packet definition information and expected headers, footers
    for defin in packet_definitions:
        #  2nd file: Cleaned Wireshark Packets
        clean_packet_generator = fetch_clean_packets()
        #print (defin)
        print("Current packet definition being analysed:", defin["name"])

        # Header-fetching
        expected_header:str = fetch_expected_header(defin)
        if not expected_header:
            print("This packet doesn't contain a header. Cannot match.")
            continue
        print(f"Expected header found: {expected_header} = {expected_header.encode().hex()}")
        #print(expected_header)
        expected_header_hex = expected_header.encode().hex()

        # Footer-fetching
        expected_footer:str = fetch_expected_footer(defin)
        if not expected_footer:
            print("Packet doesn't contain a footer, cannot match.")
            continue
        print(f"Expected footer found: {expected_footer} = {expected_footer.encode().hex()}")
        expected_footer_hex = expected_footer.encode().hex()
        print()
    #  Fetch payloads with yield.
        for payload in fetch_payloads(clean_packet_generator):
            print(payload)
            #  For every payload, start searching for every field.
            results = {}
            for field in defin["fields"]:
                searching_strategy = determine_searching_strategy(field)
                #print(searching_strategy)
                #  Implement respective searching strategy
                result,payload = implement_searching_strategy(searching_strategy,field,payload)
                results[field["field_name"]] = result
            if not result: continue
        if any(result == False for result in results.values()):
            print("\x1b[38;2;255;20;0mPacket Analysis Failed.\x1b[0m")
        else:
            print("\x1b[38;2;20;255;0mFull Packet Found.\x1b[0m")      
    #  Save results. 
    pass

if __name__ == "__main__":
    analyze_packets()