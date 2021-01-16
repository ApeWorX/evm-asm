from dataclasses import dataclass

# TODO https://ethervm.io/
# TODO Make this frozen https://docs.python-guide.org/shipping/freezing/

@dataclass(frozen=True)
class Opcode():
    """Base opcode class."""
    mnemonic: str
    gas_cost: int
    opcode_value: int

    def __str__(self):
        return self.mnemonic
