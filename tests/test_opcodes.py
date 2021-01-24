from evm_asm.forks import get_version


def test_forks(fork_name, fork_expected_opcodes):
    fork_opcodes = get_version(fork_name)
    for opcode_value, opcode in fork_expected_opcodes.items():
        assert (
            getattr(fork_opcodes, opcode.mnemonic.upper())
            == fork_opcodes[opcode.mnemonic]
            == fork_opcodes[opcode_value]
        )
        assert fork_opcodes[opcode.mnemonic].mnemonic == opcode.mnemonic.upper()
        assert fork_opcodes[opcode_value].opcode_value == opcode_value
        assert fork_opcodes[opcode.mnemonic].gas_cost == opcode.gas_cost
