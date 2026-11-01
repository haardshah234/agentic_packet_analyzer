from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
import time
from structured_docx_loader import DocxLoader

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
    loader = DocxLoader(file_path, mode="sections", table_format="html")
    return loader.load()

chunks = chunk_docx("sample.docx")

def print_third_headings(chunks: list) -> None:
    for chunk in chunks:
        if chunk.metadata["heading_level"] == 3:
            print(chunk.page_content)

