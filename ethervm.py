from flask import Flask
from flask_table import Col, Table  # type: ignore
from web3.auto.infura.goerli import w3 as goerli_w3
from web3.auto.infura.kovan import w3 as kovan_w3
from web3.auto.infura.mainnet import w3 as mainnet_w3
from web3.auto.infura.rinkeby import w3 as rinkeby_w3
from web3.auto.infura.ropsten import w3 as ropsten_w3

from evm_asm import LATEST_VERSION, disassemble, evm_opcodes
from evm_asm.typing import Bytecode

AVAILABLE_WEB3 = {
    "mainnet": mainnet_w3,
    "ropsten": ropsten_w3,
    "rinkeby": rinkeby_w3,
    "kovan": kovan_w3,
    "goerli": goerli_w3,
}

app = Flask(__name__)


class OpcodeTable(Table):
    opcode_value = Col("Opcode Value")
    mnemonic = Col("Mnemonic")
    gas_cost = Col("Gas Cost")
    input_size_bytes = Col("Input Size (in bytes)")


@app.route("/")
@app.route("/<evm_version>")
def show_table(evm_version: str = LATEST_VERSION.name):
    if evm_version not in evm_opcodes.forks():
        return ""
    opcodes = [
        dict(
            opcode_value=f"{op.opcode_value:02x}",
            mnemonic=mnemonic,
            gas_cost=op.gas_cost,
            input_size_bytes=op.input_size_bytes,
        )
        for mnemonic, op in evm_opcodes[evm_version]
    ]
    implemented_opcodes = set(op.opcode_value for _, op in evm_opcodes[evm_version])
    opcodes.extend(
        [
            dict(
                opcode_value=f"{opcode_value:02x}",
                mnemonic="",
                gas_cost="",
                input_size_bytes="",
            )
            for opcode_value in (set(range(256)) - implemented_opcodes)
        ]
    )

    def sort_opcodes(opcode):
        return opcode["opcode_value"]

    opcodes.sort(key=sort_opcodes)
    table = OpcodeTable(opcodes)
    return table.__html__()


@app.route("/disassemble/<contract_address>")
@app.route("/disassemble/<contract_address>/<network>")
@app.route("/disassemble/<contract_address>/<network>/<evm_version>")
def show_assembly(
    contract_address: str,
    network: str = "mainnet",
    evm_version: str = LATEST_VERSION.name,
):
    if network not in AVAILABLE_WEB3:
        return "Invalid network"

    if evm_version not in evm_opcodes.forks():
        return "Not Valid EVM Version"

    hexcode = AVAILABLE_WEB3[network].eth.getCode(contract_address)
    bytecode = Bytecode(hexcode)

    def convert_to_string(o):
        if isinstance(o, int):
            return f"0x{hex(o)}"
        elif isinstance(o, bytes):
            return f"0x{o.hex()}"
        else:
            return str(o)

    return "\n".join(convert_to_string(o) for o in disassemble(evm_opcodes[evm_version], bytecode))
