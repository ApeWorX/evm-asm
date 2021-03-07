from evm_asm.typing import Opcode

from .spurious_dragon import SpuriousDragon


class Byzantium(SpuriousDragon):
    REVERT = Opcode("REVERT", 0, 0xFD)
    RETURNDATASIZE = Opcode("RETURNDATASIZE", 2, 0x3D)
    RETURNDATACOPY = Opcode("RETURNDATACOPY", 3, 0x3E)
    STATICCALL = Opcode("STATICCALL", 700, 0xFA)
