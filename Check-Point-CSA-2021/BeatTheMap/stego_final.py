#CSA{lEn4_Y0u_aLm0st_fO0l3d_mE}

def triangular_numbers():
     i, t = 1, 0
     # while i <= n
     while True:
         yield t
         t += i
         i += 1

def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

with open('challange_edited.bmp', 'wb') as fixed:
    with open('challenge.bmp', 'rb') as sh:
        gen = triangular_numbers()
        flag_bits =[]
        all = sh.read()
        x= 512*512 + 1024
        header = all[:-x]
        data= all[- x :]
        i=0
        next_n = next(gen)
        while i< len(data):
            if i == next_n:
                dd = data[i]
                flag_bits.append(dd&0x1)
                next_n =next(gen)
            i+=1

        print(frombits(flag_bits))

        # fixed.write(header + data)