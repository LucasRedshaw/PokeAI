import gymnasium as gym  # Updated to gymnasium
from gymnasium import spaces  # Updated to gymnasium
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import numpy as np
from PIL import Image
import hashlib
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from datetime import datetime
import time
import datetime
import csv
import helpers.heatmap as heatmap
import os
import configparser

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
        self.take_action(action)
        self.current_step += 1
        self.pyboy.tick(24)
        observation = np.array(self.pyboy.screen.ndarray)[:, :, :3][::2, ::2]
        reward =  0
        coordreward = 0
        mapidreward = 0
        levelupreward = 0

        mapid = self.pyboy.memory[0xD35E]
        xcoord = self.pyboy.memory[0xD362]
        ycoord = self.pyboy.memory[0xD361]

        poke1lvl = self.pyboy.memory[0xD18C]      
        poke2lvl = self.pyboy.memory[0xD1B8]
        poke3lvl = self.pyboy.memory[0xD1E4]
        poke4lvl = self.pyboy.memory[0xD210]
        poke5lvl = self.pyboy.memory[0xD23C]
        poke6lvl = self.pyboy.memory[0xD268]

        poke1maxhp1 = self.pyboy.memory[0xD18D]
        poke1maxhp2 = self.pyboy.memory[0xD18E]
        poke1currenthp1 = self.pyboy.memory[0xD16C]
        poke1currenthp2 = self.pyboy.memory[0xD16D]
        poke1maxhp = poke1maxhp1 + poke1maxhp2
        poke1currenthp = poke1currenthp1 + poke1currenthp2

        poke2maxhp1 = self.pyboy.memory[0xD1B9]
        poke2maxhp2 = self.pyboy.memory[0xD1BA]
        poke2currenthp1 = self.pyboy.memory[0xD198]
        poke2currenthp2 = self.pyboy.memory[0xD199]
        poke2maxhp = poke2maxhp1 + poke2maxhp2
        poke2currenthp = poke2currenthp1 + poke2currenthp2

        poke3maxhp1 = self.pyboy.memory[0xD1E5]
        poke3maxhp2 = self.pyboy.memory[0xD1E6]
        poke3currenthp1 = self.pyboy.memory[0xD1C4]
        poke3currenthp2 = self.pyboy.memory[0xD1C5]
        poke3maxhp = poke3maxhp1 + poke3maxhp2
        poke3currenthp = poke3currenthp1 + poke3currenthp2

        poke4maxhp1 = self.pyboy.memory[0xD211]
        poke4maxhp2 = self.pyboy.memory[0xD212]
        poke4currenthp1 = self.pyboy.memory[0xD1F0]
        poke4currenthp2 = self.pyboy.memory[0xD1F1]
        poke4maxhp = poke4maxhp1 + poke4maxhp2
        poke4currenthp = poke4currenthp1 + poke4currenthp2

        poke5maxhp1 = self.pyboy.memory[0xD23D]
        poke5maxhp2 = self.pyboy.memory[0xD23E]
        poke5currenthp1 = self.pyboy.memory[0xD21C]
        poke5currenthp2 = self.pyboy.memory[0xD21D]
        poke5maxhp = poke5maxhp1 + poke5maxhp2
        poke5currenthp = poke5currenthp1 + poke5currenthp2

        poke6maxhp1 = self.pyboy.memory[0xD269]
        poke6maxhp2 = self.pyboy.memory[0xD26A]
        poke6currenthp1 = self.pyboy.memory[0xD248]
        poke6currenthp2 = self.pyboy.memory[0xD249]
        poke6maxhp = poke6maxhp1 + poke6maxhp2
        poke6currenthp = poke6currenthp1 + poke6currenthp2

        summaxhp = poke1maxhp + poke2maxhp + poke3maxhp + poke4maxhp + poke5maxhp + poke6maxhp
        sumcurrenthp = poke1currenthp + poke2currenthp + poke3currenthp + poke4currenthp + poke5currenthp + poke6currenthp

        hptracker = sumcurrenthp / summaxhp

        #print(hptracker)

        if hptracker == 0:
            if self.wait1 == 0:
                print("Fainted")
                self.wait1 = 1
        else:
            self.wait1 = 0


        pokelvlsum = poke1lvl + poke2lvl + poke3lvl + poke4lvl + poke5lvl + poke6lvl

        current_coords = (mapid, xcoord, ycoord)

        if current_coords not in self.seen_coords:
            coordreward = 1
            if mapid == 1:
                #print("Viridian City")
                coordreward += 0.2
            if mapid == 12:
                #print("Route 1")
                coordreward += 0.1
            if mapid == 51:
                #print("Viridian Forest")
                coordreward += 0.3
            if mapid == 50:
                #print("Viridian Forest")
                coordreward += 0.3
            if mapid == 47:
                #print("Viridian Forest")
                coordreward += 0.3
            if mapid == 13:
                #print("Route 2")
                coordreward += 0.3
            if mapid == 2:
                #print("Pewter City")
                coordreward += 0.4
            self.seen_coords.add(current_coords)  # Mark this state as seen
            #coordreward = (0.02 * len(self.seen_coords))

        if mapid not in self.seen_maps:
            mapidreward = 0
            if mapid == 1:
                print("Viridian City")
            if mapid == 12:
                print("Route 1")
            if mapid == 51:
                print("Viridian Forest")
            if mapid == 13:
                print("Route 2")
            if mapid == 2:
                print("Pewter City")

            self.seen_maps.add(mapid)

        if pokelvlsum > self.pokelvlsumtrack:
            levelupreward = 50*(pokelvlsum - self.pokelvlsumtrack)
            #levelupreward = 8
            #print("Caught or Levelled")
            self.pokelvlsumtrack = pokelvlsum

        # levelupreward = (0.2 *(pokelvlsum - 6))
        reward = coordreward + mapidreward + levelupreward
        self.explorationrewardtotal += coordreward
        self.levelrewardtotal += levelupreward
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

    


