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
from stream import StreamWrapper

# Define a function to create a new instance of the environment
def make_env():
    return GameBoyEnv('PokemonRed.gb', window='null')

def make_env(rank=1, seed=0):
    """
    Utility function for multiprocessed env.
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the initial seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = StreamWrapper(
            GameBoyEnv('PokemonRed.gb', window='null'), 
            stream_metadata = { # All of this is part is optional
                "user": "pw-min", # choose your own username
                "env_id": rank, # environment identifier
                "color": "#662299", # choose your color :)
                "extra": "", # any extra text you put here will be displayed
            }
        )
        env.reset(seed=(seed ))
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env = SubprocVecEnv([make_env for _ in range(1)])
    #model = PPO.load("test\poke_851968_steps.zip", env=env, verbose=1, n_steps=2048)
    model = PPO('CnnPolicy', env, verbose=1, n_steps=4096)

    checkpoint_callback = CheckpointCallback(save_freq=4096, save_path='test', name_prefix='poke')

    model.learn(total_timesteps=4096*500, callback=checkpoint_callback)

    model.save("ppo_pokemon_fin")
