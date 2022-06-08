# 特朗普位置：116.16822825174731, 40.05380267711057, 173.1387481689453
import sys
sys.path.insert(1,".")  # 把上一级目录加入搜索路径
from Agent.AirSimUavAgent import AirSimUavAgent

UE_ip = "127.0.0.1"
origin_pos = [-28, -44, -22]

origin_geopoint = (116.16872381923261, 40.05405620434274,150)
gps_path = [(116.1682074385,40.053804674937545,173.44400024414062),
(116.16820743849425,40.0538245309666,173.41134643554688),
(116.16821494905547,40.05384244215999,173.2959747314453),
(116.16823113570892,40.05383722171486,173.2694549560547),
(116.16824141867102,40.05383420717587,173.2307586669922),
(116.16823988163415,40.053821772882756,173.122314453125),
(116.16823703070543,40.05381751695653,173.1644287109375),
(116.16822806053638,40.05380206443721,172.6946563720703)]

uav = AirSimUavAgent(origin_geopoint, ip = UE_ip, vehicle_name= "Uav0", origin_pos=origin_pos)


print(uav.get_state())
print(uav.get_collision())
print(uav.get_gps())




uav.take_off(waited = True)
uav.uav.rotateToYawAsync(90,margin=30).join()

uav.move_on_gps_path(gps_path, velocity=1, waited=True)

uav.land(waited = True)