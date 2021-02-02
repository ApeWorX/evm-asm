from typing import Dict, Optional, Tuple

from evm_asm.errors import (
    InvalidOpcodeInput,
    UnsupportedOpcode,
)
from evm_asm.typing import (
    Assembly,
    Bytecode,
    Metadata,
    Opcode,
    OpcodeValue,
)
from evm_asm.forks import Fork


END_OPCODES = (
    0x00,  # STOP
    0xF3,  # RETURN
    0xFD,  # REVERT
    0xFE,  # INVALID
)


def assemble(evm: Fork, assembly: Assembly) -> Bytecode:
    bytecode = bytearray(b"")
    assembly_iter = iter(assembly)

    last_opcode = None
    for code in assembly_iter:
        # Check if string literals or metadata included after end of code
        if (
            isinstance(code, bytes)
            and last_opcode
            and last_opcode.opcode_value in END_OPCODES
        ):
            if len(code) > 0:
                bytecode.extend(code)
            continue  # These are special cases

        elif isinstance(code, str):
            code = evm[code]  # convert mnemonic to opcode

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
                bytecode.extend((input_value).to_bytes(code.input_size_bytes, "big"))
            else:
                raise InvalidOpcodeInput(
                    f"Input must be int or bytes of size '{code.input_size_bytes}',"
                    " not: '{input_value}'"
                )

        last_opcode = code

    return Bytecode(bytecode)


def valid_metadata(metadata: bytes) -> bool:
    import cbor2 as cbor  # type: ignore

    try:
        metadata = cbor.loads(metadata[:-2])  # NOTE: Ignore 2 length bytes at end
    except MemoryError:
        return False

    if not isinstance(metadata, dict):
        return False

    if "bzzr0" not in metadata and "solc" not in metadata:
        return False

    return True


def _split_metadata(bytecode: Bytecode) -> Tuple[Bytecode, Optional[Metadata]]:
    # In Solidity, last 2 bytes is the length of the metadata (if applicable)
    metadata_length = int.from_bytes(bytecode[-2:], "big") + 2
    if len(bytecode) < metadata_length:
        # Can't decode metadata with improper length
        return bytecode, None

    elif valid_metadata(bytecode[-metadata_length:]):
        return (
            Bytecode(bytecode[:-metadata_length]),
            Metadata(bytecode[-metadata_length:]),
        )

    else:
        return bytecode, None


def get_metadata(bytecode: Bytecode) -> Dict:
    import cbor2 as cbor  # type: ignore

    _, metadata = _split_metadata(bytecode)
    if metadata:
        return cbor.loads(metadata[:-2])
    else:
        return {}


def _split_string_literals(bytecode: Bytecode) -> Tuple[Bytecode, bytes]:
    reversed_bytecode = bytearray(bytecode)
    reversed_bytecode.reverse()

    for idx, code in enumerate(reversed_bytecode):
        # a contract must end in one of these
        if code in END_OPCODES:
            # NOTE: Index is from end of bytecode
            last_stopcode_idx = len(bytecode) - idx

        if code == 0:
            continue  # Could be padding bytes

        # String must be in the printable ASCII range to work in Solidity
        if code not in range(32, 127):
            break

    # Return the code up to the last "stop" opcode prior to a big string sequence
    return Bytecode(bytecode[:last_stopcode_idx]), bytecode[last_stopcode_idx:]


def disassemble(
    evm: Fork, bytecode: Bytecode, include_metadata: bool = True
) -> Assembly:
    bytecode, metadata = _split_metadata(bytecode)
    bytecode, string_literals = _split_string_literals(bytecode)

    bytecode_iter = iter(bytecode)

    for code in bytecode_iter:
        try:
            opcode = evm[OpcodeValue(code)]
        except UnsupportedOpcode as e:
            unprocessed_bytecode = bytes([code, *bytecode_iter])
            raise ValueError(f"Could not parse '0x{unprocessed_bytecode.hex()}'") from e
        yield opcode

        if opcode.input_size_bytes > 0:
            yield bytes([next(bytecode_iter) for _ in range(opcode.input_size_bytes)])

    if len(string_literals) > 0:
        yield string_literals  # String literals are at the end of the code

    if include_metadata and metadata:
        yield metadata  # Metadata exists past the end of the code
