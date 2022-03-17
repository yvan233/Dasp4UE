import time
import socket
from DaspCarClient import DaspCarClient,get_image,get_lidar

if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    remote_ip = host
    
    # 初始化客户端实例,与服务器端建立连接
    client = DaspCarClient(host)

    # 获取车辆状态
    state = client.get_state()
    print(state)  

    # 开始记录数据
    print("start record")
    client.start_record()

    # 读取碰撞信息
    collision = client.get_collision()
    if collision["has_collided"]:
        print (f"collision with {collision['object_name']}")

    # 获取图像
    img = get_image(remote_ip)
    print(img)

    # 获取雷达
    lidar = get_lidar(remote_ip)
    print(lidar)

    # 前进
    action = {"throttle": 1,"steering": 30,"brake": 0}
    client.do_action(action)
    time.sleep(3)

    # 后退
    action = {"throttle": -1,"steering": 50,"brake": 0}
    client.do_action(action)
    time.sleep(3)

    # 刹车
    action = {"throttle": 0,"steering": 0,"brake": 1}
    client.do_action(action)
    time.sleep(3)

    # 重置
    client.reset()

    # 结束记录数据
    print("stop record")
    client.stop_record()