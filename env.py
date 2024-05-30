import gymnasium as gym  # Updated to gymnasium
from gymnasium import spaces  # Updated to gymnasium
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import numpy as np
from PIL import Image
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from datetime import datetime
import helpers.heatmap as heatmap
import configparser
from helpers import calc_reward
from helpers import memory_helper

config = configparser.ConfigParser()
config.read('config.conf')
ep_length = int(config['PPO']['ep_length'])

class GameBoyEnv(gym.Env):
    def __init__(self, game_rom, window='null'):

        super(GameBoyEnv, self).__init__()
        self.pyboy = PyBoy(game_rom, window=window)
        self.pyboy.set_emulation_speed(0)
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=255, shape=(72, 80, 3), dtype='uint8')
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_maps.add(40)
        self.max_steps = ep_length
        self.current_step = 0
        self.rewardtotal = 0
        self.explorationrewardtotal = 0
        self.levelrewardtotal = 0
        self.pokelvlsumtrack = 6
        self.wait1 = 0

        #open('player_coordinates.csv', mode='w').close()

    def step(self, action):

        self.current_step += 1

        self.take_action(action)

        self.pyboy.tick(24)

        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]

        hptracker = memory_helper.get_hp(self)

        if hptracker == 0:
            if self.wait1 == 0:
                print("Fainted")
                self.wait1 = 1
        else:
            self.wait1 = 0

        reward, exploration_reward, level_reward = calc_reward.calc_reward(self)

        self.explorationrewardtotal += exploration_reward
        self.levelrewardtotal += level_reward
        self.rewardtotal += reward 

        if self.current_step >= self.max_steps:
            print("Reward of " + str(self.rewardtotal) + " | Exploration: "+ str(self.explorationrewardtotal) + " | Levels: "+ str(self.levelrewardtotal) + " (" + str(self.pokelvlsumtrack) + ")")
            done = True
        else:
            done = False

        truncated = False
        info = {"total_reward": self.rewardtotal} if done else {}
        return observation, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        np.random.seed(seed)
        with open("states\\state_file.state", "rb") as f:
            self.pyboy.load_state(f)
        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        info = {}
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_maps.add(40)
        self.current_step = 0
        self.rewardtotal = 0
        self.explorationrewardtotal = 0
        self.levelrewardtotal = 0
        self.pokelvlsumtrack = 6

        return observation, info

    def take_action(self, action):
        if action == 0:
            self.pyboy.button('a',3)
        elif action == 1:
            self.pyboy.button('b',3)
        elif action == 2:
            self.pyboy.button('up',3)
        elif action == 3:
            self.pyboy.button('down',3)
        elif action == 4:
            self.pyboy.button('left',3)
        elif action == 5:
            self.pyboy.button('right',3)
        elif action == 6:
            self.pyboy.button('start',3)
        elif action == 7:
            self.pyboy.button('select',3)

    def close(self):
        self.pyboy.stop()

    


