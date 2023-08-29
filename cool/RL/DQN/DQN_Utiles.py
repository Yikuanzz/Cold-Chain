from matplotlib import pyplot as plt


def plot_reward(x, y):
    plt.xlabel("Step")
    plt.ylabel("Total Reward")
    plt.plot(x, y)
    plt.show()
