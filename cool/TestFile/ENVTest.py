import torch
from MicroGrid_Env import MG_Env

env = MG_Env("10_27_1700.txt")

total_reward = 0  # Definite the total reward
obs = env.reset()  # Reset the environment
obs = torch.FloatTensor(obs)  # Change the data type
while True:
    # Interactive
    action = 5
    next_obs, reward, done, info = env.step(action)
    print(reward)
    if done:
        break



