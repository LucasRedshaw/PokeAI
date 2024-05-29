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
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback, CallbackList
from datetime import datetime
from helpers.stream import StreamWrapper
from tensorboardX import SummaryWriter
import configparser
from stable_baselines3.common.logger import configure
import numpy as np


## tensorboard --logdir=tensorboard_logs
## https://pwhiddy.github.io/pokerl-map-viz/

log_dir = "tensorboard_logs"
writer = SummaryWriter(log_dir)

class TensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.writer = SummaryWriter(log_dir)

    def _on_step(self) -> bool:
        value = np.random.random()
        self.writer.add_scalar("random_value", value, self.num_timesteps)
        return True
    
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

    log_dir = "tensorboard_logs"
    logger = configure(log_dir, ["tensorboard"])

    if load_checkpoint and exists(checkpoint_path):
        print("model loaded")
        model = PPO.load(checkpoint_path, env=env, verbose=1, n_steps=ep_length, batch_size=128, n_epochs=3, gamma=0.998, tensorboard_log=log_dir)
    else:
        print("new model")
        model = PPO('CnnPolicy', env, verbose=1, n_steps=ep_length, gamma=0.998, tensorboard_log=log_dir)
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path='checkpoints', name_prefix='poke')
    callback = CallbackList([checkpoint_callback, TensorboardCallback()])
    model.learn(total_timesteps=total_length, callback=callback)
    model.save("ppo_pokemon_fin")