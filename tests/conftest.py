import pytest
from eth.vm import forks as pyevm_forks

from evm_asm import evm_opcodes


@pytest.fixture(scope="session")
def w3():
    from web3.auto.infura.mainnet import w3

    yield w3


@pytest.fixture(params=[*evm_opcodes.forks()])
def fork_name(request):
    yield request.param


@pytest.fixture
def fork_expected_opcodes(fork_name):
    opcodes_module = getattr(pyevm_forks, fork_name).opcodes
    yield getattr(opcodes_module, f"{fork_name.upper()}_OPCODES")
