from pydantic import BaseModel
from typing import Any, Literal

class myPacketField(BaseModel):
    field_name: str
    data_type: Literal["str","int","float"]
    size_in_bytes: int | None
    is_variable_length: bool = False
    fixed_value: Any | None
    equation_for_variable_length: str | None

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
