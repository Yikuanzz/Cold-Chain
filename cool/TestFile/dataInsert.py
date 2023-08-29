import numpy as np
import os

# 获取数据所在的路径
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
dataPath = rootPath + "\\Data"


# 读取数
def read_Data(fileName):
    """ 读取数据，返回一个列表 """
    c_list = []
    v_list = []
    p_list = []
    datafile = dataPath + "\\" + fileName
    with open(datafile, 'r') as fp:
        dataAll = fp.readlines()
    for data in dataAll:
        current = data.split("|")[1].split(":")[-1]
        voltage = data.split("|")[2].split(":")[-1]
        power = data.split("|")[3].split(":")[-1]
        c_list.append(current)
        v_list.append(voltage)
        p_list.append(power)
    return c_list, v_list, p_list


currentList, voltageList, powerList = read_Data("PV\\10_27_1700.txt")

Load_Current, Load_Voltage, Load_Power = read_Data("Load\\refrigerator.txt")

print(np.array(Load_Power).shape)
