import numpy as np
from abc import ABC
import gym
from gym import spaces
from pygame_cool import run
from Utils import dataProcess
from Utils.calculateFunc import calculate_Power

"""
    action 0 : 电池 + 光伏 -> 负载
    action 1 : 电池 -> 负载
    action 2 : 蓄电池 + 光伏 -> 负载
    action 3 : 蓄电池 -> 负载 
    action 4 : 光伏 -> 蓄电池
    action 5 : 光伏 -> 动力电池 
"""
N_DISCRETE_ACTIONS = 6

# Battery characteristics (KWh)
DEFAULT_BAT_CAPACITY = 5
DEFAULT_MAX_CHARGE = 3  # (KW)
DEFAULT_MAX_DISCHARGE = 3  # (KW)

DEFAULT_MAX_SOC = 0.9
DEFAULT_MIN_SOC = 0.1
DEFAULT_INI_CAP = 0.4
DEFAULT_BAT_EFFICIENCY = 0.95


class Battery:
    def __init__(self, max_cap, max_charge, max_discharge, efficiency, ini_cap):
        self.current_cap = ini_cap  # 当前电池容量百分比
        self.max_cap = max_cap  # 电池容量
        self.ini_cap = ini_cap  # 电池初始容量
        self.max_charge = max_charge  # 最大充电能量大小
        self.max_discharge = max_discharge  # 最大放电能量大小
        self.efficiency = efficiency  # 充放电效率

    def charge(self, energy):
        """ 充电成功返回1；失败返回0 """
        temp_energy = energy
        if energy > self.max_charge:
            temp_energy = self.max_charge
        if energy < 0:
            temp_energy = 0

        current_cap = (self.current_cap * self.max_cap + temp_energy * self.efficiency) / self.max_cap

        if current_cap > 0.95:
            return 0
        else:
            self.current_cap = current_cap
            return 1

    def discharge(self, energy):
        """ 放电成功返回1；失败返回0 """
        temp_energy = energy
        if energy > self.max_discharge:
            temp_energy = self.max_discharge
        if energy < 0:
            temp_energy = 0

        current_cap = (self.current_cap * self.max_cap - temp_energy / self.efficiency) / self.max_cap

        if current_cap < 0.05:
            return 0
        else:
            self.current_cap = current_cap
            return 1

    def SOC(self):
        return self.current_cap

    def reset(self):
        self.current_cap = self.ini_cap


class PV:
    def __init__(self, fileName):
        self.cur_time = 0
        self.dataPath = "\\PV\\" + fileName
        self.cur_Power = self.get_Power()

    def get_Power(self):
        if self.dataPath == "\\PV\\":
            return print("错误：没有加载数据！")
        _, _, PV_Power = dataProcess.read_Data(self.dataPath)

        if self.cur_time == len(PV_Power):
            self.cur_time = 0
        else:
            self.cur_time = self.cur_time + 1
        cur_Power = PV_Power[self.cur_time - 1]

        if self.cur_time != 1:
            self.cur_Power = cur_Power
        return cur_Power

    def reset(self):
        self.cur_time = 0


class Load:
    def __init__(self):
        self.cur_time = 0
        self.cur_Power = self.get_Power()

    def get_Power(self):
        _, _, Load_Power = dataProcess.read_Data("Load\\refrigerator.txt")

        # 不断重复该池内数据
        if self.cur_time == len(Load_Power):
            self.cur_time = 0
        else:
            self.cur_time = self.cur_time + 1

        cur_Power = Load_Power[self.cur_time - 1]

        if self.cur_time != 1:
            self.cur_Power = cur_Power
        return cur_Power

    def reset(self):
        self.cur_time = 0


class MG_Env(gym.Env, ABC):
    def __init__(self, fileName):
        super(MG_Env, self).__init__()
        # max_cap (W), max_charge(W), max_discharge(W), efficiency, ini_cap
        self.B1 = Battery(1800 * 20, 3000, 3000, 0.95, 1)  # 蓄电池
        self.B2 = Battery(1800 * 10, 1500, 1500, 0.95, 1)  # 动力电池
        self.Time = 0
        self.L = Load()
        self.PV = PV(fileName)
        self.iterations = dataProcess.get_Iteration(fileName)
        self.current_reward = 0
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # 观察值：电池1的电量、电池2的电量、光伏发电量、负荷耗电量、次数
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, 0), dtype=np.float32)
        # 设置电池状态：1 为正常状态，0 为不正常状态
        self.reward_set = 1
        self.B1State = 1
        self.B2State = 1
        self.cur_action = 0

    def get_reward(self, action):
        self.cur_action = action
        reward = 0
        if action == 0:
            """ 电池 + 光伏 -> 负载"""
            B_Power = float(self.L.cur_Power) - float(self.PV.cur_Power)
            if self.B2.discharge(B_Power) == 1:
                self.B2State = 1
                reward -= dataProcess.get_Average_price() * calculate_Power(B_Power)
            else:
                self.B2State = 0
                print("A0错误：动力电池电力不足！")
                if self.B1.discharge(B_Power) == 0:
                    print("A0错误：蓄电池电力不足！")
                    self.B1State = 0
                reward -= self.reward_set
            self.current_reward = reward
            return reward

        elif action == 1:
            """ 电池 -> 负载 """
            B_Power = float(self.L.cur_Power)
            if self.B2.discharge(B_Power) == 1:
                self.B2State = 1
                reward -= dataProcess.get_Average_price() * (calculate_Power(B_Power) +
                                                             calculate_Power(float(self.PV.cur_Power)))
            else:
                self.B2State = 0
                print("A1错误：动力电池电力不足！")
                if self.B1.discharge(B_Power) == 0:
                    print("A1错误：蓄电池电力不足！")
                    self.B1State = 0
                reward -= self.reward_set
            self.current_reward = reward
            return reward

        elif action == 2:
            """ 蓄电池 + 光伏 -> 负载 """
            B_Power = float(self.L.cur_Power) - float(self.PV.cur_Power)
            if self.B1.discharge(B_Power) == 1:
                self.B1State = 1
                reward -= dataProcess.get_price(dataProcess.get_time(), 0) * calculate_Power(B_Power)
            else:
                print("A2错误：蓄电池电力不足！")
                self.B1State = 0
                reward -= self.reward_set
            self.current_reward = reward
            return reward

        elif action == 3:
            """ 蓄电池 -> 负载 """
            B_Power = float(self.L.cur_Power)
            if self.B1.discharge(B_Power) == 1:
                reward -= dataProcess.get_price(dataProcess.get_time(), 0) * calculate_Power(B_Power) \
                          + dataProcess.get_price(dataProcess.get_time(), 1) * calculate_Power(float(self.PV.cur_Power))
                self.B1State = 1
            else:
                print("A3错误：蓄电池电力不足！")
                self.B1State = 0
                reward -= self.reward_set
            self.current_reward = reward
            return reward

        elif action == 4:
            """ 光伏 -> 蓄电池 """
            B_Power = float(self.PV.cur_Power)
            if self.B1.charge(B_Power) == 1:
                reward += dataProcess.get_price(dataProcess.get_time(), 1) * calculate_Power(B_Power) \
                          - dataProcess.get_price(dataProcess.get_time(), 0) * calculate_Power(float(self.L.cur_Power))
                self.B1State = 1
            else:
                reward -= self.reward_set
            self.current_reward = reward
            if self.B2.discharge(float(self.L.cur_Power)) == 0:
                self.B2State = 0
                if self.B1.discharge(float(self.L.cur_Power)) == 0:
                    self.B1State = 0
            return reward

        elif action == 5:
            """ 光伏 -> 动力电池 """
            B_Power = float(self.PV.cur_Power)
            if self.B2.charge(B_Power) == 1:
                reward += dataProcess.get_Average_price() * calculate_Power((B_Power - float(self.L.cur_Power)))
                self.B2State = 1
            else:
                reward -= self.reward_set
            self.current_reward = reward
            if self.B2.discharge(float(self.L.cur_Power)) == 0:
                self.B2State = 0
                if self.B1.discharge(float(self.L.cur_Power)) == 0:
                    self.B1State = 0
            return reward

    def _build_state(self):
        obs = np.concatenate((np.array([float(self.B1.current_cap), float(self.B2.current_cap),
                                        float(self.PV.cur_Power), float(self.L.cur_Power)]),
                              np.array([self.Time])), axis=None)
        return obs

    def get_state(self):
        """ 环境观察值为一维向量 """
        return self._build_state()

    def step(self, action):
        self.PV.get_Power()
        self.L.get_Power()
        self.Time += 1
        reward = self.get_reward(action)
        finish = (self.Time == self.iterations or (self.B1State == 0 and self.B2State == 0))
        if finish:
            self.reset()
        next_obs = self._build_state()
        info_d = {}
        return next_obs, reward, finish, info_d

    def reset(self, seed=None, return_info=False, options=None):
        self.B1.reset()
        self.B2.reset()
        self.PV.reset()
        self.L.reset()
        self.Time = 0
        return self._build_state()

    def render(self, mode="human", close=False, run_pygame=True):
        if run_pygame:
            obj_list = [self.Time, int(self.B1.current_cap * 100),
                        int(self.B2.current_cap * 100),
                        int(float(self.PV.cur_Power)),
                        int(float(self.L.cur_Power)),
                        self.cur_action]
            run(obj_list)
        print('time={}, B1={}%, B2={}%, PV={}W, L={}W, Reward={}\n'.format(self.Time, int(self.B1.current_cap * 100),
                                                                           int(self.B2.current_cap * 100),
                                                                           self.PV.cur_Power,
                                                                           self.L.cur_Power,
                                                                           self.current_reward * 10000))


# 测试一下坏境
if __name__ == '__main__':
    env = MG_Env("10_31_1300.txt")
    rewards = []
    current_state = env.reset()
    for _ in range(100):
        rand_Action = np.random.randint(5)
        _, cur_reward, done, _ = env.step(rand_Action)
        env.render()
        rewards.append(cur_reward)
    print(f"total reward {sum(rewards)}")
