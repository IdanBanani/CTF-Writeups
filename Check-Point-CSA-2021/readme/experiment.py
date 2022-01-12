
def solve():
    d= {}
    new_messed = []
    new_plain = []
    with open("plain.txt") as plain:
        with open("messed.txt") as messed:

            for m_line,p_line in  zip(messed.readlines(),plain.readlines()):
                fixed_line = []
                messed_words = m_line.split(" ")
                plain_words = p_line.split(" ")
                for i,(m,p) in enumerate(zip(messed_words,plain_words)):
                    # correct_word = plain_words[i]
                    if len(m) != len(p):
                        if 'Â' in m:
                            print(len(m), len(p))
                            m = ''.join([c for c in m if c != 'Â'])
                        else:
                            print('1')
                        print(len(m),len(p))
                        messed_words[i] = m + ' '* (len(p)-len(m))

                    fixed_line.append(messed_words[i])
                new_messed.append(' '.join(messed_words))
                new_plain.append(p_line)

    new_messed = ''.join(new_messed)
    new_plain = ''.join(new_plain)
    print("new messed and new plain length: ", len(new_messed),len(new_plain))
                # messed_txt = ' '.join(messed_words)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solve()

