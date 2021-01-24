from .homestead import Homestead
from evm_asm.opcode import Opcode


class TangerineWhistle(Homestead):
    BALANCE = Opcode("BALANCE", 400, 0x31)
    EXTCODESIZE = Opcode("EXTCODESIZE", 700, 0x3B)
    EXTCODECOPY = Opcode("EXTCODECOPY", 700, 0x3C)
    SLOAD = Opcode("SLOAD", 200, 0x54)
    CALL = Opcode("CALL", 700, 0xF1)
    CALLCODE = Opcode("CALLCODE", 700, 0xF2)
    SELFDESTRUCT = Opcode("SELFDESTRUCT", 5000, 0xFF)
    DELEGATECALL = Opcode("DELEGATECALL", 700, 0xF4)
