import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import configparser

config = configparser.ConfigParser()
config.read('config.conf')
file_path = str(config['GRAPH']['file_name'])
update_frequency = int(config['GRAPH']['update_frequency'])

# Function to read the CSV file and process the data
def read_data(file_path):
    df = pd.read_csv(file_path)
    # Drop rows with any missing or NaN values
    return df

# Function to update the graph
def update_graph(i):
    try:
        df = read_data(file_path)
        # Graph 1: % of agents with 1 badge per init step
        ax1.clear()
        init_steps = df['Init Step'].unique()
        percent_agents_with_badge = []
        for step in init_steps:
            total_agents = df[df['Init Step'] == step].shape[0]
            if total_agents > 0:
                agents_with_badge = df[(df['Init Step'] == step) & (df['Total Badges'] >= 1)].shape[0]
                percent_agents_with_badge.append((agents_with_badge / total_agents) * 100)
            else:
                percent_agents_with_badge.append(0)
        
        ax1.plot(init_steps, percent_agents_with_badge, marker='o', color='lightblue', linestyle='-', linewidth=2)
        ax1.set_title('% of Agents with 1 Badge per Init Step', color='white')
        ax1.set_xlabel('Init Step', color='white')
        ax1.set_ylabel('% of Agents with 1 Badge', color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        
        # Graph 2: Average reward against total run steps
        ax2.clear()
        avg_rewards = df.groupby('Total Run Steps')['Total Reward'].mean()
        avg_level_rewards = df.groupby('Total Run Steps')['Level Reward'].mean()
        avg_exploration_rewards = df.groupby('Total Run Steps')['Exploration Reward'].mean()
        avg_heal_rewards = df.groupby('Total Run Steps')['Heal Reward'].mean()
        avg_faint_rewards = df.groupby('Total Run Steps')['Faint Reward'].mean()
        avg_battle_rewards = df.groupby('Total Run Steps')['Battle Reward'].mean()
        avg_badge_rewards = df.groupby('Total Run Steps')['Badge Reward'].mean()
        avg_checkpoint_rewards = df.groupby('Total Run Steps')['Checkpoint Reward'].mean()
        
        ax2.plot(avg_rewards.index, avg_rewards.values, marker='o', color='lightcoral', linestyle='-', linewidth=2, label='Average Total Reward')
        ax2.plot(avg_level_rewards.index, avg_level_rewards.values, marker='o', color='lightgreen', linestyle='-', linewidth=2, label='Average Level Reward')
        ax2.plot(avg_exploration_rewards.index, avg_exploration_rewards.values, marker='o', color='lightblue', linestyle='-', linewidth=2, label='Average Exploration Reward')
        ax2.plot(avg_heal_rewards.index, avg_heal_rewards.values, marker='o', color='pink', linestyle='-', linewidth=2, label='Average Heal Reward')
        ax2.plot(avg_faint_rewards.index, avg_faint_rewards.values, marker='o', color='yellow', linestyle='-', linewidth=2, label='Average Faint Reward')
        ax2.plot(avg_battle_rewards.index, avg_battle_rewards.values, marker='o', color='purple', linestyle='-', linewidth=2, label='Average Battle Reward')
        ax2.plot(avg_badge_rewards.index, avg_badge_rewards.values, marker='o', color='orange', linestyle='-', linewidth=2, label='Average Badge Reward')
        ax2.plot(avg_checkpoint_rewards.index, avg_checkpoint_rewards.values, marker='o', color='cyan', linestyle='-', linewidth=2, label='Average Checkpoint Reward')
        
        ax2.set_title('Average Rewards Against Total Agent Steps', color='white')
        ax2.set_xlabel('Total Run Steps', color='white')
        ax2.set_ylabel('Average Reward', color='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        ax2.legend(loc='upper left', facecolor='black', edgecolor='white', labelcolor='white')
    except Exception as e:
        print(f"Error updating graph: {e}")

# Use dark background
plt.style.use('dark_background')

# Setting up the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Creating the animation
ani = FuncAnimation(fig, update_graph, interval=(update_frequency*1000), cache_frame_data=False)

# Display the graphs
plt.tight_layout()
plt.show()