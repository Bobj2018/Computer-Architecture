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
            "PRN": 0b01000111,
            "MUL": 0b10100010
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
            split_line = line.split("#")[0].strip()

            if split_line != "":
                command = int(split_line, 2)
                self.ram_write(address, command)
            address += 1

        program.close()
        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            operands = 0

            if instruction == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
                operands = 2
            elif instruction == self.instructions["PRN"]:
                print(self.reg[operand_a])
                operands = 1
            elif instruction == self.instructions["MUL"]:
                operands = 2
                self.reg[operand_a] *= self.reg[operand_b]
            elif instruction == self.instructions["HLT"]:
                self.running = False

            self.pc += (1 + operands)
pass
