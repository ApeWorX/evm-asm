from .petersburg import Petersburg
from evm_asm.opcode import Opcode


class Istanbul(Petersburg):
    BALANCE = Opcode("BALANCE", 700, 0x31)
    SLOAD = Opcode("SLOAD", 800, 0x54)
    EXTCODEHASH = Opcode("EXTCODEHASH", 700, 0x3F)
    CHAINID = Opcode("CHAINID", 2, 0x46)
    SELFBALANCE = Opcode("SELFBALANCE", 5, 0x47)
