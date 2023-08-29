import argparse
import numpy as np
from MicroGrid_Env import MG_Env
from RL.D3QN.D3QN import D3QN
from Utils.plotFunction import plot_learning_curve


parser = argparse.ArgumentParser()
parser.add_argument('--max_episodes', type=int, default=1000)
parser.add_argument('--ckpt_dir', type=str, default='./checkpoints/D3QN/')
parser.add_argument('--reward_path', type=str, default='./output_images/test_reward.png')
parser.add_argument('--epsilon_path', type=str, default='./output_images/test_epsilon.png')

args = parser.parse_args()


def main(dataName):
    env = MG_Env(dataName)
    # env = gym.make('LunarLander-v2')
    agent = D3QN(alpha=0.0003, state_dim=env.observation_space.shape[0], action_dim=env.action_space.n,
                 fc1_dim=256, fc2_dim=256, ckpt_dir=args.ckpt_dir, gamma=0.99, tau=0.005, epsilon=1.0,
                 eps_end=0.05, eps_dec=5e-4, max_size=1000000, batch_size=256)
    agent.load_models(episode=4000)
    total_rewards, avg_rewards, epsilon_history = [], [], []

    for episode in range(args.max_episodes):
        total_reward = 0
        done = False
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation, isTrain=False)
            print(action)
            observation_, reward, done, info = env.step(action)
            # agent.remember(observation, action, reward, observation_, done)
            # agent.learn()
            total_reward += reward
            observation = observation_
            env.render()

        total_rewards.append(total_reward)
        avg_reward = np.mean(total_rewards[-100:])
        avg_rewards.append(avg_reward)
        epsilon_history.append(agent.epsilon)
        print('EP:{} Reward:{} Avg_reward:{} Epsilon:{}'.
              format(episode + 1, total_reward, avg_reward, agent.epsilon))

    episodes = [i + 1 for i in range(args.max_episodes)]
    plot_learning_curve(episodes, avg_rewards, title='Reward', ylabel='reward',
                        figure_file=args.reward_path)
    plot_learning_curve(episodes, epsilon_history, title='Epsilon', ylabel='epsilon',
                        figure_file=args.epsilon_path)


if __name__ == '__main__':
    main("10_31_1300.txt")
