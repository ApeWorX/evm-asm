from .byzantium import Byzantium
from evm_asm.opcode import Opcode


class Petersburg(Byzantium):
    SHL = Opcode("SHL", 3, 0x1B)
    SHR = Opcode("SHR", 3, 0x1C)
    SAR = Opcode("SAR", 3, 0x1D)
    EXTCODEHASH = Opcode("EXTCODEHASH", 400, 0x3F)
    CREATE2 = Opcode("CREATE2", 32000, 0xF5)
