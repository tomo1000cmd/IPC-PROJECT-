import cv2
import pickle
import numpy as np
import socket

class ParkingSpaceDetector:
    def __init__(self, video_path, pos_list_path):
        self.cap = cv2.VideoCapture(video_path)
        with open(pos_list_path, 'rb') as f:
            self.posList = pickle.load(f)
        self.width, self.height = 107, 48
        self.spaceCounter = 0

    def checkParkingSpace(self, imgPro):
        self.spaceCounter = 0
        available_spaces = []

        for pos in self.posList:
            x, y = pos

            imgCrop = imgPro[y:y + self.height, x:x + self.width]
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                self.spaceCounter += 1
                available_spaces.append(True)
            else:
                available_spaces.append(False)
    def getSpaceCounter(self):
        return self.spaceCounter
           
    def run(self):
        while True:
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = self.cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16)
            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            self.checkParkingSpace(imgDilate)

            # Send spaceCounter to the client
            server_socket.send(str(self.spaceCounter).encode())
            
            cv2.waitKey(10)

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # Replace with your server IP
port = 1234  # Replace with your desired port
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

# Accept client connections
client_socket, addr = server_socket.accept()
print(f"Client connected: {addr}")

# Initialize the parking space detector
detector = ParkingSpaceDetector('carpark.mp4', 'CarParkPos')
detector.run()






    

   
