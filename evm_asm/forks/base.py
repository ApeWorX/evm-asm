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

    def assemble(self, assembly: Assembly) -> Bytecode:
        bytecode = bytearray(b"")
        assembly_iter = iter(assembly)

        for code in assembly_iter:
            if isinstance(code, str):
                code = self[code]  # convert mnemonic to opcode
            elif not isinstance(code, Opcode):
                raise InvalidOpcodeInput(f"'{code}' is not a mnemonic or opcode")

            bytecode.append(code.opcode_value)

            if code.input_size_bytes > 0:
                input_value = next(assembly_iter)
                if not isinstance(input_value, int):
                    raise InvalidOpcodeInput(f"Input must be int, not: '{input_value}'")
                elif 0 <= input_value < 2 ** (8 * code.input_size_bytes):
                    bytecode.extend(
                        (input_value).to_bytes(code.input_size_bytes, "big")
                    )
                else:
                    raise InvalidOpcodeInput(f"Input out of range: '{input_value}'")

        return Bytecode(bytecode)

    def disassemble(self, bytecode: Bytecode) -> Assembly:
        bytecode_iter = iter(bytecode)

        for code in bytecode_iter:
            opcode = self[OpcodeValue(code)]
            yield opcode

            if opcode.input_size_bytes > 0:
                input_bytes = bytes(
                    [next(bytecode_iter) for _ in range(opcode.input_size_bytes)]
                )
                yield int.from_bytes(input_bytes, "big")
