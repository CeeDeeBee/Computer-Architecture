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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        running = True

        # op functions
        def HLT():
            nonlocal running
            running = False

        def LDI(reg_addr, val):
            self.reg[reg_addr] = val
            self.pc += 3

        def PRN(reg_addr):
            print(self.reg[reg_addr])
            self.pc += 2

        # op code hash table
        op_codes = {
            0b00000001: HLT,
            0b10000010: LDI,
            0b01000111: PRN
        }

        while running:
            # get current instruction
            IR = self.ram_read(self.pc)

            # get potential operands
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # run op
            op_func = op_codes[IR]
            func_params = signature(op_func).parameters
            if len(func_params) == 1:
                op_func(operand_a)
            elif len(func_params) == 2:
                op_func(operand_a, operand_b)
            else:
                op_func()
