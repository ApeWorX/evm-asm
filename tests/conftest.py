import pytest

from eth.vm import forks as pyevm_forks


@pytest.fixture(
    params=[
        "frontier",
        "homestead",
        "tangerine_whistle",
        "spurious_dragon",
        "byzantium",
        "constantinople",
        "petersburg",
        "istanbul",
        "muir_glacier",
    ]
)
def fork_name(request):
    yield request.param


@pytest.fixture
def fork_expected_opcodes(fork_name):
    opcodes_module = getattr(pyevm_forks, fork_name).opcodes
    yield getattr(opcodes_module, f"{fork_name.upper()}_OPCODES")
