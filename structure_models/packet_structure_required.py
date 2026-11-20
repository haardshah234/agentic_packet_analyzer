from pydantic import BaseModel, model_validator
from typing import Any, Literal

class myPacketField(BaseModel):
    field_name: str
    data_type: Literal["str","int","float"]

    size_in_bytes: int | None
    is_variable_length: bool = False

    is_packet_header: bool = False
    fixed_value: str | int | float | None = None
    #  equation_for_variable_length: str | None = None

    #  Boundary detection for variable-length fields:
    boundary_type: Literal["fixed", "length_prefix", "delimiter", "remaining"] = "fixed"

    #  For length-prefixed fields:
    length_prefix_bytes: int | None = None
    length_prefix_endian: Literal["big", "little"] = "little"
    length_include_prefix: bool | None = None

    #  For delimiter terminated fields:
    delimiter: str | None = None


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
    contains_variable_lengthed_fields: bool
    fields: list[myPacketField]
    assumptions: list[str]

    @model_validator(mode="after")
    def validate_contains_variable_lengthed_fields(self):

        has_variable_field = any( field.boundary_type != "fixed" for field in self.fields )

        if self.contains_variable_lengthed_fields and not has_variable_field:
            raise ValueError(
                "contains_variable_lengthed_fields is True, "
                "but no variable-length fields were found."
            )

        if not self.contains_variable_lengthed_fields and has_variable_field:
            raise ValueError(
                "contains_variable_lengthed_fields is False, "
                "but variable-length fields were found."
            )

        return self

    @model_validator(mode="after")
    def validate_delimiter_field(self):

        for i, field in enumerate(self.fields):

            if field.boundary_type == "delimiter":

                # Ensure a next field exists
                if i + 1 >= len(self.fields):
                    raise ValueError(
                        f"Field '{field.field_name}' uses delimiter boundary, "
                        "but no subsequent delimiter field exists."
                    )

                next_field = self.fields[i + 1]

                # Check if the next field's fixed_value matches the delimiter
                if next_field.fixed_value != field.delimiter:
                    raise ValueError(
                        f"Field '{field.field_name}' specifies delimiter "
                        f"'{field.delimiter}', but the next field "
                        f"'{next_field.field_name}' has fixed_value "
                        f"'{next_field.fixed_value}'."
                    )

        return self


class PacketCollection(BaseModel):
    packets: list[myPacket]
