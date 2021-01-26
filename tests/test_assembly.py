import pytest

from evm_asm.forks import get_version


# NOTE: Pick the fork the contracts were compiled with
@pytest.mark.parametrize(
    "evm_version,contract_address",
    [
        ("istanbul", "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"),
        ("byzantium", "0xdAC17F958D2ee523a2206206994597C13D831ec7"),
        ("muir_glacier", "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"),
        ("muir_glacier", "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"),
        ("constantinople", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),
        ("petersburg", "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"),
    ],
)
def test_assembly(w3, evm_version, contract_address):
    evm = get_version(evm_version)
    code = w3.eth.getCode(contract_address)
    assert evm.assemble(evm.disassemble(code)) == code
