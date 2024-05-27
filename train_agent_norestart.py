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

def make_env(rank, seed=0):
    def _init():
        env = GameBoyEnv('PokemonRed.gb', window='null')
        env.reset(seed=(seed + rank))
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env_fns = [make_env(i) for i in range(8)]
    env = DummyVecEnv(env_fns)
    model = PPO.load("test\poke_1024000_steps.zip", env=env, verbose=1, n_steps=16000)
    #model = PPO('CnnPolicy', env, verbose=1, n_steps=16000)

    checkpoint_callback = CheckpointCallback(save_freq=16000, save_path='test', name_prefix='poke')

    model.learn(total_timesteps=160000*50000, callback=checkpoint_callback)

    model.save("ppo_pokemon_fin")
