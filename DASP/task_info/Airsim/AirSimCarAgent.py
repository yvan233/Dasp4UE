import airsim
import numpy as np
import os
import time
import cv2
import csv
import sys
import socket
from threading import Thread

class AirSimCarAgent():
    def __init__(self, ip = "", vehicle_name = "", control_flag = False):
        image_size = (84, 84, 1)  # image shape for default gym env
        ## name
        self.name = vehicle_name
        self.recordflag = False
        self.header = ['timestamp', 'position', 'orientation', 'speed', 'throttle', 'steering', 'brake', 
            'linear_velocity', 'linear_acceleration', 'angular_velocity', 'angular_acceleration']
        self.connect(ip, control_flag)

    def connect(self, ip, control_flag):
        ## car client, connect to airsim unreal simulator
        self.car = airsim.CarClient(ip=ip)
        self.car.confirmConnection()
        self.car.enableApiControl(True,self.name) if not control_flag else self.car.enableApiControl(False,self.name)
        self.car.armDisarm(True,self.name) if not control_flag else self.car.enableApiControl(False,self.name)
        time.sleep(0.01)

    def get_car_state(self):
        # 获取车辆状态
        DIG = 4
        State = self.car.getCarState(self.name)
        action = self.car.getCarControls(self.name)
        kinematics = State.kinematics_estimated
        state = {
            "timestamp":str(State.timestamp)[:-6],
            "position":[round(i,DIG) for i in kinematics.position.to_numpy_array().tolist()],
            "orientation":[round(i,DIG) for i in kinematics.orientation.to_numpy_array().tolist()],
            "speed": round(State.speed,DIG),
            "throttle":round(action.throttle,DIG),
            "steering":round(action.steering*50,DIG),
            "brake":round(action.brake,DIG),
            "linear_velocity":[round(i,DIG) for i in kinematics.linear_velocity.to_numpy_array().tolist()],
            "linear_acceleration":[round(i,DIG) for i in kinematics.linear_acceleration.to_numpy_array().tolist()],
            "angular_velocity":[round(i,DIG) for i in kinematics.angular_velocity.to_numpy_array().tolist()],
            "angular_acceleration":[round(i,DIG) for i in kinematics.angular_acceleration.to_numpy_array().tolist()]
        }
        return state

    def get_collision(self):
        collision_info = self.car.simGetCollisionInfo(self.name)
        info = {
            "has_collided":collision_info.has_collided,
            "object_name": collision_info.object_name,
        }
        return info

    def reset(self):
        self.car.reset()

    def do_action(self, action):
        car_controls = airsim.CarControls()
        car_controls.throttle = action["throttle"]
        car_controls.steering = action["steering"]/50
        car_controls.brake = action["brake"]
        if action["throttle"] < 0:
            car_controls.is_manual_gear = True
            car_controls.manual_gear = -1
        self.car.setCarControls(car_controls, self.name)

    def get_image(self):
        img_response = self.car.simGetImage("0", airsim.ImageType.Scene, self.name)
        np_response_image = np.asarray(bytearray(img_response), dtype="uint8")
        decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
        # cv2.imwrite("result.jpg", decoded_frame)
        ret, encoded_jpeg = cv2.imencode('.jpg', decoded_frame)
        data = encoded_jpeg.tobytes()
        image = cv2.imdecode(encoded_jpeg, cv2.IMREAD_COLOR)
        # 解码
        # imgstring = np.asarray(bytearray(data), dtype="uint8")
        # image = cv2.imdecode(imgstring, cv2.IMREAD_COLOR)
        return image, data

    def get_lidar(self):
        lidar_data = self.car.getLidarData("Lidar1", self.name)

        if (len(lidar_data.point_cloud) < 3):
            print("No points received from Lidar data")
            return np.array([])
        else:
            points = np.array(lidar_data.point_cloud, dtype=np.dtype('f4'))
            # data = points.tobytes()
            # 解码
            # points = np.asarray(bytearray(data), dtype=np.dtype('f4'))
            # points =  np.reshape(points, (int(points.shape[0]/3), 3)) # reshape array of floats to array of [X,Y,Z]
            return points


    def startRecording(self, rootpath = "D:/Qiyuan/Record"):
        timelabel = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        self.path = os.path.join(rootpath, timelabel)
        os.system('mkdir "%s"' %self.path) 
        os.system('mkdir "%s"' %self.path+"/pointcloud") 
        os.system('mkdir "%s"' %self.path+"/image") 
        with open(self.path+'/record.csv', 'a', newline='',encoding='utf-8') as f: 
            writer = csv.DictWriter(f,fieldnames=self.header) 
            writer.writeheader()  # 写入列名
        self.recordflag = True

    def stopRecording(self):
        self.recordflag = False

    def upload_video_lidar(self,remote_ip):
        clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            image, data = self.get_image()
            lidar_data = self.get_lidar()
            state = self.get_car_state()
            print(state["timestamp"], sys.getsizeof(data), sys.getsizeof(lidar_data))
            clisocket.sendto(data, (remote_ip, 5001))
            if lidar_data.size:
                clisocket.sendto(lidar_data.tobytes(), (remote_ip, 5002))
            # 如果打开录制
            if self.recordflag:
                time_stamp = state["timestamp"]
                filepath0 = os.path.join(self.path, "record.csv")
                filepath1 = os.path.join(self.path, "pointcloud/pointcloud_" + time_stamp)
                filepath2 = os.path.join(self.path, "image/img_" + time_stamp+".jpg")
                with open(filepath0, 'a', newline='',encoding='utf-8-sig') as f: 
                    writer = csv.DictWriter(f,fieldnames=self.header) 
                    writer.writerow(state) 
                np.save(filepath1, lidar_data)
                cv2.imwrite(filepath2, image)

if __name__ == '__main__':
    # 开启udp视频流
    UE_ip = "59.66.17.186"
    remote_ip = "127.0.0.1"

    record = CarAgent(ip = UE_ip)
    thread = Thread(target=record.upload_video_lidar, args = (remote_ip,), daemon=True)
    thread.start()
    record.startRecording()

    car = CarAgent(ip = UE_ip, vehicle_name= "Escaper")
    print(car.get_car_state())
    print(car.get_collision())
    # 前进
    action = {
        "throttle": 1,
        "steering": 30,
        "brake": 0
    }
    car.do_action(action)
    time.sleep(3)
    # 后退
    action = {
        "throttle": -1,
        "steering": 50,
        "brake": 0
    }
    car.do_action(action)
    time.sleep(3)
    # 刹车
    action = {
        "throttle": 0,
        "steering": 0,
        "brake": 1
    }
    car.do_action(action)
    time.sleep(2)
    car.reset()

    record.stopRecording()