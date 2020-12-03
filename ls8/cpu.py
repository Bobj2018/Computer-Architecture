"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.instructions = {
            "HLT": 0b00000001,
            "LDI": 0b10000010,
            "PRN": 0b01000111
        }


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address,  value):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""
        program = open(file, 'r')
        address = 0

        for line in program:
            if line[0] != "#" and len(line) > 1:
                if "#" in line:
                    self.ram_write(address, int(line.split("#")[0], 2))
                else:
                    self.ram_write(address, int(line[0:len(line) - 1], 2))
            address += 1

        program.close()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b

            if instruction == self.instructions["PRN"]:
                print(self.reg[operand_a])

            if instruction == self.instructions["HLT"]:
                self.running = False

            self.pc += 1



        pass
