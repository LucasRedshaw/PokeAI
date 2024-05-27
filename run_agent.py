from env import GameBoyEnv
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.utils import set_random_seed

def make_env(rank, seed=0):
    def _init():
        env = GameBoyEnv('PokemonRed.gb', window='SDL2')
        env.reset(seed=(seed + rank))
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env = make_env(0)() 
    file_name = 'evening25-05-24.zip'
    print('\nloading checkpoint')
    model = PPO.load(file_name, env=env)
    obs, info = env.reset()
    while True:
        action, _states = model.predict(obs, deterministic=False)
        obs, rewards, terminated, truncated, info = env.step(action)
