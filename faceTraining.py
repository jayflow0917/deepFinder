import cv2
import numpy as np
from PIL import Image
import os

# 사진은 고화질일수록 (픽셀 값이 높을수록) 좋다.

# Path for face image database
path = 'faces\\poster3'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Cascades\\haarcascade_frontalface_default.xml");
# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        width, height = PIL_img.size
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # openface를 이용하여 얻은 사진은 꽉찬 얼굴사진이라서 detecMultiScale()로 얼굴을
        # 검출해내지 못함. 그러므로 좌표를 직접 지정하기로 함.
        # detectMultiScale()을 이용하여 얼굴의 x,y,w,h를 얻어오지 않고 직접 (0,0), (width,height)로
        # 좌표를 지정하여 faceSamples에 추가.
        #faces = detector.detectMultiScale(img_numpy)
        #for (x,y,w,h) in faces:
        faceSamples.append(img_numpy[0:height, 0:width])
        ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)

# To Check
#for face in faces:
#    print(face)
#print("============")
#print(np.array(ids))
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer_alone.yml
recognizer.save("trainer\\trainer_poster.yml") # recognizer.save() worked on Mac, but not on Pi
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
