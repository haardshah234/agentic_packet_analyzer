from logger.time_logger import time_log
from langchain_core.documents import Document

@time_log
def print_third_headings(chunks: list[Document]) -> None:
    for chunk in chunks:
        if chunk.metadata["heading_level"] == 3:
            print(chunk.page_content)

@time_log
def get_section(chunks: list[Document], section_number:float):
    section_content = []
    if section_number == int(section_number):
        section_number = int(section_number)
    for chunk in chunks:
        if chunk.metadata["heading"].startswith(str(section_number)):
            section_content.append(chunk.page_content)
    return "\n\n".join(section_content)

