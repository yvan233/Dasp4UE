import airsim
import numpy as np
import sys
sys.path.insert(1,".")
from Agent.AirSimUavAgent import AirSimUavAgent
import math
import time

def calculateVelocity(x_d, y_d, leader_state, follower_state):
    min_velocity = 0.01
    max_velocity = 5.0
    # 机体坐标系下目标位置
    X_d = np.array([[x_d],[y_d]])
    # 旋转矩阵
    yaw_l = leader_state["orientation"][2]
    yaw_f = follower_state["orientation"][2]
    R_b_e = np.array([[math.cos(yaw_l), -math.sin(yaw_l)],[math.sin(yaw_l), math.cos(yaw_l)]])
    R_e_b = np.array([[math.cos(yaw_l), math.sin(yaw_l)],[-math.sin(yaw_l), math.cos(yaw_l)]])

    X_l = np.array([[leader_state["position"][0]], [leader_state["position"][1]]])
    X_f = np.array([[follower_state["position"][0]], [follower_state["position"][1]]])
    
    X_err = R_e_b@(X_f - X_l)
    omega = X_d - X_err
    Vel = R_b_e@omega

    V_l = np.array([[leader_state["linear_velocity"][0]], [leader_state["linear_velocity"][1]]])
    Vel += V_l

    # if np.linalg.norm(Vel) < min_velocity:
    #     pass
    # if np.linalg.norm(Vel) > max_velocity:
    #     Vel = Vel/np.linalg.norm(Vel)*max_velocity

    if yaw_l-yaw_f > math.pi/2:
        yaw_rate = 45
    elif yaw_l-yaw_f < -math.pi/2:
        yaw_rate = -45
    else:
        yaw_rate = 45*math.sin(yaw_l-yaw_f)
    v_x_f, v_y_f = Vel[0][0], Vel[1][0]
    return v_x_f, v_y_f, yaw_rate

UE_ip = "127.0.0.1"
origin_geopoint = (116.16872381923261, 40.05405620434274,150)

leader = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav0", origin_pos=[0, 0, -2])
follower1 = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav1", origin_pos=[0, 3, -2])
follower2 = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav2", origin_pos=[-3, 0, -2])
# 初始化，建立连接
leader.take_off()      # 起飞
leader.move_to_position(0,0,-10,3)

follower1.take_off()      # 起飞
follower1.move_to_position(0,3,-10,3)

follower2.take_off()      # 起飞
follower2.move_to_position(-3,0,-10,3,waited=True)

x_d = -3*math.cos(math.pi/3)
y_d = 3*math.sin(math.pi/3)

# 生成队形
while True:
    leader_state = leader.get_state()
    follower1_state = follower1.get_state()
    follower2_state = follower2.get_state()

    z = leader_state["position"][2]
    v1_x, v1_y, yaw1_rate = calculateVelocity(x_d, y_d, leader_state, follower1_state)
    v2_x, v2_y, yaw2_rate = calculateVelocity(x_d, -y_d, leader_state, follower2_state)

    follower1.move_by_velocity_z(v1_x, v1_y, z, duration = 0.2, yaw_mode=airsim.YawMode(True, yaw1_rate))
    follower2.move_by_velocity_z(v2_x, v2_y, z, duration = 0.2,  yaw_mode=airsim.YawMode(True, yaw2_rate))
    # print(time.time(),v1_x,v1_y,v2_x,v2_y)
    if v1_x*v1_x + v1_y*v1_y < 0.01 and v2_x*v2_x + v2_y*v2_y < 0.01:
        break

points = [airsim.Vector3r(30, 0, -20),
          airsim.Vector3r(60, 5, -20),
          airsim.Vector3r(90, 0, -20),
          airsim.Vector3r(120, 10, -20)]
leader.move_on_path(points, velocity=3, drivetrain=airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False, 0))

# 跟随
while True:    
    leader_state = leader.get_state()
    follower1_state = follower1.get_state()
    follower2_state = follower2.get_state()

    z = leader_state["position"][2]
    v1_x, v1_y, yaw1_rate = calculateVelocity(x_d, y_d, leader_state, follower1_state)
    v2_x, v2_y, yaw2_rate = calculateVelocity(x_d, -y_d, leader_state, follower2_state)

    follower1.move_by_velocity_z(v1_x, v1_y, z, duration = 0.2, yaw_mode=airsim.YawMode(True, yaw1_rate))
    follower2.move_by_velocity_z(v2_x, v2_y, z, duration = 0.2,  yaw_mode=airsim.YawMode(True, yaw2_rate))
    # print(time.time(),v1_x,v1_y,v2_x,v2_y)