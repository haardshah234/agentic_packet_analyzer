from logger.colors import *
from logger.time_logger import time_log
from result_generators.generate_report import generate_report
from packet_analyzer.fetch_packet_definitions import fetch_packet_definitions
from packet_analyzer.validate_testcase_datatypes import validate_testcases_datatypes
from testcase_web_interface.server import start_server, wait_for_testcase_submission
from packet_analyzer.match_packets_using_regex import match_packets_using_regex_and_extract_fields
from packet_analyzer.compare_extracted_and_expected_fields import compare_extracted_and_expected_fields
import pprint

@time_log
def analyze_packets(stop_after_first_match=False):
    #stop_after_first_match = True
    #  Open 2 files
    #  1st file: Packet Definitions
    packet_definitions = fetch_packet_definitions()
    server, testcase_queue = start_server(packet_definitions)
    #  Fetch expected field values (Testcases/ITP)            
    expected_fields = wait_for_testcase_submission(server,testcase_queue)
    extracted_fields,metadata = match_packets_using_regex_and_extract_fields(packet_definitions,stop_after_first_match)
    if not expected_fields:
        print("Testcases not found. Nothing to match against.")
        return
    #  Compare and validate
    validate_testcases_datatypes(expected_fields, packet_definitions)
    results = compare_extracted_and_expected_fields(extracted_fields, expected_fields)#, metadata)
    print(crimson)
    #pprint.pp(metadata, indent=4)
    print(metadata)
    print(reset)
    print(electric_blue, packet_definitions, reset)
    print(emerald,extracted_fields,reset)
    print(coral,expected_fields,reset)
    print(f"{gold}{results}{reset}")
    # Generate Reports
    generate_report(expected_fields,extracted_fields,packet_definitions,metadata, results)
    
if __name__ == "__main__":
    analyze_packets()