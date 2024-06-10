import torch
import numpy as np
from stable_baselines3 import PPO
from torchviz import make_dot
import gym
from gym.spaces import Dict, Box
import matplotlib.pyplot as plt

# Define your observation space
observation_space = Dict({
    'image': Box(low=0, high=255, shape=(72, 80, 3), dtype=np.uint8),
    'health': Box(low=0, high=1, shape=(1,), dtype=np.float32),
    'badges': Box(low=0, high=8, shape=(1,), dtype=np.float32),
    'levels': Box(low=0, high=600, shape=(1,), dtype=np.float32)
})

# Load your trained model
model = PPO.load("checkpoints\poke_8683520_steps.zip")

# Extract the policy (neural network)
policy = model.policy

# Check if the model is on GPU
device = next(policy.parameters()).device

# Create dummy input tensors for each sub-space and move them to the appropriate device
dummy_input = {
    'image': torch.zeros((1, 72, 80, 3), dtype=torch.uint8).permute(0, 3, 1, 2).to(device),  # permute to [batch, channels, height, width]
    'health': torch.zeros((1, 1), dtype=torch.float32).to(device),
    'badges': torch.zeros((1, 1), dtype=torch.float32).to(device),
    'levels': torch.zeros((1, 1), dtype=torch.float32).to(device)
}

# Ensure the dummy input dictionary is in the format expected by the policy
dummy_input = {key: value for key, value in dummy_input.items()}

# Hook to capture activations
activations = {}

def get_activation(name):
    def hook(model, input, output):
        activations[name] = output.detach()
    return hook

# Register hooks to the layers you are interested in
policy.features_extractor.cnn[0].register_forward_hook(get_activation('conv1'))
policy.features_extractor.cnn[2].register_forward_hook(get_activation('conv2'))
policy.features_extractor.cnn[4].register_forward_hook(get_activation('conv3'))

# Perform a forward pass using the dummy input to get the output
output = policy(dummy_input)

# Visualize the neural network
dot = make_dot(output, params=dict(policy.named_parameters()))
dot.render("sb3_neural_network", format="png")

# Plot the activations of specific layers
for layer_name, activation in activations.items():
    num_neurons = activation.shape[1]
    fig, axes = plt.subplots(1, num_neurons, figsize=(num_neurons * 2, 2))
    for i in range(num_neurons):
        axes[i].imshow(activation[0, i].cpu().numpy(), cmap='viridis')
        axes[i].axis('off')
    plt.suptitle(f'Activations of {layer_name}')
    plt.show()
