from os.path import exists
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from env import GameBoyEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback, CallbackList
from helpers.stream import StreamWrapper
from tensorboardX import SummaryWriter
import configparser
from stable_baselines3.common.logger import configure


## tensorboard --logdir=tensorboard_logs
## https://pwhiddy.github.io/pokerl-map-viz/

log_dir = "tensorboard_logs"  
writer = SummaryWriter(log_dir)
    
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
                "user": "Lucas\n", # choose your own username
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

    if load_checkpoint == True:
        print("model loaded")
        model = PPO.load(checkpoint_path, env=env, verbose=0, n_steps=ep_length // 8, batch_size=128, n_epochs=3, gamma=0.998, tensorboard_log=log_dir, ent_coef=0.01)
    else:
        print("new model")
        model = PPO('CnnPolicy', env, verbose=0, n_steps=ep_length // 8, batch_size=128, n_epochs=3, gamma=0.998, tensorboard_log=log_dir, ent_coef=0.01)
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path='checkpoints', name_prefix='poke')
    callback = CallbackList([checkpoint_callback])
    model.learn(total_timesteps=total_length, callback=callback)
    model.save("ppo_pokemon_fin")