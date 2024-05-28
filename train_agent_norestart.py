from os.path import exists
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from pathlib import Path
import uuid
from env import GameBoyEnv
from stable_baselines3 import A2C, PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback
from datetime import datetime
from helpers.stream import StreamWrapper
import configparser

config = configparser.ConfigParser()
config.read('config.conf')
ep_length = int(config['PPO']['ep_length'])
total_length = int(config['PPO']['total_length'])
agents = int(config['PPO']['agents'])
load_checkpoint = config.getboolean('PPO', 'load_checkpoint')
checkpoint_path = config['PPO']['checkpoint_path']

def make_env(rank, seed=0):
    def _init():
        env = GameBoyEnv('rom\\PokemonRed.gb', window='null')
        env.reset(seed=(seed + rank))
        env = StreamWrapper(
            env, 
            stream_metadata = { # All of this is part is optional
                "user": "Lucas", # choose your own username
                "env_id": id, # environment identifier
                "color": "#f766ff", # choose your color :)
                "extra": "", # any extra text you put here will be displayed
            }
        )
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env_fns = [make_env(i) for i in range(agents)]
    env = SubprocVecEnv(env_fns)

    if load_checkpoint and exists(checkpoint_path):
        model = PPO.load(checkpoint_path, env=env, verbose=1, n_steps=ep_length)
    else:
        model = PPO('CnnPolicy', env, verbose=1, n_steps=ep_length, batch_size=128, n_epochs=3, gamma=0.998)
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path='checkpoints', name_prefix='poke')
    model.learn(total_timesteps=total_length, callback=checkpoint_callback)
    model.save("ppo_pokemon_fin")
