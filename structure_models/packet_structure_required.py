from pydantic import BaseModel, model_validator
from typing import Any, Literal

class myPacketField(BaseModel):
    field_name: str
    data_type: Literal["str","int","float"]

    size_in_bytes: int | None
    is_variable_length: bool = False
    
    fixed_value: Any | None
    equation_for_variable_length: str | None

    #  Boundary detection for variable-length fields:
    boundary_type: Literal["fixed", "length_prefix", "delimiter", "remaining"]

    #  For length-prefixed fields:
    length_prefix_bytes: int | None
    length_prefix_endian: Literal["big", "little"] | None
    length_include_prefix: bool | None

    #  For delimiter terminated fields:
    delimiter: str | None


    #  validation to avoid inconsistent replies.
    @model_validator(mode="after")
    def validate_boundary(self):

        if self.boundary_type == "fixed":
            if self.size_in_bytes is None:
                raise ValueError("Fixed fields requires size_in_bytes")

        elif self.boundary_type == "length_prefix":
            if self.length_prefix_bytes is None:
                raise ValueError("Length-prefixed fields require length_prefix_bytes")

            if self.length_prefix_endian is None:
                raise ValueError("Length-prefixed fields require endianness")

        elif self.boundary_type == "delimiter":
            if self.delimiter is None:
                raise ValueError("Delimiter-terminated fields require a delimiter.")

        return self
    
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
