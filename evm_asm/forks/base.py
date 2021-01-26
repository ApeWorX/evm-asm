from typing import Dict, Iterator, Tuple

import re
from collections import OrderedDict


from evm_asm.typing import Assembly, Bytecode, Mnemonic, Opcode, OpcodeLike, OpcodeValue


class UnsupportedOpcode(ValueError):
    """Exception raised when a fork doesn't support an opcode."""


class InvalidOpcodeInput(ValueError):
    """Exception raised when am opcode doesn't support the given input."""


class Fork:
    INVALID = Opcode("INVALID", 0, 0xFE)  # Designated invalid (see EIP 141)

    def __init__(self):
        self._opcodes = OrderedDict()

    @property
    def opcodes(self) -> Dict[Mnemonic, Opcode]:
        if len(self._opcodes) == 0:
            for opcode in dir(self):
                opcode = getattr(self, opcode)
                if isinstance(opcode, Opcode):
                    self._opcodes[opcode.mnemonic] = opcode

        return self._opcodes

    def _search_opcode_by_value(self, opcode_value: OpcodeValue) -> Opcode:
        for opcode in self.opcodes.values():
            if opcode.opcode_value == opcode_value:
                return opcode

        raise UnsupportedOpcode(
            f"Fork '{self.name}' does not support opcode '0x{opcode_value:02x}'"
        )

    @property
    def name(self):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def __len__(self) -> int:
        return len(self.opcodes) - 1  # Ignore INVALID opcode

    def __iter__(self) -> Iterator[Tuple[Mnemonic, Opcode]]:
        for mnemonic, opcode in self.opcodes.items():
            yield mnemonic, opcode

    def __getitem__(self, opcode_ref: OpcodeLike) -> Opcode:
        if isinstance(opcode_ref, Opcode):
            return opcode_ref
        elif isinstance(opcode_ref, int):
            return self._search_opcode_by_value(opcode_ref)
        elif isinstance(opcode_ref, str):
            opcode_name = Mnemonic(opcode_ref.upper())
            if opcode_name in self.opcodes:
                return self.opcodes[opcode_name]
            else:
                raise UnsupportedOpcode(
                    f"Fork '{self.name}' does not support opcode '{opcode_name}'"
                )
        else:
            raise TypeError(f"Unsupported type '{type(opcode_ref)}'")
