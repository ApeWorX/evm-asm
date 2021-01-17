import inspect
import forks.forks as forks
from tests import FORK_OPCODES


def test_forks():
    # for each fork in py-evm
    for key, value in FORK_OPCODES.items():
        # get the according fork from our factory
        fork = forks.get(key)

        # build a list of all of our fork's properties. We'll prune this as we go,
        # and perform a check to ensure we don't have any opcodes that py-evm doesn't
        attributes = inspect.getmembers(fork, lambda a: not (inspect.isroutine(a)))
        evm_opcodes = [
            a[0]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
            and not (a[0] == "Name")
        ]

        assert fork.Name == key

        # for each opcode in py-evm's fork
        for opcode, props in value.items():
            mnemonic = props.mnemonic.upper()

            # check that we have a matching opcode
            assert evm_opcodes.__contains__(
                mnemonic
            ), f"mnemonic {mnemonic} not in evm_opcodes"
            # prune our list
            evm_opcodes.remove(mnemonic)
            # fetch the opcode
            fork_opcode = getattr(fork, mnemonic)

            assert (
                opcode == fork_opcode.opcode_value
            ), f"opcode {mnemonic}'s hex value does not match for {key}"
            assert (
                props.gas_cost == fork_opcode.gas_cost
            ), f"opcode {mnemonic} gas cost does not match for {key}"

        print(*evm_opcodes, sep="\n")
        print(evm_opcodes.__len__())
        assert (
            evm_opcodes.__len__() == 0
        ), f"{key} has an opcode that is not found in py-evm"
