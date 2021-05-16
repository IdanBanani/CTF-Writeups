import itertools
import subprocess
import os

cartesian_product = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [0, 1, 2, 3, 4, 5, 6],
    ['+', '-'],
    ['+', '-']]

for element in itertools.product(*cartesian_product):
    subprocess.Popen(['./pinball.exe', 'transform', './msg.enc', 'output_{0}.txt'.format(element),
                      "{0}".format(element[0]),
                      "{0}".format(element[1]),
                      "{0}".format(element[2]),
                      "{0}".format(element[3])])

for output_file in os.listdir('outputs'):
    file_content = open('outputs\\' + output_file, 'r').read()
    print("File {0}: {1}".format(output_file, file_content))
