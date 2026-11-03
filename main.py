from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

from retriever.file_opener import fetch_irs
from logger.time_logger import time_log
from chunker.chunk_document import chunk_docx
from chunker.chunks_to_json import jsonify_doc
from retriever.packet_extractor import extract_packets
from result_generators.save_to_jsons import save_packets_as_json

project_root = Path(__file__).parent

@time_log
def main():

    filepath = fetch_irs()

    chunks = chunk_docx(filepath)
    
    jsonify_doc(chunks)

    #   Extracting the packets in structured format
    response_packets_list = extract_packets(chunks)

    #   Saving the packets in json for ease of future use
    save_packets_as_json(response_packets_list)


if __name__ == "__main__":
    main()