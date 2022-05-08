import cv2
import socket
import json
import time
import numpy as np

class DaspCarClient():
    def __init__(self, host = "localhost", port = 5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, method, data = ""):
        pack = {
                "Method":method,
                "Data":data
            }
        pack = json.dumps(pack)
        self.sock.sendall(pack.encode())
        time.sleep(0.01)

    def recv(self):
        pack = self.sock.recv(1024)
        if pack:
            pack = json.loads(pack.decode())
        return pack

    def get_state(self):
        self.send("Get state")
        data = self.recv()
        return data["Data"]
        
    def get_collision(self):
        self.send("Get collision")
        data = self.recv()
        return data["Data"]

    def do_action(self, action):
        self.send("Control", action)
        data = self.recv()
        return data["Method"]

    def reset(self):
        self.send("Reset")
        data = self.recv()
        return data["Method"]

    def start_record(self, path =  "D:/Qiyuan/Record"):
        self.send("Start record", path)
        data = self.recv()
        return data["Method"]

    def stop_record(self):
        self.send("Stop record")
        data = self.recv()
        return data["Method"]

def get_image(remote_ip = "127.0.0.1"):
    """
    获取图像数据
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((remote_ip, 5001))
    data, address = sock.recvfrom(65535)
    imgstring = np.asarray(bytearray(data), dtype="uint8")
    image = cv2.imdecode(imgstring, cv2.IMREAD_COLOR)
    sock.close()
    return image

def get_lidar(remote_ip = "127.0.0.1"):
    """
    获取雷达数据
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((remote_ip, 5002))
    data, address = sock.recvfrom(65535)
    points = np.frombuffer(data, dtype=np.dtype('f4'))
    points = np.reshape(points, (int(points.shape[0]/3), 3)) # reshape array of floats to array of [X,Y,Z]
    sock.close()
    return points
