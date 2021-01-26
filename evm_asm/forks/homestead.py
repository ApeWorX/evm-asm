from .frontier import Frontier
from evm_asm.opcode import Opcode


class Homestead(Frontier):
    DELEGATECALL = Opcode("DELEGATECALL", 40, 0xF4)
