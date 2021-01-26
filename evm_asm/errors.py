class UnsupportedOpcode(ValueError):
    """Exception raised when a fork doesn't support an opcode."""


class InvalidOpcodeInput(ValueError):
    """Exception raised when am opcode doesn't support the given input."""
