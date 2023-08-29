import numpy as np

import time

# 获取运行的时间戳
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
HAM = now.split(" ")[-1].split(":")
print(int(HAM[0] + HAM[1]))


# 千瓦时计算
def calculate_Power(power):
    """ 输入为 瓦特， 转换为 千瓦时。 """
    return power / 1800 / 1000


rand = np.random.randint(5)

print(rand)

new = np.concatenate((12, 64, 1569, 15), axis=None)

print(new.shape)

ti = np.array([13])

reward = 2
reward -= 2 - 1

print(reward)

tt = 20
ii = 1
ss1 = 0
ss2 = 0
finish = (tt == ii or (ss1 == 0 and ss2 == 0))

print(finish)

a = np.array([[1, 2, 1, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [0, 0, 1, 0]])

a2 = a.dot(a)

a3 = a2.dot(a)

a4 = a3.dot(a)

print("A")
print(a)
print("A2")
print(a2)
print("A3")
print(a3)
print("A4")
print(a4)

print(sum(sum(a4)))

print(sum(sum(a3)) + sum(sum(a2)) + sum(sum(a)))

print(a + a2 + a3 + a4)
