# FLAG is CSA{still_other_of_them_that_are_gone_before}
import re

replacements = {
    'S': ' / ',
    'X': ' '
}

# ' # ' = H
# '# ' = F
# ' #' = B
# ' / ' = S
# ' ' = X

with open('regex.txt') as token:
    pattern = token.read()
    prog = re.compile(pattern)
    with open ('encoded.txt') as encoded:
        text = encoded.read()
        result = prog.findall(text)
        new_res = []
        for answer in result:
            s = answer[:]
            s = [replacements.get(x, x) for x in s]
            new_res.append(''.join(s))

        print('\n#'.join(new_res))