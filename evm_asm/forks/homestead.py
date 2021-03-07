from evm_asm.typing import Opcode

from .frontier import Frontier


class Homestead(Frontier):
    DELEGATECALL = Opcode("DELEGATECALL", 40, 0xF4)
