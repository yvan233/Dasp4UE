# gym demo
import airgym
import airsim
import gym
import time
import socket

if __name__ == '__main__':
    hostIP = socket.gethostbyname(socket.gethostname())
    localIP = hostIP
    env = gym.make("airsim-car-dasp-v0", hostIP=hostIP, localIP=localIP)    
    for i_episode in range(20):
        observation = env.reset()
        env.start_record()
        for t in range(100):
            action = env.action_space.sample()
            print(action, observation["car"]["position"])
            observation, reward, done, info = env.step(action)
            if done:
                print(f"Episode finished after {t+1} round: Collision with {info['object_name']}")
                env.stop_record()
                break
            time.sleep(1)
        env.stop_record()