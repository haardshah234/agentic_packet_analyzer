from structure_models.packet_structure_required import PacketCollection
from langchain_core.documents import Document
from chunker.fetch_chunks import get_section
from logger.time_logger import time_log
from langchain_groq import ChatGroq
from functools import lru_cache

@time_log
def extract_packets(chunks: list[Document]) -> PacketCollection:
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
    return response