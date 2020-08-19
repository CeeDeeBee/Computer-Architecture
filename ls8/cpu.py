"""CPU functionality."""

import sys
from inspect import signature


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP
        }
        self.running = True
        self.sp = 7
        self.reg[self.sp] = 244

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Error: incorrect usage")
            print("Please enter in format: python ls8.py filename")
            sys.exit(1)

        filename = sys.argv[1]

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # remove comments and whitespace
                    b = line.split("#")[0].strip()

                    # skip if line is empty
                    if b == '':
                        continue

                    d = int(b, 2)
                    self.ram[address] = d
                    address += 1

        except FileNotFoundError:
            print(f"File {filename} not found.")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            val = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = val
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, addr, val):
        self.ram[addr] = val

    # op functions
    def HLT(self):
        self.running = False

    def LDI(self, reg_addr, val):
        self.reg[reg_addr] = val
        self.pc += 3

    def PRN(self, reg_addr):
        print(self.reg[reg_addr])
        self.pc += 2

    def MUL(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)

    def PUSH(self, reg_addr):
        self.sp -= 1
        self.ram[self.sp] = self.reg[reg_addr]
        self.pc += 2

    def POP(self, reg_addr):
        self.reg[reg_addr] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.running:
            # get current instruction
            IR = self.ram_read(self.pc)

            # get potential operands
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # run op
            op_func = self.branchtable[IR]
            func_params = signature(op_func).parameters
            if len(func_params) == 1:
                op_func(operand_a)
            elif len(func_params) == 2:
                op_func(operand_a, operand_b)
            else:
                op_func()
