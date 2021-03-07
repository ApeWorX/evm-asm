from typing import Iterator

from .base import Fork

from .frontier import Frontier
from .homestead import Homestead
from .tangerine_whistle import TangerineWhistle
from .spurious_dragon import SpuriousDragon
from .byzantium import Byzantium
from .constantinople import Constantinople
from .petersburg import Petersburg
from .istanbul import Istanbul
from .muir_glacier import MuirGlacier


class EvmForks:
    FRONTIER = Frontier()
    HOMESTEAD = Homestead()
    TANGERINE_WHISTLE = TangerineWhistle()
    SPURIOUS_DRAGON = SpuriousDragon()
    BYZANTIUM = Byzantium()
    CONSTANTINOPLE = Constantinople()
    PETERSBURG = Petersburg()
    ISTANBUL = Istanbul()
    MUIR_GLACIER = MuirGlacier()

    def forks(self) -> Iterator[str]:
        for attr in dir(self):
            if isinstance(getattr(self, attr), Fork):
                yield attr.lower()

    def __iter__(self) -> Iterator[Fork]:
        forks = [getattr(self, f.upper()) for f in self.forks()]
        forks.sort()
        return iter(forks)

    def __len__(self) -> int:
        return len(list(self.forks()))

    def __getitem__(self, fork_name: str) -> Fork:
        forks = tuple(self.forks())
        if fork_name in forks:
            return getattr(self, fork_name.upper())

        raise TypeError(f"'{fork_name}' is not a valid fork name, must be one of '{forks}'")


evm_opcodes = EvmForks()
LATEST_VERSION = evm_opcodes.MUIR_GLACIER


__all__ = [
    "LATEST_VERSION",
    "Fork",
    "evm_opcodes",
]
