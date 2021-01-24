from typing import Union

from enum import Enum

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


class EvmVersion(Enum):
    FRONTIER = 1
    HOMESTEAD = 2
    TANGERINE_WHISTLE = 3
    SPURIOUS_DRAGON = 4
    BYZANTIUM = 5
    CONSTANTINOPLE = 6
    PETERSBURG = 7
    ISTANBUL = 8
    MUIR_GLACIER = 9

    @classmethod
    def get_version(cls, version_name: str) -> "EvmVersion":
        for name, val in cls.__members__.items():
            if version_name.upper() == name:
                return val

        versions = (f.lower() for f in cls.__members__.keys())
        raise TypeError(
            f"'{version_name}' is not a valid fork name, must be one of '{versions}'"
        )


EVM_VERSIONS = {
    EvmVersion.FRONTIER: Frontier,
    EvmVersion.HOMESTEAD: Homestead,
    EvmVersion.TANGERINE_WHISTLE: TangerineWhistle,
    EvmVersion.SPURIOUS_DRAGON: SpuriousDragon,
    EvmVersion.BYZANTIUM: Byzantium,
    EvmVersion.CONSTANTINOPLE: Constantinople,
    EvmVersion.PETERSBURG: Petersburg,
    EvmVersion.ISTANBUL: Istanbul,
    EvmVersion.MUIR_GLACIER: MuirGlacier,
}
LATEST_VERSION = EvmVersion.MUIR_GLACIER


def get_version(version: Union[str, EvmVersion] = LATEST_VERSION) -> Fork:
    """
    Factory method for building forks
    """
    if isinstance(version, str):
        version = EvmVersion.get_version(version)

    if isinstance(version, EvmVersion):
        return EVM_VERSIONS[version]()
    else:
        raise TypeError("fork must be an instance of Fork Enum")
