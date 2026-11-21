from logger.colors import *
from logger.time_logger import time_log
from packet_analyzer.fetch_packet_definitions import fetch_packet_definitions
from packet_analyzer.match_packets_using_regex import match_packets_using_regex_and_extract_fields
from testcase_web_interface.server import start_server, wait_for_testcase_submission
@time_log
def analyze_packets(stop_after_first_match=False):
    #stop_after_first_match = True
    #  Open 2 files
    #  1st file: Packet Definitions
    packet_definitions = fetch_packet_definitions()
    server, testcase_queue = start_server(packet_definitions)
    #  Fetch expected field values (Testcases/ITP)            
    expected_fields = wait_for_testcase_submission(server,testcase_queue)
    extracted_fields = match_packets_using_regex_and_extract_fields(packet_definitions,stop_after_first_match)
    
    print(coral,expected_fields,reset)
    #  Compare and validate
    if not expected_fields:
        print("Testcases not found. Nothing to match against.")
        return
    

if __name__ == "__main__":
    analyze_packets()