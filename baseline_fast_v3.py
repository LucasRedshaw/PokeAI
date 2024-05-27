from os.path import exists
from pathlib import Path
import uuid

from stable_baselines3 import PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList


from red_gym_env_v3_minimal import PokeRedEnv
from stream import StreamWrapper

def make_env(rank, seed=0):
    """
    Utility function for multiprocessed env.
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the initial seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = StreamWrapper(
            PokeRedEnv('../PokemonRed.gb', '../has_pokedex_nballs.state'), 
            stream_metadata = { # All of this is part is optional
                "user": "pw-min", # choose your own username
                "env_id": rank, # environment identifier
                "color": "#662299", # choose your color :)
                "extra": "", # any extra text you put here will be displayed
            }
        )
        env.reset(seed=(seed + rank))
        return env
    set_random_seed(seed)
    return _init

if __name__ == "__main__":

    use_wandb_logging = True
    ep_length = 2048 * 10
    sess_id = str(uuid.uuid4())[:8]
    sess_path = Path(f'session_{sess_id}')

        
    num_cpu = 24  # Also sets the number of episodes per training iteration
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
    
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path=sess_path,
                                     name_prefix="poke")
    
    callbacks = [checkpoint_callback]

    #env_checker.check_env(env)

    # put a checkpoint here you want to start from
    file_name = "" #"session_9ff8e5f0/poke_21626880_steps"

    train_steps_batch = ep_length // 10
    
    if exists(file_name + ".zip"):
        print("\nloading checkpoint")
        model = PPO.load(file_name, env=env)
        model.n_steps = train_steps_batch
        model.n_envs = num_cpu
        model.rollout_buffer.buffer_size = train_steps_batch
        model.rollout_buffer.n_envs = num_cpu
        model.rollout_buffer.reset()
    else:
        model = PPO("MultiInputPolicy", env, verbose=1, n_steps=train_steps_batch, batch_size=128, n_epochs=1, gamma=0.998, tensorboard_log=sess_path)
    
    print(model.policy)

    model.learn(total_timesteps=(ep_length)*num_cpu*10000, callback=CallbackList(callbacks), tb_log_name="poke_ppo")


