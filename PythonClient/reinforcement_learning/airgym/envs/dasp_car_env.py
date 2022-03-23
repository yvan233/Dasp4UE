import airsim
import numpy as np
import time

import gym
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv

import socket
from DaspCarClient import DaspCarClient,get_image,get_lidar

class AirSimCarDaspEnv(AirSimEnv):
    def __init__(self, hostIP, localIP):
        # 初始化客户端实例,与服务器端建立连接
        self.localIP = localIP
        self.state = {}
        self.client = DaspCarClient(hostIP)
        # self.action_space = spaces.Discrete(11)
        self.action_space = spaces.Discrete(6)

    def _setup_car(self):
        self.client.reset()
        time.sleep(0.01)

    def __del__(self):
        self.client.reset()

    def _do_action(self, action):
        throttle = 1
        steering = 0
        brake = 0
        if action == 0:
            throttle = 0
            brake = 1
        elif action == 1:
            steering = 0
        elif action == 2:
            steering = 30
        elif action == 3:
            steering = -30
        elif action == 4:
            steering = 15
        else:
            steering = -15
        # elif action == 5:
        #     steering = -25
        # elif action == 6:
        #     throttle = -1
        #     steering = 0
        # elif action == 7:
        #     throttle = -1
        #     steering = 50
        # elif action == 8:
        #     throttle = -1
        #     steering = -50
        # elif action == 9:
        #     throttle = -1
        #     steering = 25
        # else:
        #     throttle = -1
        #     steering = -25
        action = {"throttle": throttle,"steering": steering,"brake": brake}
        self.client.do_action(action)

    def _get_obs(self):
        self.state["car"] = self.client.get_state()
        self.state["collision"] = self.client.get_collision()
        self.state["image"] = get_image(self.localIP)
        self.state["lidar"] = get_lidar(self.localIP)
        return self.state

    def _compute_reward(self):
        reward = 1

        done = 0
        # if brake == 0:
        #     if speed <= 1:
        #         done = 1
        if self.state["collision"]["has_collided"]:
            done = 1
        return reward, done

    def step(self, action):
        self._do_action(action)
        obs = self._get_obs()
        reward, done = self._compute_reward()

        return obs, reward, done, self.state["collision"]

    def reset(self):
        self._setup_car()
        self._do_action(0)
        return self._get_obs()

    def start_record(self):
        self.client.start_record()

    def stop_record(self):
        self.client.stop_record()