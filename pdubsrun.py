from os.path import exists
from pathlib import Path
import uuid
from env import GameBoyEnv
from stable_baselines3 import PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList
from helpers.stream import StreamWrapper

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

    use_wandb_logging = False
    ep_length = 2048 * 10
    sess_id = str(uuid.uuid4())[:8]
    sess_path = Path(f'session_{sess_id}')
    
    num_cpu = 8 # Also sets the number of episodes per training iteration
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
    
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path=sess_path,
                                     name_prefix='poke')
    
    callbacks = [checkpoint_callback]


    file_name = '' 
    
    if exists(file_name + '.zip'):
        print('\nloading checkpoint')
        model = PPO.load(file_name, env=env)
        model.n_steps = ep_length
        model.n_envs = num_cpu
        model.rollout_buffer.buffer_size = ep_length
        model.rollout_buffer.n_envs = num_cpu
        model.rollout_buffer.reset()
    else:
        model = PPO('CnnPolicy', env, verbose=1, n_steps=ep_length // 8, batch_size=128, n_epochs=3, gamma=0.998, tensorboard_log=sess_path)

    # run for up to 5k episodes
    model.learn(total_timesteps=(ep_length)*num_cpu*5000, callback=CallbackList(callbacks))
