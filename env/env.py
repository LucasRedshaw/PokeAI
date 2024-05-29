import gymnasium as gym  # Updated to gymnasium
from gymnasium import spaces  # Updated to gymnasium
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import numpy as np
from PIL import Image
import hashlib
from datetime import datetime
import time
import datetime
import csv
import extras.heatmap as heatmap
import os
import env.ram_map as ram_map

class GameBoyEnv(gym.Env):
    def __init__(self,window='null'):
        super(GameBoyEnv, self).__init__()
        game_rom = "PokemonRed.gb"
        self.pyboy = PyBoy(game_rom, window=window)
        self.pyboy.set_emulation_speed(0)
        
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low=0, high=255, shape=(72, 80, 3), dtype='uint8')
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_maps.add(40)
        self.max_steps = 16000
        self.current_step = 0
        self.rewardtotal = 0
        self.pokelvlsumtrack = 6
        #open('player_coordinates.csv', mode='w').close()

    def _get_obs(self):
        observation = {
            "screen": self.render(),
        }
        return observation

    def render(self):
        game_pixels_render = np.array(self.pyboy.screen.image)[:, :, :3][::2, ::2]
        return game_pixels_render # [::2, ::2, :]

    def step(self, action):

        self.take_action(action)
        self.current_step += 1
        self.pyboy.tick(60)

        reward =  0
        coordreward = 0
        mapidreward = 0
        levelupreward = 0
    
        mapid = self.pyboy.memory[0xD35E]

        poke1lvl = self.pyboy.memory[0xD18C]
        poke2lvl = self.pyboy.memory[0xD1B8]
        poke3lvl = self.pyboy.memory[0xD1E4]
        poke4lvl = self.pyboy.memory[0xD210]
        poke5lvl = self.pyboy.memory[0xD23C]
        poke6lvl = self.pyboy.memory[0xD268]

        pokelvlsum = poke1lvl + poke2lvl + poke3lvl + poke4lvl + poke5lvl + poke6lvl

        # Exploration
        r, c, map_n = ram_map.position(self.pyboy) # this is [y, x, z]
        self.seen_coords.add((r, c, map_n))
        coordreward = (0.02 * len(self.seen_coords))

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
            levelupreward = 8
            print("Caught or Levelled")
            self.pokelvlsumtrack = pokelvlsum

        reward = coordreward + mapidreward + levelupreward
        self.rewardtotal += reward 
        
        if self.current_step >= self.max_steps:
            print(str(self.rewardtotal))
            done = True
        else:
            done = False

        truncated = False
        info = {}

        #print(reward)
        # with open('player_coordinates.csv', mode='a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([self.current_step, mapid, xcoord, ycoord])

        return self.render(), reward, done, truncated, info

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)
        np.random.seed(seed)
        with open("state_file.state", "rb") as f:
            self.pyboy.load_state(f)

        info = {}
        self.seen_coords = set()
        self.seen_maps = set()
        self.seen_maps.add(40)
        self.current_step = 0
        self.rewardtotal = 0
        self.pokelvlsumtrack = 6

        image_path = "amap.png"
        csv_path = "player_coordinates.csv"
        map_ids = [0, 12]  

        # Read coordinates
        #coordinates = heatmap.read_coordinates(csv_path, map_ids)


        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


        #output_path = f"heatmaps\heatmap_{current_time}.png"

        # Create the heatmap
        #if not os.path.exists(output_path):
         #   heatmap.create_heatmap(image_path, coordinates, output_path, heatmap.base_coordinates)

        #open('player_coordinates.csv', mode='w').close()

        #print("Reset Environment")

        return self.render(), info

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

    


