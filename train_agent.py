import os
from os.path import exists
import re
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
    return GameBoyEnv('PokemonRed.gb', window='null')

def get_latest_checkpoint():
    checkpoint_files = [f for f in os.listdir('test') if f.endswith('.zip')]
    if not checkpoint_files:
        return None
    latest_checkpoint = max(checkpoint_files, key=extract_prefixes)
    return os.path.join('test', latest_checkpoint)

def extract_prefixes(filename):
    match = re.findall(r'\d+', '_'.join(filename.split('_')[0:2]))
    return tuple(map(int, match))

if __name__ == '__main__':
    attempt = 11
    while True:
        try:
            reload = get_latest_checkpoint()
            if reload:
                print(f"loading: {reload}")
                env = SubprocVecEnv([make_env for _ in range(8)])
                checkpoint_callback = CheckpointCallback(save_freq=2048, save_path='test', name_prefix=str(attempt))
                model = PPO.load(reload, env=env, verbose=1)
                model.learn(total_timesteps=2048 * 5000, callback=checkpoint_callback)
                model.save("ppo_pokemon_fin")
                env.close()  # Ensure the environment is closed gracefully
                break
            else:
                print("No checkpoint found, starting new training session.")
                env = SubprocVecEnv([make_env for _ in range(8)])
                checkpoint_callback = CheckpointCallback(save_freq=2048, save_path='test', name_prefix=str(attempt))
                model = PPO('MlpPolicy', env, verbose=1)
                model.learn(total_timesteps=2048 * 5000, callback=checkpoint_callback)
                model.save("ppo_pokemon_fin")
                env.close()  # Ensure the environment is closed gracefully
                break

        except Exception as e:
            print("An error occurred during training - retrying")
            print(e)
            attempt += 1
