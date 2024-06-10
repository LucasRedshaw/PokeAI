from os.path import exists
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from env import GameBoyEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecFrameStack
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
username = config['STREAM']['username']
color = config['STREAM']['color']
verbose = int(config['PPO']['verbose'])
nstepdivisor = int(config['PPO']['nstepdivisor'])
batchsize = int(config['PPO']['batchsize'])
epochs = int(config['PPO']['epochs'])
gamma = float(config['PPO']['gamma'])
ent_coef = float(config['PPO']['ent_coef'])

def make_env(rank, seed=0):
    def _init():
        rom_file_path = os.path.join('rom', 'PokemonRed.gb')
        env = GameBoyEnv(rom_file_path, window='null')
        env.reset(seed=(seed + rank))
        env = StreamWrapper(
            env, 
            stream_metadata = { 
                "user": username + "\n", 
                "env_id": id, 
                "color": color, 
                "extra": "", 
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
        model = PPO.load(
            checkpoint_path, 
            env, 
            n_steps=ep_length // nstepdivisor, 
            batch_size=batchsize, 
            n_epochs=epochs, 
            gamma=gamma, 
            ent_coef=ent_coef
            )
    else:
        print("new model")
        model = PPO(
            policy='MultiInputPolicy',
            env=env,
            verbose=verbose,
            n_steps=ep_length // nstepdivisor,
            batch_size=batchsize,
            n_epochs=epochs,
            gamma=gamma,
            tensorboard_log=log_dir,
            ent_coef=ent_coef
        )
    
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path='checkpoints', name_prefix='poke')
    callback = CallbackList([checkpoint_callback])
    
    model.learn(total_timesteps=total_length, callback=callback)
    model.save("ppo_pokemon_fin")
