from evm_asm.typing import Opcode

from .petersburg import Petersburg


class Istanbul(Petersburg):
    BALANCE = Opcode("BALANCE", 700, 0x31)
    SLOAD = Opcode("SLOAD", 800, 0x54)
    EXTCODEHASH = Opcode("EXTCODEHASH", 700, 0x3F)
    CHAINID = Opcode("CHAINID", 2, 0x46)
    SELFBALANCE = Opcode("SELFBALANCE", 5, 0x47)
