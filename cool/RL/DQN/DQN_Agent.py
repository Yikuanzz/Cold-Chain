import numpy as np
import torch


class DQNAgent:

    def __init__(self, q_func, optimizer, n_action, e_greed=0.1, gamma=0.9):
        self.q_func = q_func  # Q Function : A neural Network
        self.criterion = torch.nn.MSELoss()  # Loss Function : Mean Square Error
        self.optimizer = optimizer  # Optimizer : Optimization Function
        self.n_action = n_action  # Number of action : Discrete action's number
        self.e_greed = e_greed  # Greedy Rate : To choose the action
        self.gamma = gamma  # Discount Rate : To control the rewards in the future

    def predict(self, obs):
        """Predict the next action greedily"""
        Q_list = self.q_func(obs)  # Get the action reward in the observation
        action = int(torch.argmax(Q_list).detach().numpy())  # Change to the numpy
        return action

    def action(self, obs):
        """Get the action"""
        if np.random.uniform(0, 1) < self.e_greed:  # Use Greedy Rate
            action = np.random.choice(self.n_action)  # Exploration
        else:
            action = self.predict(obs)  # Exploitation
        return action

    def step(self, obs, action, reward, next_obs, done):
        """Update the Q_Function"""
        predict_Q = self.q_func(obs)[action]
        target_Q = reward + (1 - float(done)) * self.gamma * self.q_func(next_obs).max()
        # Update parameters
        self.optimizer.zero_grad()
        loss = self.criterion(predict_Q, target_Q)
        loss.backward()
        self.optimizer.step()
