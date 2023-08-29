import os
import time

# 获取数据所在的路径
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
dataPath = rootPath + "\\Data"


# 读数据
def read_Data(fileName):
    """ 读取数据，返回一个列表 """
    c_list = []
    v_list = []
    p_list = []
    datafile = dataPath + "\\" + fileName
    with open(datafile, 'r') as fp:
        dataAll = fp.readlines()
    for data in dataAll:
        current = data.split("|")[1].split(":")[-1].split(" ")[2]
        voltage = data.split("|")[2].split(":")[-1].split(" ")[-2]
        power = data.split("|")[3].split(":")[-1].split(" ")[-1]
        c_list.append(current)
        v_list.append(voltage)
        p_list.append(power)
    return c_list, v_list, p_list


# 获取迭代次数
def get_Iteration(fileName):
    _, _, PV_Power = read_Data("\\PV\\" + fileName)
    return len(PV_Power)


# 读价格
def get_price(times, flag):
    """ 如果是售电，那么 flag = 1; 如果是购电，那么 flag = 0 """
    if 0 <= times < 800:
        if flag == 1:
            return 0.34 - 0.29
        elif flag == 0:
            return 0.34 + 0.29
        else:
            print("错误：请选择售电或购电！")
            return 0
    elif 800 <= times < 1400:
        if flag == 1:
            return 0.64 - 0.31
        elif flag == 0:
            return 0.64 + 0.31
        else:
            print("错误：请选择售电或购电！")
            return 0
    elif 1400 <= times < 1700:
        if flag == 1:
            return 1.04 - 0.14
        elif flag == 0:
            return 1.04 + 0.14
        else:
            print("错误：请选择售电或购电！")
            return 0
    elif 1700 <= times < 1900:
        if flag == 1:
            return 0.64 - 0.31
        elif flag == 0:
            return 0.64 + 0.31
        else:
            print("错误：请选择售电或购电！")
            return 0
    elif 1900 <= times < 2200:
        if flag == 1:
            return 1.04 - 0.19
        elif flag == 0:
            return 1.04 + 0.19
        else:
            print("错误：请选择售电或购电！")
            return 0
    elif 2200 <= times < 2400:
        if flag == 1:
            return 0.64 - 0.31
        elif flag == 0:
            return 0.64 + 0.31
        else:
            print("错误：请选择售电或购电！")
            return 0
    else:
        print("错误：请输入合理的时间！")
        return 0


# 读取平均电价
def get_Average_price():
    AVERAGE_PRICE = 1 / 8 * 0.63 + 1 / 6 * 0.95 + 1 / 3 * 1.18 + 1 / 2 * 0.95 + 1 / 3 * 1.23 + 1 / 2 * 0.95
    return AVERAGE_PRICE


# 获取当前时间
def get_time():
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    HAM = now.split(" ")[-1].split(":")
    return int(HAM[0] + HAM[1])

