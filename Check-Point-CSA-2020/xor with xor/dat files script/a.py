import os
import glob
import re

pattern = re.compile('(\d+)')
files = glob.glob("*.dat")

files.sort(key=lambda name: int(re.findall(pattern, name)[0]))
# files.sort(key= lambda name1,name2: re.match(pattern))

print(files)

# files = [f for f in os.listdir('.') if os.path.isfile(f)]

for file in files:
    print(file)

with open('out', 'wb') as out_fp:
    combined = b''
    for f in files:
        with open(f, 'rb') as data:
            combined += data.read()

    out_fp.write(combined)
