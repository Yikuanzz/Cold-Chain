import time
import numpy as np
import torch.optim
from DQN_Agent import DQNAgent
from DQN_modules import MLP
from DQN_Utiles import plot_reward
from MicroGrid_Env import MG_Env


class TrainManager:
    def __init__(self, environment, episodes=20000, lr=0.001, gamma=0.9, e_greed=0.1):
        self.env = environment
        self.episodes = episodes
        # Build the Agent
        n_obs = env.observation_space.shape[0]
        n_act = env.action_space.n
        q_func = MLP(n_obs, n_act)
        optimizer = torch.optim.Adam(q_func.parameters(), lr=lr)
        self.agent = DQNAgent(
            q_func=q_func,
            optimizer=optimizer,
            n_action=n_act,
            gamma=gamma,
            e_greed=e_greed
        )

    def train_episode(self):
        """Training in one episode"""
        total_reward = 0  # Definite the total reward
        obs = self.env.reset()  # Reset the environment
        obs = torch.FloatTensor(obs)  # Change the data type
        while True:
            # Interactive
            action = self.agent.action(obs)
            next_obs, reward, done, info = self.env.step(action)
            next_obs = torch.FloatTensor(next_obs)  # Change the data type
            # Update the Agent
            self.agent.step(obs, action, reward, next_obs, done)
            # Update the State of Agent
            obs = next_obs
            total_reward += reward
            # print(action, reward)

            if done:
                break
        return total_reward

    def test_episode(self):
        """Test the episode"""
        total_reward = 0  # Definite the total reward
        obs = self.env.reset()  # Reset the environment
        obs = torch.FloatTensor(obs)
        while True:
            # 1. Choose the best action in Q_table
            action = self.agent.predict(obs)

            # 2. Interactivity
            next_obs, reward, done, _ = self.env.step(action)

            # 3. Cumulate the reward
            total_reward += reward

            # 4. Update the state
            obs = next_obs

            # 5. Render the environment
            self.env.render()
            time.sleep(0.5)
            if done:
                break
            return total_reward

    def train(self):
        rewards_record = []
        test_rewards = []
        """Train our Agent"""
        for e in range(self.episodes):
            ep_reward = self.train_episode()
            rewards_record.append(ep_reward)
            print('Episode %s: reward = %.8f' % (e + 1, ep_reward))

            if e % 100 == 0:
                test_reward = self.test_episode()
                test_rewards.append(test_reward)
                print('test reward = %.8f' % test_reward)
        plot_reward(x=np.arange(1, int(self.episodes / 100) + 1), y=np.array(test_rewards))
        plot_reward(x=np.arange(1, self.episodes + 1), y=np.array(rewards_record))


if __name__ == '__main__':
    env = MG_Env("10_31_1300.txt")
    TrainM = TrainManager(env)
    TrainM.train()
