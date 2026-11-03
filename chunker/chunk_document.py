from structured_docx_loader import DocxLoader
from logger.time_logger import time_log

@time_log
def chunk_docx(file_path):
    loader:DocxLoader = DocxLoader(file_path, mode="sections", table_format="html")
    chunks = loader.load()
    return chunks