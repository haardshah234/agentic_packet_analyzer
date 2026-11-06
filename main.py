from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

from logger.time_logger import time_log
from retriever.file_opener import fetch_irs
from chunker.chunk_document import chunk_docx
from chunker.chunks_to_json import jsonify_doc
from retriever.packet_extractor import extract_packets
from result_generators.save_to_jsons import save_packets_as_json
from result_generators.clean_json_generator import generate_clean_packets

project_root = Path(__file__).parent

@time_log
def main():

    #  IRS Chunking
    #------------
    filepath = fetch_irs()

    chunks = chunk_docx(filepath)

    jsonify_doc(chunks) #For personal verification of chunking.

    #   Extracting the packets in structured format
    response_packets_list = extract_packets(chunks)

    #   Saving the packets in json for ease of future use
    save_packets_as_json(response_packets_list)
    #-----------------------------------------------------

    #  Wireshark Parsing
    #  Expected file: JSON file (<capture>.pcapng opened in Wireshark and exported as JSON.)
    #  O/p file: clean_packets.json in jsons folder
    generate_clean_packets()

    # TODO: Find Packet patterns in clean packets for analysis. Code in packet_analyzer folder.



if __name__ == "__main__":
    main()