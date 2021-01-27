import pytest

from evm_asm import assemble, disassemble, evm_opcodes


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
        ("petersburg", "0x00c83aeCC790e8a4453e5dD3B0B4b3680501a7A7"),
        ("byzantium", "0x009ef15C147Ff4C0eB373e1ABD2F4D184e5cb916"),
        ("petersburg", "0x003faFEA71245Cb13171B9fEBfe6121A4d3fF4d1"),
        ("byzantium", "0x0000000000027f6D87be8Ade118d9ee56767d993"),
        ("byzantium", "0x00D53126139c547c7Bd4f4285fc3756c2F081Ab1"),
    ],
)
def test_assembly(w3, evm_version, contract_address):
    evm = evm_opcodes[evm_version]
    code = w3.eth.getCode(contract_address)
    assert assemble(evm, disassemble(evm, code)) == code
