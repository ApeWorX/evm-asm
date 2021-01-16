import forks

class ForkBase:
    def __init__(self, Fork):
        self.Name : Fork = Fork

    #def __getattr__(self, opcode):
        # Is this necessary?
        #if opcode in self.opcodes:
        #    return self.opcodes[opcode]
    #    raise UnsupportedOpcode(self.__name__, opcode)

class UnsupportedOpcode(Exception):
    """Exception raised when a fork doesn't support an opcode.
    """

    def __init__(self, fork_name, opcode, message='fork does not support this opcode.'):
        self.fork_name = fork_name
        self.opcode = opcode
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.opcode} -> {self.fork_name} {self.message}'