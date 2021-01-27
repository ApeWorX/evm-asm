from .frontier import Frontier
from evm_asm.typing import Opcode


class Homestead(Frontier):
    DELEGATECALL = Opcode("DELEGATECALL", 40, 0xF4)
