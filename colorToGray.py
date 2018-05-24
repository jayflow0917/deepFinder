# 내가 직접 만듦.

import cv2
import os
import numpy as np
from PIL import Image

path = "C:\\Anaconda3\\envs\\venv\\communication\\faces\\poster2"
imagePaths = [os.path.join(path,file_name) for file_name in os.listdir(path)]
count = 0
for imagePath in imagePaths:
    count += 1
    img = Image.open(imagePath)
    img_numpy = np.array(img, 'uint8')
    gray = cv2.cvtColor(img_numpy, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("C:\\Anaconda3\\envs\\venv\\communication\\faces\\poster3\\User.1." + str(count) + ".jpg" , gray)

print("All Done")
