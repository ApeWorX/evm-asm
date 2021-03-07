import sys
import pathlib

path = str(pathlib.Path(__file__).absolute().parent.parent)
sys.path.insert(0, path)

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
    "frontier": FRONTIER_OPCODES,
    "homestead": HOMESTEAD_OPCODES,
    "tangerine_whistle": TANGERINE_WHISTLE_OPCODES,
    "spurious_dragon": SPURIOUS_DRAGON_OPCODES,
    "byzantium": BYZANTIUM_OPCODES,
    "constantinople": CONSTANTINOPLE_OPCODES,
    "petersburg": PETERSBURG_OPCODES,
    "istanbul": ISTANBUL_OPCODES,
    "muir_glacier": MUIR_GLACIER_OPCODES,
}

previous_key = ""
previous = "ForkBase"

used_opcodes = {}

for key, value in PY_EVM_FORKS.items():
    split = key.split("_")

    current = "".join(x.title() for x in split)

    original_stdout = sys.stdout
    with open(f"../evm_asm/forks/{key}.py", "w") as f:
        sys.stdout = f

        # If we're on frontier, inherit the base class
        if key == "frontier":
            print("from .fork_base import ForkBase")
        # petersburg is a special case
        elif key == "petersburg":
            print("from .byzantium import Byzantium")
        else:
            print(f"from .{previous_key} import {previous}")

        print("from evm_asm.opcodes.opcode import Opcode")
        print()
        print()

        if key == "petersburg":
            previous = "Byzantium"

        print(f"class {current}({previous}):")

        lines = 0
        for opcode, props in value.items():
            mnemonic = props.mnemonic.upper()
            if mnemonic not in used_opcodes.keys() or used_opcodes[mnemonic] != props.gas_cost:
                print(
                    f'    {mnemonic} = Opcode("{mnemonic}", {props.gas_cost}, {"0x{:02X}".format(opcode)})'
                )
                # don't update if constantinople, petersburg is also based off byzantium and will add them
                if key != "constantinople":
                    used_opcodes[mnemonic] = props.gas_cost
                lines += 1
            else:
                print(f"    {mnemonic} = {previous}.{mnemonic}")
                lines += 1

        if lines == 0:
            print("    pass")

        sys.stdout = original_stdout

    previous = current
    previous_key = key
