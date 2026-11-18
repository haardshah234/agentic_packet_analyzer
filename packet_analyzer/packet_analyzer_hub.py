from logger.time_logger import time_log
from packet_analyzer.fetch_payloads import fetch_payloads
from packet_analyzer.fetch_clean_packets import fetch_clean_packets
from packet_analyzer.fetch_expected_header import fetch_expected_header
from packet_analyzer.fetch_expected_footer import fetch_expected_footer
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
    #  Determine searching strategy
    #  Use searching strategy and save results. 
    pass

if __name__ == "__main__":
    analyze_packets()