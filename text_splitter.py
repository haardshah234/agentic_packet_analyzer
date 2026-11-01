from langchain_core.documents import Document
import time
from structured_docx_loader import DocxLoader
from dotenv import load_dotenv
load_dotenv()
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def time_log(base_fn:function):
    def timed_fn(*args):
        print(f"Function: {base_fn.__name__} starting...")
        start_time = time.time()
        data = base_fn(*args)
        end_time = time.time()
        print(f"Function: {base_fn.__name__} stopping...\nExecution Time = {end_time - start_time} seconds.\n\n")
        return data
    return timed_fn

@time_log
def chunk_docx(file_path):
    loader:DocxLoader = DocxLoader(file_path, mode="sections", table_format="html")
    return loader.load()

chunks = chunk_docx("sample.docx")

def print_third_headings(chunks: list[Document]) -> None:
    for chunk in chunks:
        if chunk.metadata["heading_level"] == 3:
            print(chunk.page_content)