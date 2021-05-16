rows, cols = ((317,1438))
import cv2
import numpy as np
import os

matrix = np.zeros((rows,cols))
r=0
c=0
count=0

for root, dirs, files in os.walk('../frames'):
    for name in sorted(files):
        frame = os.path.join(root, name)
        im = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
       
        pixel = im[0, 0]
        matrix[r,c]= pixel
        c += 1
        if c == cols:
            c=0
            r += 1
        
        count+=1
        # print(count)

cv2.imwrite('out.png',matrix)




# for frame in glob.glob('frames/*.png'):
    