from forks.forks import Fork
from eth.vm.forks.frontier.opcodes import FRONTIER_OPCODES
from eth.vm.forks.homestead.opcodes import HOMESTEAD_OPCODES
from eth.vm.forks.tangerine_whistle.opcodes import TANGERINE_WHISTLE_OPCODES
from eth.vm.forks.spurious_dragon.opcodes import SPURIOUS_DRAGON_OPCODES
from eth.vm.forks.byzantium.opcodes import BYZANTIUM_OPCODES
from eth.vm.forks.constantinople.opcodes import CONSTANTINOPLE_OPCODES
from eth.vm.forks.petersburg.opcodes import PETERSBURG_OPCODES
from eth.vm.forks.istanbul.opcodes import ISTANBUL_OPCODES
from eth.vm.forks.muir_glacier.opcodes import MUIR_GLACIER_OPCODES

PY_EVM_FORKS = {
    Fork.Frontier: FRONTIER_OPCODES,
    Fork.Homestead: HOMESTEAD_OPCODES,
    Fork.TangerineWhistle: TANGERINE_WHISTLE_OPCODES,
    Fork.SpuriousDragon: SPURIOUS_DRAGON_OPCODES,
    Fork.Byzantium: BYZANTIUM_OPCODES,
    Fork.Constantinople: CONSTANTINOPLE_OPCODES,
    Fork.Petersburg: PETERSBURG_OPCODES,
    Fork.Istanbul: ISTANBUL_OPCODES,
    Fork.MuirGlacier: MUIR_GLACIER_OPCODES,
}
