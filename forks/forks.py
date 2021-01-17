from enum import Enum
from .frontier import Frontier
from .homestead import Homestead
from .tangerine_whistle import TangerineWhistle
from .spurious_dragon import SpuriousDragon
from .byzantium import Byzantium
from .constantinople import Constantinople
from .petersburg import Petersburg
from .istanbul import Istanbul
from .muir_glacier import MuirGlacier


class Fork(Enum):
    Frontier = 1
    Homestead = 2
    TangerineWhistle = 3
    SpuriousDragon = 4
    Byzantium = 5
    Constantinople = 6
    Petersburg = 7
    Istanbul = 8
    MuirGlacier = 9


FORK_OPCODES = {
    Fork.Frontier: Frontier,
    Fork.Homestead: Homestead,
    Fork.TangerineWhistle: TangerineWhistle,
    Fork.SpuriousDragon: SpuriousDragon,
    Fork.Byzantium: Byzantium,
    Fork.Constantinople: Constantinople,
    Fork.Petersburg: Petersburg,
    Fork.Istanbul: Istanbul,
    Fork.MuirGlacier: MuirGlacier,
}


def get(fork):
    """
    Factory method for building forks
    """
    # Type checking
    if not isinstance(fork, Fork):
        raise TypeError("fork must be an instance of Fork Enum")

    return FORK_OPCODES[fork](fork)
