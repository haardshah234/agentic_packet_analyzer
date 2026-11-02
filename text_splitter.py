from langchain_core.documents import Document
import time
import json
from structured_docx_loader import DocxLoader
from dotenv import load_dotenv
load_dotenv()
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_core.tools.retriever import create_retriever_tool
from langchain_groq import ChatGroq
#from langchain.agents import create_agent
from pydantic import BaseModel
from typing import Any

import os
from pathlib import Path

CHROMA_DIR = Path(os.getenv("CHROMA_PERSIST_DIR"))

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION")

class myPacketField(BaseModel):
    field_name: str
    size_in_bytes: int | None
    is_variable_length: bool = False
    fixed_value: Any | None

class myPacket(BaseModel):
    name: str
    reference_document: str | None
    total_size_in_bytes: int | None
    fields: list[myPacketField]
    assumptions: list[str]

class PacketCollection(BaseModel):
    packets: list[myPacket]

def time_log(base_fn):
    def timed_fn(*args):
        print(f"\x1b[38;2;255;255;0mFunction: {base_fn.__name__} starting...\x1b[0m")
        start_time = time.time()
        data = base_fn(*args)
        end_time = time.time()
        print(f"\x1b[38;2;255;255;0mFunction: {base_fn.__name__} stopping...\n\x1b[38;2;0;64;255mExecution Time = {end_time - start_time} seconds.\x1b[0m\n\n")
        return data
    return timed_fn

@time_log
def chunk_docx(file_path):
    loader:DocxLoader = DocxLoader(file_path, mode="sections", table_format="html")
    return loader.load()


@time_log
def print_third_headings(chunks: list[Document]) -> None:
    for chunk in chunks:
        if chunk.metadata["heading_level"] == 3:
            print(chunk.page_content)

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
    with open("chunks.json","w") as file:
        file.write(json.dumps(mydict, indent=4))

@time_log
def get_section(chunks: list[Document], section_number:float):
    section_content = []
    if section_number == int(section_number):
        section_number = int(section_number)
    for chunk in chunks:
        if chunk.metadata["heading"].startswith(str(section_number)):
            section_content.append(chunk.page_content)
    return "\n\n".join(section_content)
#print_third_headings(chunks)

#jsonify_doc(chunks)
#get_section(chunks, 5.1)

@time_log
def vectorise_chunks(chunks: list[Document]) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PERSIST_DIR, collection_name=CHROMA_COLLECTION)

@time_log
def load_vector_store() -> Chroma:

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    return Chroma(
        collection_name=os.getenv("CHROMA_COLLECTION"),
        embedding_function=embeddings,
        persist_directory=os.getenv("CHROMA_PERSIST_DIR")
    )


def extract_packets(chunks: list[Document]) -> PacketCollection:
    #def extract_packets(vector_store: Chroma) -> PacketCollection:

    # retriever = vector_store.as_retriever(search_kwargs={"k":30})

    # retrieved_docs = retriever.invoke(
    #     """
    #     Find all network packet definitions in the IRS.
    #     Include every distinct packet type, its fields, field sizes, variable-length fields and structural requirements.
    #     """
    # )

    # for i, doc in enumerate(retrieved_docs, 1):
    #     print(f"\n{'=' * 30} CHUNK {i} {'=' * 30}")
    #     print("METADATA:", doc.metadata)
    #     print("CONTENT:", doc.page_content)

    # context = "\n\n".join(
    #     f"Heading: {doc.metadata.get('heading', 'Unknown')}\n"
    #     f"{doc.page_content}"
    #     for doc in retrieved_docs
    # )

    context = get_section(chunks, 3)

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    structured_llm = llm.with_structured_output(PacketCollection)

    response = structured_llm.invoke(
        [
            (
                "system",
                
                """
                You are a senior network protocol engineer.

                Your task is to extract every distinct network packet definition
                from the supplied IRS sections.

                Rules:
                - Extract every distinct packet definition.
                - Never combine different packet types.
                - Extract every field belonging to each packet.
                - Preserve the order of fields as specified in the IRS.
                - Do not invent field names, sizes, offsets or properties.
                - Use null for unspecified field sizes.
                - Mark explicitly variable-length fields as variable.
                - Include the reference section for each packet.
                - Include assumptions only when genuinely necessary.
                - Do not treat examples as separate packet definitions
                unless the IRS explicitly defines them as packet types.
                """

            ),
            ("human", context)
        ]
    )
    #print(f"LLM's response: {response}")
    return response


def main():

    # if CHROMA_DIR.exists():
    #     print("Existing vector store found. Loading...")
    #     vectors = load_vector_store()
    # else:
    #     print("Creating a Chroma vectore store...")
    #     vectors = vectorise_chunks(chunks)

    chunks = chunk_docx("sample_2.docx")
    jsonify_doc(chunks)

    response_packets_list = extract_packets(chunks)
    
    with open("packet.json", "w") as file:
        file.write(response_packets_list.model_dump_json(indent=4))
    print("\x1b[38;2;0;255;64mWritten to packet.json in current directory\x1b[0m")

if __name__ == "__main__":
    main()