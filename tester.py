from env import GameBoyEnv

env = GameBoyEnv('PokemonRed.gb', window='null')
env.reset()
for _ in range(100):
    observation, reward, done, truncated, info = env.step(env.action_space.sample())
    if done:
        env.reset()
print("Environment works fine.")
