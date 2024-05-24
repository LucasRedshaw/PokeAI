from os.path import exists
from pathlib import Path
import uuid
from env import GameBoyEnv
from stable_baselines3 import A2C, PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback
from datetime import datetime

# Define a function to create a new instance of the environment
def make_env():
    return GameBoyEnv('PokemonRed.gb', window='headless')


env = DummyVecEnv([make_env for _ in range(1)])



#model = PPO.load("ppo_pokemon39_last_good", env=env, verbose=1, n_steps=2048)
#model = PPO('CnnPolicy', env, verbose=1, n_steps=2048)
model = PPO('CnnPolicy', env, verbose=1, n_steps=8192)



checkpoint_callback = CheckpointCallback(save_freq=8192, save_path='test', name_prefix='poke')

model.learn(total_timesteps=8192*5000, callback=checkpoint_callback)

model.save("ppo_pokemon_fin")
