import io
import socket
import struct
import datetime
from PIL import Image

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a "file-like object" out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        # struct. calcsize = Return size in bytes of the struct described by the format string fmt.
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        # print(image_len) # To check length of an image
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)

        # 이름을 넘기기 위해서 이미지를 넘기는 것과 같은 동작을 반복.
        str_len = struct.unpack('<L', connection.read(struct.calcsize('L')))[0]
        str_stream = io.BytesIO()
        str_stream.write(connection.read(str_len))
        str_stream.seek(0)
        face_name = str_stream.read().decode()
        print(face_name)
        # 현재 시각 출력
        date_string = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        # save the image in faces directory with name and time
        image.save("./receiveFace/" + face_name + "-" + date_string + ".jpg")
        # If .verify() finds any problems, it raises suitable exceptions.
        # Otherwise, returns none.
        image.verify()
        print('Image is verified\n')
finally:
    connection.close()
    server_socket.close()