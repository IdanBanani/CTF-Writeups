rows, cols = ((719, 634))

import os
for root, dirs, files in os.walk('/frames'):
    for name in files:
        print (os.path.join(root, name))

# import cv2
# import glob
# import numpy as np

# # matrix = [[]]
# matrix = np.zeros((rows,cols))
# r=0
# c=0
# count=0
# for frame in glob.glob('frames/*.png'):
#     im = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
#     pixel = im[0, 0]
#     matrix[r,c]= pixel
#     c += 1
#     if c == cols:
#       c=0
#       r += 1
#     count+=1
#     print(count)

# cv2.imwrite('out.png',matrix)
