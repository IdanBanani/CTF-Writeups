#bytearray.fromhex(hex(89490564489314326449816467341755769981)[2:])
#bytearray(b'CSA{cs@5s3mbl3d}')
import operator

def twos_complement(val, bits=8):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def get_reg_idx(val):
    return (val & 0x0F) - 0xA

def parse_regs(val):
    dest = (val >> 4 ) & 0x0F
    src = val & 0x0F
    return get_reg_idx(dest),get_reg_idx(src)

ops = {0xAB :operator.add ,0xBA :operator.sub,
        0xCD : operator.mul , 0xDC : operator.truediv}

regs_state = [0]*6

with open('flag', 'rb') as f:
    while True:

        opcode,regs = f.read(2)
        if opcode == 0:
            break

        if opcode in ops:
            dest,src = parse_regs(regs)
            operation = ops[opcode]
            if operation == operator.truediv:
                regs_state[dest] = regs_state[dest] // regs_state[src]
            else:
                regs_state[dest] = operation(regs_state[dest],regs_state[src])
            print(f'{operation} {dest},{src} res={ regs_state[dest] }'.ljust(60),end='\t')
            print(regs_state)
        elif 0x1A <= opcode <= 0x1F:
            i = get_reg_idx(opcode)
            val = regs
            regs_state[i] = val
            # print(f'mov ${i},{val}'.ljust(30), end='\t')
            print(regs_state)
        else:
            continue


    # print([((hex(t[0]),t[1])) for t in Counter(data).items()])
