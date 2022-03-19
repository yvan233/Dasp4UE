# 手柄控制demo
import time
import socket
import sys
sys.path.append(".")
from DaspCarClient import DaspCarClient,get_image,get_lidar
from xbox.Xboxcmd import *

if __name__ == '__main__':

    pygame.init()
    pygame.joystick.init()

    #查看现在有几个遥控器
    joycount = pygame.joystick.get_count()
    print("joycount:"+str(joycount))

    #连接第一个控制器
    joystick = pygame.joystick.Joystick(0)

    host = socket.gethostbyname(socket.gethostname())
    remote_ip = host
    
    # 初始化客户端实例,与服务器端建立连接
    client = DaspCarClient(host)

    # 重置
    print("reset")
    client.reset()

    # 获取车辆状态
    state = client.get_state()
    print("车辆状态",state)  

    # # 开始记录数据
    # print("start record")
    # client.start_record()

    # # 读取碰撞信息
    # collision = client.get_collision()
    # if collision["has_collided"]:
    #     print (f"collision with {collision['object_name']}")
    
    t = 0
    while True:
        #手柄控制
        pygame.event.get()
        steering = get_axis(joystick=joystick)[0]*50
        brake = get_button(joystick=joystick)[1]
        throttle1 = get_button(joystick=joystick)[3]
        throttle2 = get_button(joystick=joystick)[0]
        if throttle1 and not throttle2:
            throttle = 1
        elif not throttle1 and throttle2:
            throttle = -1
        else:
            throttle = 0
        # 前进
        action = {"throttle": throttle,"steering": steering,"brake": brake}
        client.do_action(action)
        time.sleep(0.01)
        if t % 100 == 0:
            print("控制策略",action)
        t += 1


    # # 结束记录数据
    # print("stop record")
    # client.stop_record()