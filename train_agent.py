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
    return GameBoyEnv('PokemonRed.gb', window='null')


env = DummyVecEnv([make_env for _ in range(4)])

model = PPO.load("ppo_pokemon39_last_good", env=env, verbose=1, n_steps=2048)
#model = PPO('CnnPolicy', env, verbose=1, n_steps=2048)

learn_steps = 40

for i in range(learn_steps):
     print(f"Starting iteration {i + 1}/{learn_steps}")
     current_time = datetime.now()
     print("Starting " + str(i) +":", current_time.strftime("%H:%M:%S"))


    # Learn for the specified number of timesteps
     model.learn(total_timesteps=2048)
     print("Finished " + str(i) +":", current_time.strftime("%H:%M:%S"))
     model.save("ppo_pokemon" + str(i))

model.save("ppo_pokemon")