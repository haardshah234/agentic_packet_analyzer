from pydantic import BaseModel
from typing import Any

class myPacketField(BaseModel):
    field_name: str
    size_in_bytes: int | None
    is_variable_length: bool = False
    fixed_value: Any | None

class myPacket(BaseModel):
    name: str
    from_subsystem: str | None
    to_subsystem: str | None
    reference_section: str | None
    total_size_in_bytes: int | None
    fields: list[myPacketField]
    assumptions: list[str]

class PacketCollection(BaseModel):
    packets: list[myPacket]
