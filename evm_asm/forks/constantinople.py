from evm_asm.typing import Opcode

from .byzantium import Byzantium


class Constantinople(Byzantium):
    SHL = Opcode("SHL", 3, 0x1B)
    SHR = Opcode("SHR", 3, 0x1C)
    SAR = Opcode("SAR", 3, 0x1D)
    EXTCODEHASH = Opcode("EXTCODEHASH", 400, 0x3F)
    CREATE2 = Opcode("CREATE2", 32000, 0xF5)
