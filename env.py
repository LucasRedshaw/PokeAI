import gymnasium as gym  
from gymnasium import spaces  
from pyboy import PyBoy
import numpy as np
import configparser
from helpers import calc_reward
from helpers import memory_helper
import csv
import os

config = configparser.ConfigParser()
config.read('config.conf')

ep_length = int(config['PPO']['ep_length'])
rewardthreshold = int(config['ENV']['rewardthreshold'])
actions = int(config['ENV']['actions'])
ticksperstep = int(config['ENV']['ticksperstep'])
buttonholdlength = int(config['ENV']['buttonholdlength'])
episodereductionmultiplier = int(config['ENV']['episodereductionmultiplier'])


class GameBoyEnv(gym.Env):
    def __init__(self, game_rom, window='null'):
        super(GameBoyEnv, self).__init__()
        self.pyboy = PyBoy(game_rom, window=window)
        self.action_space = spaces.Discrete(actions)
        #self.observation_space = spaces.Box(low=0, high=255, shape=(72, 80, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Dict({
            'image': gym.spaces.Box(low=0, high=255, shape=(72, 80, 3), dtype=np.uint8),
            'health': gym.spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
            'badges': gym.spaces.Box(low=0, high=8, shape=(1,), dtype=np.float32),
            'levels': gym.spaces.Box(low=0, high=600, shape=(1,), dtype=np.float32)
        })
        self.resetvars()
        self.resetinitvars()
        self.csv_file_path = 'run_stats.csv'
        self.initialize_csv()

    def step(self, action):

        self.current_step += 1
        self.totalstepsinrun += 1
        self.take_action(action)
        self.pyboy.tick(ticksperstep)
        
        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        observationhealth = np.array([self.healthtracker], dtype=np.float32) 
        observationbadges = np.array([self.badges], dtype=np.float32)
        observationlevels = np.array([self.pokelvlsum], dtype=np.float32)

        obs = {'image': observation, 'health': observationhealth, 'badges': observationbadges, 'levels': observationlevels}

        reward, exploration_reward, level_reward, heal_reward, faint_reward, battle_reward, badge_reward, checkpoint_reward = calc_reward.calc_reward(self)
        self.explorationrewardtotal += exploration_reward
        self.levelrewardtotal += level_reward
        self.rewardtotal += reward 
        self.truetotal += reward
        self.heal_reward_total += heal_reward
        self.faint_reward_total += faint_reward
        self.battle_reward_total += battle_reward
        self.badge_reward_total += badge_reward
        self.checkpoint_reward_total += checkpoint_reward
        if self.current_step >= self.max_steps:
            if self.rewardtotal < rewardthreshold:
                done = True
            else:
                self.rewardtotal -= rewardthreshold*3
                if self.rewardtotal < 0:
                    self.rewardtotal = 0
                self.current_step = 0
                self.resetssurvived += 1
                done = False
        else:
            done = False
        truncated = False
        info = {}
        return obs, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        state_file_path = os.path.join('states', 'state_file.state')
        with open(state_file_path, "rb") as f:
            self.pyboy.load_state(f)

        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        observationhealth = np.array([self.healthtracker], dtype=np.float32) 
        observationbadges = np.array([self.badges], dtype=np.float32)
        observationlevels = np.array([self.pokelvlsum], dtype=np.float32)

        obs = {'image': observation, 'health': observationhealth, 'badges': observationbadges, 'levels': observationlevels}

        info = {}
        # self.write_stats_to_csv()

        # print("-----------------\nAgent reset with total reward: " + str(self.truetotal) + "\nResets survived: " + str(self.resetssurvived) + "\nTotal steps: " + str((self.resetssurvived*ep_length)+ep_length) + "\nLevel reward:  " + str(self.levelrewardtotal) + "\nExploration reward:  " + str(self.explorationrewardtotal)+"\n-----------------")
        
        self.resetvars()
        return obs, info

    def take_action(self, action):
        if action == 0:
            self.pyboy.button('a', buttonholdlength)
        elif action == 1:
            self.pyboy.button('b', buttonholdlength)
        elif action == 2:
            self.pyboy.button('up', buttonholdlength)
        elif action == 3:
            self.pyboy.button('down', buttonholdlength)
        elif action == 4:
            self.pyboy.button('left', buttonholdlength)
        elif action == 5:
            self.pyboy.button('right', buttonholdlength)
        elif action == 6:
            self.pyboy.button('start', buttonholdlength)
        elif action == 7:
            self.pyboy.button('select', buttonholdlength)

    def close(self):
        self.pyboy.stop()

    def resetvars(self):
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_checkpoints = set()
        self.seen_checkpoints.add(0)
        self.seen_maps.add(40)
        self.healthtracker = 0
        self.max_steps = ep_length
        self.current_step = 0
        self.pokelvlsumtrack = 6
        self.pokelvlsum = 0
        self.hpold = 0
        self.badges = 0
        self.mapid = 0
        self.opplvlold = 0
        self.previousreward = 0
        self.wait1 = 0
        self.rewardtotal = 0
        return
    
    def resetinitvars(self):
        self.explorationrewardtotal = 0
        self.levelrewardtotal = 0
        self.resetssurvived = 0
        self.truetotal = 0
        self.totalstepsinrun = 0
        self.heal_reward_total = 0
        self.faint_reward_total = 0
        self.battle_reward_total = 0
        self.badge_reward_total = 0
        self.checkpoint_reward_total = 0
        return

    def initialize_csv(self):
        with open(self.csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Total Reward', 'Resets Survived', 'Total Steps', 'Level Reward', 'Exploration Reward', 'Total Run Steps', 'Total Badges', 'Init Step', 'Heal Reward', 'Faint Reward', 'Battle Reward', 'Badge Reward', 'Checkpoint Reward'])

    def write_stats_to_csv(self):
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.truetotal, self.resetssurvived, (self.resetssurvived*ep_length)+ep_length, self.levelrewardtotal, self.explorationrewardtotal, self.totalstepsinrun, self.badges, self.totalstepsinrun - ((self.resetssurvived*ep_length)+ep_length), self.heal_reward_total, self.faint_reward_total, self.battle_reward_total, self.badge_reward_total, self.checkpoint_reward_total])
