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
import dill

# Define a custom Gym environment for the Game Boy using PyBoy
class GameBoyEnv(gym.Env):
    # Initialization method
    def __init__(self, game_rom, window='null'):
        super(GameBoyEnv, self).__init__()  # Initialize the superclass
        # Initialize PyBoy with a ROM file and set the window type
        self.pyboy = PyBoy(game_rom, window=window)
        self.pyboy.set_emulation_speed(0)
        # Define the action space - Game Boy has 8 buttons
        self.action_space = spaces.Discrete(6)
        # Define the observation space - Game Boy screen size 160x144, RGB
        self.observation_space = spaces.Box(low=0, high=255, shape=(144, 160, 3), dtype='uint8')
        self.seen_coords = set()
        self.seen_maps = set()
        self.max_steps = 8192
        self.current_step = 0

    def step(self, action):
        self.take_action(action)
        self.current_step += 1
        print(self.current_step)
        self.pyboy.tick(60)

        observation = np.array(self.pyboy.screen.image)[:, :, :3]

        reward =  0  # Default reward for non-unique state

        # Retrieve current position and map data
        mapid = self.pyboy.memory[0xD35E]
        xcoord = self.pyboy.memory[0xD362]
        ycoord = self.pyboy.memory[0xD361]

        # Unique key based on map, x, and y coordinates
        current_coords = (mapid, xcoord, ycoord)

        # Check if the state has been seen before and update the reward if it's new
        if current_coords not in self.seen_coords:
            reward = 1  # Reward for discovering a new state
            self.seen_coords.add(current_coords)  # Mark this state as seen

        if mapid not in self.seen_maps:
            reward = 10
            if mapid == 1:
                print("Viridian City")
                reward = 50
            if mapid == 12:
                print("Route 1")
                reward = 25

        #print(f"Map ID: {mapid}, X Coord: {xcoord}, Y Coord: {ycoord}")
        #print(reward)
        if self.current_step >= self.max_steps:
            done = True
        else:
            done = False
        truncated = False
        info = {}
        #print(reward)

        return observation, reward, done, truncated, info
    
    
    # Reset function to start a new episode
    def reset(self, seed=None, options=None):
        # Seed the random number generator for reproducibility
        super().reset(seed=seed)
        np.random.seed(seed)
        with open("state_file.state", "rb") as f:
            self.pyboy.load_state(f)

        # Get the current screen image as an RGB numpy array

        observation = np.array(self.pyboy.screen.image)
        observation = observation[:, :, :3]
        info = {}
        self.seen_coords = set()
        self.seen_maps = set()
        self.current_step = 0
        print("Reset Environment")
        return observation, info

    def take_action(self, action):
    # Map action to PyBoy controls
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

    # Close function to clean up resources
    def close(self):
        # Stop the emulator and free resources
        final_image = self.pyboy.screen.image
        final_image.save("final_observation.png")
        # Stop the emulator and free resources
        self.pyboy.stop()

    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     # Remove the PyBoy instance from the state
    #     del state['pyboy']
    #     return state

    # def __setstate__(self, state):
    #     self.__dict__.update(state)
    #     # Re-initialize the PyBoy instance
    #     self.pyboy = PyBoy('PokemonRed.gb', window='SDL2')
    #     self.pyboy.set_emulation_speed(0)


