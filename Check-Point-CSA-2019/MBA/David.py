import os
import mmap
import glob
import struct

from itertools import permutations
from z3 import *

NUM_OF_BITS = 8


def memory_map(filename, access=mmap.ACCESS_READ):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDONLY)
    return mmap.mmap(fd, size, access=access)


class MBASolver(object):
    EQUAL = '\x8A'  # equal sign encoding
    LAST_LINE_PREFIX = bytes('\x2E'.encode("ascii") * 7)
    RESULT_LENGTH = 8  # calculation result is 8 bytes =64 bit signed integer

    def __init__(self, mmaped):
        self.mmap_obj = mmaped
        self.bytes_left_from_8A_len = self.get_variable_section_length()
        self.first_ending_byte_idx = self.get_last_line_first_byte_index()
        self.num_of_cols_in_equation = self.bytes_left_from_8A_len + len(self.EQUAL) + self.RESULT_LENGTH

    def get_variable_section_length(self):
        for i in range(len(self.mmap_obj)):
            if chr(self.mmap_obj[i]) == self.EQUAL:
                assert (i % 2 == 1)  # 8A column index must be odd
                return i

        raise Exception("Can't find '=' sign ")

    def get_last_line_first_byte_index(self):
        return self.mmap_obj.find(self.LAST_LINE_PREFIX)

    def add_single_equation(self, equation, operators, variables, solver):
        operators[ord(self.EQUAL)] = ""  # add the '=' as ???
        str_equation = ""
        for i in range(0, self.bytes_left_from_8A_len, 2):
            variable = "x{}".format(equation[i])  # x0 x1 x2 x3 ....
            if variable not in variables:
                variables[variable] = BitVec(variable, NUM_OF_BITS)
                # TODO: check - is in ascii.printable
                solver.add(variables[variable] >= ord('!'))
                solver.add(variables[variable] <= ord('~'))
            curr_operator_key = equation[i + 1]
            operator = operators[curr_operator_key]

            # Would be eval-ed later (get item from dictionary)
            str_equation += "{} {} ".format("variables['" + variable + "']", operator)

        # bytes_right_from_8A = equation[self.bytes_left_from_8A_len + 1:]
        # long long, signed 8 bytes integer

        # unpacked =struct.unpack_from('<q', bytes_right_from_8A,offset = self.bytes_left_from_8A_len + 1)
        unpacked = struct.unpack_from('<q', equation, offset=self.bytes_left_from_8A_len + 1)
        result = unpacked[0]
        str_equation += " == {}".format(result)
        evaled_equation_str = eval(str_equation)
        solver.add(evaled_equation_str)

    def solve(self, verbose=False):

        for perm in permutations(["*", "-", "&", "+", "|", "^"], 3):
            solver = Solver()  # Z3 solver object
            # TODO: reset solver, add as class atrribute
            variables = {}  # dict

            x = 0xff  # highest code for operator (0xFF,0xFE,0xFD
            operator_codes = ((0xFF, 0xFE, 0xFD))
            checked_operators = {op: perm for op, perm in zip(operator_codes, perm)}

            # for all lines (of equatios)
            for i in range(0, self.first_ending_byte_idx, self.num_of_cols_in_equation):
                line_bytes = self.mmap_obj[i:i + self.num_of_cols_in_equation]
                self.add_single_equation(line_bytes,
                                         checked_operators,
                                         variables,
                                         solver)

            if solver.check() == sat:
                res = ""
                model = solver.model()
                if verbose:
                    print(model)
                    print(checked_operators)
                for c in self.mmap_obj[self.first_ending_byte_idx + len(self.LAST_LINE_PREFIX):]:
                    c_bitvec = model[variables["x{}".format(c)]]
                    # res += chr(c_bitvec.as_long())
                    as_long = c_bitvec.as_signed_long()
                    res += chr(as_long)
                return res


def solve_for_file(path, verbose=False):
    with memory_map(path) as mmaped_file:
        answer = (MBASolver(mmaped_file)).solve(verbose)

    return answer


def test():
    msg_prefix = "message_"
    bin_prefix = "bin_"
    for msg_file_path in glob.iglob(f'fs/{msg_prefix}*'):
        print("Testing {}".format(msg_file_path))
        with open(msg_file_path) as msg:
            expected = msg.read()
            actual = solve_for_file(msg_file_path.replace(msg_prefix, bin_prefix), False)
            if expected != actual:
                print(f"\t Mismatch: Expected: {expected}, actual {actual}")

    print("All tests done")


if __name__ == "__main__":
    print(solve_for_file("fs/bin_secret", True))
    # test()
