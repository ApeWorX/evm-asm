from typing import Dict, Iterator, Optional, Tuple

import re
from collections import OrderedDict


from evm_asm.typing import (
    Assembly,
    Bytecode,
    Metadata,
    Mnemonic,
    Opcode,
    OpcodeLike,
    OpcodeValue,
)


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

        last_opcode = None
        for code in assembly_iter:
            # Check if string literals or metadata included after end of code
            if (
                isinstance(code, bytes)
                and last_opcode
                and last_opcode.opcode_value
                in (
                    0,  # STOP
                    243,  # RETURN
                    253,  # REVERT
                    254,  # INVALID
                )
            ):
                bytecode.extend(code)
                continue  # These are special cases

            elif isinstance(code, str):
                code = self[code]  # convert mnemonic to opcode

            elif not isinstance(code, Opcode):
                raise InvalidOpcodeInput(f"'{code!r}' is not a mnemonic or opcode")

            bytecode.append(code.opcode_value)

            if code.input_size_bytes > 0:
                input_value = next(assembly_iter)
                if (
                    isinstance(input_value, bytes)
                    # bytes must be equal to it's size
                    and len(input_value) == code.input_size_bytes
                ):
                    bytecode.extend(input_value)
                elif (
                    isinstance(input_value, int)
                    # integer must be unsigned and LEQ it's size
                    and 0 <= input_value < 2 ** (8 * code.input_size_bytes)
                ):
                    bytecode.extend(
                        (input_value).to_bytes(code.input_size_bytes, "big")
                    )
                else:
                    raise InvalidOpcodeInput(
                        f"Input must be int or bytes of size '{code.input_size_bytes}',"
                        " not: '{input_value}'"
                    )

            last_opcode = code

        return Bytecode(bytecode)

    def _split_metadata(self, bytecode: Bytecode) -> Tuple[Bytecode, Metadata]:
        # Pattern is `(0xa1|0xa2).*0x00.`, so 2nd to last byte must be 0x00
        if bytecode[-2] != 0:
            return bytecode, Metadata(b"")

        metadata_length = int.from_bytes(bytecode[-1:], "big") + 2
        # 0xa1, 0xa2 are known Solidity metadata start codes
        if bytecode[-metadata_length] in (161, 162):
            return (
                Bytecode(bytecode[:-metadata_length]),
                Metadata(bytecode[-metadata_length:]),
            )
        else:
            return bytecode, Metadata(b"")

    def _split_string_literals(self, bytecode: Bytecode) -> Tuple[Bytecode, bytes]:
        reversed_bytecode = bytearray(bytecode)
        reversed_bytecode.reverse()

        for idx, code in enumerate(reversed_bytecode):
            # Record the last "stop" opcode (a contract must end in one of these)
            if code in (
                0,  # STOP
                243,  # RETURN
                253,  # REVERT
                254,  # INVALID
            ):
                # NOTE: Index is from end of bytecode
                last_stopcode_idx = len(bytecode) - idx

            if code == 0:
                continue  # Could be padding bytes

            # String must be in the printable ASCII range to work in Solidity
            if code not in range(32, 127):
                break

        # Return the code up to the last "stop" opcode prior to a big string sequence
        return Bytecode(bytecode[:last_stopcode_idx]), bytecode[last_stopcode_idx:]

    def get_metadata(self, bytecode: Bytecode) -> Metadata:
        _, metadata = self._split_metadata(bytecode)
        return metadata

    def disassemble(self, bytecode: Bytecode) -> Assembly:
        bytecode, metadata = self._split_metadata(bytecode)
        bytecode, string_literals = self._split_string_literals(bytecode)

        bytecode_iter = iter(bytecode)

        for code in bytecode_iter:
            try:
                opcode = self[OpcodeValue(code)]
            except UnsupportedOpcode as e:
                unprocessed_bytecode = bytes([code, *bytecode_iter])
                raise ValueError(
                    f"Could not parse '0x{unprocessed_bytecode.hex()}'"
                ) from e
            yield opcode

            if opcode.input_size_bytes > 0:
                yield bytes(
                    [next(bytecode_iter) for _ in range(opcode.input_size_bytes)]
                )

        yield string_literals  # String literals are at the end of the code
        yield metadata  # Metadata exists past the end of the code
