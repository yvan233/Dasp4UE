import airsim
import numpy as np
import sys
sys.path.insert(1,".")
from Agent.AirSimUavAgent import AirSimUavAgent
import math

UE_ip = "127.0.0.1"
origin_geopoint = (116.16872381923261, 40.05405620434274,150)

leader = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav0", origin_pos=[0, 0, -2])
follower = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav1", origin_pos=[0, 5, -2])
# 初始化，建立连接
leader.take_off()      # 起飞
leader.move_to_position(0,0,-5,2)

follower.take_off()      # 起飞
follower.move_to_position(0,5,-5,2,waited=True)

fd = 2*1.172
sd = 2
velocity = 3
X_d = np.array([[-fd],[sd]])
while True:
    leader_state = leader.get_state()
    follower_state = follower.get_state()

    z = leader_state["position"][2]
    # 旋转矩阵
    yaw = leader_state["orientation"][2]
    R_b_e = np.array([[math.cos(yaw), -math.sin(yaw)],[math.sin(yaw), math.cos(yaw)]])
    R_e_b = np.array([[math.cos(yaw), math.sin(yaw)],[-math.sin(yaw), math.cos(yaw)]])

    X1 = np.array([[leader_state["position"][0]], [leader_state["position"][1]]])
    X2 = np.array([[follower_state["position"][0]], [follower_state["position"][1]]])
    
    X_b = R_e_b@(X2 - X1)
    omega = X_d - X_b
    V2 = R_b_e@omega

    if np.linalg.norm(V2) < 0.1:
        follower.hover()
    elif np.linalg.norm(V2) > velocity:
        V2 = V2/np.linalg.norm(V2)*velocity
        follower.move_by_velocity_z(V2[0][0], V2[1][0], z, duration= 1/velocity)
    else:
        follower.move_by_velocity_z(V2[0][0], V2[1][0], z, duration= 1/velocity)