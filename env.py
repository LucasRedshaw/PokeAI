import gymnasium as gym  
from gymnasium import spaces  
from pyboy import PyBoy
import numpy as np
import configparser
from helpers import calc_reward
from helpers import memory_helper
import numpy as np
import csv
import os

config = configparser.ConfigParser()
config.read('config.conf')

ep_length = int(config['PPO']['ep_length'])
rewardthreshold = int(config['ENV']['rewardthreshold'])
actions = int(config['ENV']['actions'])
ticksperstep = int(config['ENV']['ticksperstep'])
buttonholdlength = int(config['ENV']['buttonholdlength'])


class GameBoyEnv(gym.Env):
    def __init__(self, game_rom, window='null'):
        super(GameBoyEnv, self).__init__()
        self.pyboy = PyBoy(game_rom, window=window)
        self.action_space = spaces.Discrete(actions)
        self.observation_space = spaces.Box(low=0, high=255, shape=(72, 80, 3), dtype=np.uint8)
        self.resetvars()
        self.explorationrewardtotal = 0
        self.levelrewardtotal = 0
        self.resetssurvived = 0
        self.truetotal = 0

    def step(self, action):
        self.current_step += 1
        self.take_action(action)
        self.pyboy.tick(ticksperstep)
        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        reward, exploration_reward, level_reward = calc_reward.calc_reward(self)
        self.explorationrewardtotal += exploration_reward
        self.levelrewardtotal += level_reward
        self.rewardtotal += reward 
        self.truetotal += reward
        if self.current_step >= self.max_steps:
            if self.rewardtotal < rewardthreshold:
                done = True
            else:
                self.rewardtotal = 0
                self.current_step = 0
                self.resetssurvived += 1
                done = False
        else:
            done = False
        truncated = False
        info = {}
        return observation, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        state_file_path = os.path.join('states', 'state_file.state')
        with open(state_file_path, "rb") as f:
            self.pyboy.load_state(f)
        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        info = {}
        self.resetvars()

        print("-----------------\nAgent reset with total reward: " + str(self.truetotal) + "\nResets survived: " + str(self.resetssurvived) + "\nTotal steps: " + str(self.resetssurvived*ep_length) + "\nLevel reward:  " + str(self.levelrewardtotal) + "\nExploration reward:  " + str(self.explorationrewardtotal)+"\n-----------------")
        
        return observation, info

    def take_action(self, action):
        if action == 0:
            self.pyboy.button('a',buttonholdlength)
        elif action == 1:
            self.pyboy.button('b',buttonholdlength)
        elif action == 2:
            self.pyboy.button('up',buttonholdlength)
        elif action == 3:
            self.pyboy.button('down',buttonholdlength)
        elif action == 4:
            self.pyboy.button('left',buttonholdlength)
        elif action == 5:
            self.pyboy.button('right',buttonholdlength)
        elif action == 6:
            self.pyboy.button('start',buttonholdlength)
        elif action == 7:
            self.pyboy.button('select',buttonholdlength)

    def close(self):
        self.pyboy.stop()

    def resetvars(self):
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_checkpoints = set()
        self.seen_checkpoints.add(0)
        self.seen_maps.add(40)
        self.max_steps = ep_length
        self.current_step = 0
        self.rewardtotal = 0
        self.explorationrewardtotal = 0
        self.levelrewardtotal = 0
        self.pokelvlsumtrack = 6
        self.truetotal = 0
        self.resetssurvived = 0
        self.hpold = 0
        self.badges = 0
        self.mapid = 0
        self.opplvlold = 0
        self.previousreward = 0
        self.wait1 = 0
        return