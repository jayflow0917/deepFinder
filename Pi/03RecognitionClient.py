import cv2
import numpy as np
import os
import io
import socket
import struct
import time
from PIL import Image

# Connect a client socket to server IP:8000
client_socket = socket.socket()
client_socket.connect(('192.168.137.2', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

# Construct a stream to hold image data temporarily 
# (we could write it directly to connection but in this
# case we want to find out the size of each capture first 
# to keep our protocol simple)
stream = io.BytesIO()
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer.read('trainer/trainer_alone.yml') # alone
    recognizer.read('trainer/trainer_Lteam.yml') # Lteam
    #recognizer.read('trainer/trainer_IRENE.yml') # IRENE
    #recognizer.read('trainer/trainer_poster.yml') # poster
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0

    # names related to ids: example ==> Yeongjin: id=1,  etc
        # alone
    #names = ['None', 'Gian84', 'Henry', 'Hyejin', 'Hyunmu', 'Narae', 'Siun']
        # Lteam
    names = ['None', 'Yeongjin', 'Jihye']
        # IRENE
    #names = ['None', 'IRENE']
        # poster
    #names = ['Jihye', 'Yeongjin']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, img =cam.read()
        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                # if confidence is less than 60, send face image to server
                if (confidence < 60): # update number 100 to other later
                    # convert opencv frame (with type()==numpy) into PIL Image
                    pil_img = Image.fromarray(img)
                    # convert PIL Image to Bytes
                    pil_img.save(stream, format='jpeg')
                    # Write the length of the capture to the stream 
                    # and flush to ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()

                    # Send image name(label, time, location, etc.)
                    # In order to write string on a stream, should 
                    # convert string to bytes object using by encode()
                    stream.write(names[id].encode())
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    stream.seek(0)
                    connection.write(stream.read())
                    stream.seek(0)
                    stream.truncate()
                
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                                                                    
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()
