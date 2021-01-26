from dataclasses import dataclass
from typing import Iterable, Optional, NewType, Union


# TODO https://ethervm.io/

Bytecode = NewType("Bytecode", bytes)

Mnemonic = NewType("Mnemonic", str)
OpcodeCost = NewType("OpcodeCost", int)
OpcodeValue = NewType("OpcodeValue", int)


# TODO Make this frozen https://docs.python-guide.org/shipping/freezing/
@dataclass(frozen=True)
class Opcode:
    """Base opcode class."""

    # NOTE: Union is done so constructor doesn't throw typing issues
    mnemonic: Union[Mnemonic, str]
    gas_cost: Union[OpcodeCost, int]
    opcode_value: Union[OpcodeValue, int]
    input_size_bytes: int = 0

    def __str__(self):
        return f"{self.mnemonic}"

    def serialize(self, input_value: Optional[int] = None) -> Bytecode:
        input_bytes = b""
        if self.input_size_bytes > 0:
            assert input_value, "Must have value"
            assert (
                0 <= input_value < 2 ** self.input_size_bytes
            ), "Value outside of range"
            input_bytes = input_value.to_bytes(self.input_size_bytes, "little")

        return Bytecode(bytes(self.opcode_value) + input_bytes)


OpcodeLike = Union[Opcode, Mnemonic, OpcodeValue]
Assembly = Iterable[Union[OpcodeLike, int]]
