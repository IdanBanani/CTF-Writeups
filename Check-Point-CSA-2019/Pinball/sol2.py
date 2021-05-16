import os

PINBALL_PATH = './pinball.exe'
for i in range(0,7):
    for j in range(0,7):
        for vy in ['+', '-']:
            for vx in ['+', '-']:
                py = str(i)
                px = str(j)
                params = ' transform msg.enc output ' +  py + ' ' + px + ' ' + vy + ' ' + vx
                os.system(PINBALL_PATH + params)

                with open('aggregated_output', 'ab') as f:
                    with open('output', 'rb') as f2:
                        f.write(f2.read())
                        line = str(0) + "\n\n"
                        f.write(line.encode('utf-8'))