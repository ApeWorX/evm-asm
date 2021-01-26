from typing import Dict, Iterator, Tuple, Union

import re
from collections import OrderedDict


from evm_asm.opcode import Opcode


class UnsupportedOpcode(ValueError):
    """Exception raised when a fork doesn't support an opcode."""


class Fork:
    def __init__(self):
        self._opcodes = OrderedDict()

    @property
    def opcodes(self) -> Dict[str, Opcode]:
        if len(self._opcodes) == 0:
            for opcode in dir(self):
                opcode = getattr(self, opcode)
                if isinstance(opcode, Opcode):
                    self._opcodes[opcode.mnemonic] = opcode

        return self._opcodes

    def _search_opcode_by_value(self, opcode_value: int) -> Opcode:
        for opcode in self.opcodes.values():
            if opcode.opcode_value == opcode_value:
                return opcode

        raise UnsupportedOpcode(
            f"Fork '{self.name} does not support opcode '{opcode_value}'"
        )

    @property
    def name(self):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def __len__(self) -> int:
        return len(self.opcodes)

    def __iter__(self) -> Iterator[Tuple[str, Opcode]]:
        for mnemonic, opcode in self.opcodes.items():
            yield mnemonic, opcode

    def __getitem__(self, opcode_ref: Union[int, str]) -> Opcode:
        if isinstance(opcode_ref, int):
            return self._search_opcode_by_value(opcode_ref)

        opcode_name = opcode_ref.upper()
        if opcode_name in self.opcodes:
            return self.opcodes[opcode_name]
        else:
            raise UnsupportedOpcode(
                f"Fork '{self.name} does not support opcode '{opcode_name}'"
            )
