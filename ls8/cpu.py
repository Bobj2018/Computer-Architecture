"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.FL = [0] * 8
        self.IR = 0
        self.running = False
        self.instructions = {
            "HLT": 0b00000001,
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "POP": 0b01000110,
            "PUSH": 0b01000101,
            "CALL": 0b01010000,
            "RET": 0b00010001,
            "ST": 0b10000100,
            "PRA": 0b01001000,
            "IRET": 0b00010011,
            "CMP": 0b10100111,
            "JNE":  0b01010110,
            "JEQ":  0b01010101,
            "JMP":  0b01010100,
        }
        self.reg[7] = 0xF4


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
            num_of_operands = instruction >> 6

            if instruction == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
            elif instruction == self.instructions["PRN"]:
                print(self.reg[operand_a])
            elif instruction == self.instructions["MUL"]:
                self.reg[operand_a] *= self.reg[operand_b]
            elif instruction == self.instructions["PUSH"]:
                self.reg[7] -= 1
                value = self.reg[operand_a]
                self.ram[self.reg[7]] = value
            elif instruction == self.instructions["POP"]:
                SP = self.reg[7]
                value = self.ram[SP]
                self.reg[operand_a] = value
                self.reg[7] += 1
            elif instruction == self.instructions["HLT"]:
                self.running = False
            elif instruction == self.instructions["CALL"]:
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.pc + 2
                self.pc = self.reg[operand_a]
            elif instruction == self.instructions['RET']:
                self.pc = self.ram[self.reg[7]]
            elif instruction == self.instructions['ST']:
                self.ram[self.reg[operand_a]] = self.reg[operand_b]
            elif instruction == self.instructions["PRA"]:
                value = chr(self.ram_read(operand_a))
                print(f"{value}")
            elif instruction == self.instructions["JMP"]:
                self.pc = self.ram_read(operand_a)
            elif instruction == self.instructions["CMP"]:
                if self.ram_read(operand_a) == self.ram_read(operand_b):
                    self.FL[5] = 0  #Less than flag
                    self.FL[6] = 0  #Greater than flag
                    self.FL[7] = 1  #Equals flag
                elif self.ram_read(operand_a) > self.ram_read(operand_b):
                    self.FL[5] = 0
                    self.FL[6] = 1
                    self.FL[7] = 0
                elif self.ram_read(operand_a) < self.ram_read(operand_b):
                    self.FL[5] = 1
                    self.FL[6] = 0
                    self.FL[7] = 0
                num_of_operands += 2
            elif instruction == self.instructions["JEQ"]:
                if self.FL[7] == 1:
                    self.pc = self.ram_read(operand_a)
                else:
                    pass
                    num_of_operands += 1
            elif instruction == self.instructions["JNE"]:
                if self.FL[7] == 0:
                    self.pc = self.ram_read(operand_a)
                else:
                    pass
                    num_of_operands += 1



            sets_pc = ((instruction >> 4) & 0b001) == 0b001

            if not sets_pc:
                self.pc += (1 + num_of_operands)
