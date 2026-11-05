from langchain_core.documents import Document
from logger.time_logger import time_log
from pathlib import Path
import json

project_root = Path(__file__).parent.parent

@time_log
def jsonify_doc(chunks: list[Document]):
    mydict = {}
    chunk_no = 1
    for chunk in chunks:
        mydict[f"chunk_{chunk_no}"] = {}
        mydict[f"chunk_{chunk_no}"]["id"] = chunk_no
        mydict[f"chunk_{chunk_no}"]["metadata"] = chunk.metadata
        mydict[f"chunk_{chunk_no}"]["page_content"] = chunk.page_content
        chunk_no += 1
    with open(project_root/"jsons/chunks.json","w",encoding="utf-8") as file:
        file.write(json.dumps(mydict, indent=4))