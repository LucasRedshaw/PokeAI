![Logo](https://i.imgur.com/Dx3gPsT.png)


# PokeAI

A Pokemon Red Gymnasium environment for reinforcement learning using Stable Baslines 3. The model interacts with the game by sending button presses, and observes the screen the same way a human player would.


## Progress

![Static Badge](https://img.shields.io/badge/Code%20Runs%20-%20Completed%20-%20Red?color=green)

![Static Badge](https://img.shields.io/badge/Viridian%20Forrest%20-%20Completed%20-%20Red?color=green)

![Static Badge](https://img.shields.io/badge/First%20Gym%20-%20Completed%20-%20Red?color=green)

![Static Badge](https://img.shields.io/badge/Mount%20Moon%20-%20Not%20Completed%20-%20Red?color=red)

![Static Badge](https://img.shields.io/badge/Rescue%20Bill%20-%20Not%20Completed%20-%20Red?color=red)

![Static Badge](https://img.shields.io/badge/Second%20Gym%20-%20Not%20Completed%20-%20Red?color=red)

## Run Locally

Clone the project

```bash
  git clone https://github.com/LucasRedshaw/PokeAI
```

Go to the project directory

```bash
  cd PokeAI
```

Install dependencies (You will also need to obtain and place a Pokemon Red ROM in the root folder named PokemonRed.gb)

```bash
  pip install -r requirements.txt
```

To train a new model, set the config file as below, and run "train_agent_norestart.py"

```bash
  load_checkpoint = False

```
To continue training an old model, set the config file as below, and run "train_agent_norestart.py"

```bash
  load_checkpoint = True
  checkpoint_path = [path_to_a_checkpoint]
```

To run a model, set the config file as below, and run "run_agent.py;"

```bash
  checkpoint_path = [path_to_a_checkpoint]
```


## Acknowledgements

 - [Original Pokemon RL Project by PWhiddy](https://github.com/PWhiddy/PokemonRedExperiments)
 - [Live Visualisation by PWhiddy](https://github.com/pwhiddy/pokerl-map-viz/)


