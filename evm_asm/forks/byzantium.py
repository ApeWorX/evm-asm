from .spurious_dragon import SpuriousDragon
from evm_asm.opcode import Opcode


class Byzantium(SpuriousDragon):
    REVERT = Opcode("REVERT", 0, 0xFD)
    RETURNDATASIZE = Opcode("RETURNDATASIZE", 2, 0x3D)
    RETURNDATACOPY = Opcode("RETURNDATACOPY", 3, 0x3E)
    STATICCALL = Opcode("STATICCALL", 700, 0xFA)
