# 小蜜蜂楼外进入楼内脚本demo
"""
{
	"SettingsVersion": 1.2,
	"ViewMode":"SpringArmChase",
	"ClockType": "ScalableClock",
	"ClockSpeed": 1,
	"OriginGeopoint": {
	  "Latitude": 40.05405620434274,
	  "Longitude": 116.16872381923261, 
	  "Altitude": 150
	},
	"PawnPaths": {
		"Bee":{"PawnBP":"Class'/Game/newFly/BP_FlyingPawn.BP_FlyingPawn_C'"}
		},
	"Vehicles": {
	  "Uav0": {
		"VehicleType": "SimpleFlight",
		"PawnPath": "Bee",
		"X": -16, "Y": -76, "Z": -2,
		"Yaw": 90
	  }
	}
}
"""
import sys
sys.path.insert(1,".")  # 把上一级目录加入搜索路径
from Agent.AirSimUavAgent import AirSimUavAgent
import time
UE_ip = "127.0.0.1"
origin_pos = [-16, -76, -2]

origin_geopoint = (116.16872381923261, 40.05405620434274,150)
# 进入楼内
gps_path = [(116.16794445523611,40.05388613206607,154.67825317382812),
(116.16794409043491,40.05388555746181,162.2622528076172),
(116.16794409043491,40.05388555746181,172.6),
(116.16794503279978,40.05389133664743,172.6),
(116.16799008746888,40.05388969166288,172.6),
(116.16800331501977,40.05384891056716,172.6)]

# 潜入安全屋
gps_path2 = [(116.16800474190822,40.05380922531766,172.6),
(116.16807267053656,40.053799866639956,172.6),
(116.16813578561599,40.053845880431076,172.6),
(116.16820251144168,40.053838581486474,172.6),
(116.16822353306844,40.053838062087266,172.6)]

# 击杀vip
gps_path3 = [(116.16823340147532,40.05383504837999,172.6),
(116.16823419719795,40.05382717734135,172.6),
(116.168233048514,40.053821974088486,172.6),
(116.16823339979337,40.05381496127576,172.6)]

uav = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav0", origin_pos=origin_pos)

print(uav.get_state())
print(uav.get_collision())
print(uav.get_gps())

uav.take_off(waited = True)

# 转向
# uav.uav.rotateToYawAsync(90,margin=30).join()

uav.move_on_gps_path(gps_path, velocity=2.5, waited=True)
time.sleep(1.5)

uav.move_on_gps_path(gps_path2, velocity=1, waited=True)
time.sleep(3)

uav.move_on_gps_path(gps_path3, velocity=1, waited=True)
time.sleep(3)
# uav.move_on_gps_path(gps_path2, velocity=0.6, waited=True)
# time.sleep(5)
uav.land(waited = True)