import airsim
import math
# 通过设置cv_car的后置摄像头姿态从而修改主视角，进入游戏需要按i键

"""
{
	"SettingsVersion": 1.2,
	"ClockType": "ScalableClock",
	"ViewMode": "Front",
	"Vehicles": {
		"test3_drone": {
			"VehicleType": "SimpleFlight",
			"X": 7, "Y": 7, "Z": -2
		},
		"cv_car": {
			"VehicleType": "PhysXCar",
			"X": 0, "Y": 7, "Z": -2
		}
	}
}
"""

def list2Pose(list):
    return airsim.Pose(airsim.Vector3r(list[0], list[1], list[2]), 
        airsim.to_quaternion(math.radians(list[3]), math.radians(list[4]), math.radians(list[5])))
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True,vehicle_name="cv_car")
client.armDisarm(True,vehicle_name="cv_car")

# x,y,z,pitch,roll,yaw
pose1 = [20,30,-50,-30,0,-120]
pose2 = [20,-60,-50,-40,0,135]

# airsim.wait_key('Press any key to switch pose 1')
camera_pose = list2Pose(pose1)
client.simSetCameraPose(4, camera_pose, vehicle_name="cv_car")