import dill
from env import GameBoyEnv

def make_env():
    return GameBoyEnv('PokemonRed.gb', window='SDL2')

# Test pickleability
env = make_env()
try:
    pickled_env = dill.dumps(env)
    unpickled_env = dill.loads(pickled_env)
    print("Environment is pickleable")
except Exception as e:
    print(f"Environment is not pickleable: {e}")
