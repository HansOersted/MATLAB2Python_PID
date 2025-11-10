import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_figures_latest():
    # 读取 CSV 文件
    filename = '12000点测试数据.csv'
    df = pd.read_csv(filename, encoding='utf-8')

    # 提取时间列
    time_str = df['时间']
    time = pd.to_datetime(time_str, format='%Y-%m-%d %H:%M:%S')

    # 提取 PV, SV, MV
    PV = df['TIC3011_1.PV']
    SV = df['TIC3011_1.SV']
    MV = df['TIC3011_1.MV']
    
    # 蒸气压
    pressure = df['PI3001.PV']

    # 转为列向量
    PV = PV.values
    SV = SV.values
    mv = MV.values  # 控制器输出，导出变量名为 mv
    e = SV - PV    # tracking error，导出变量名为 e

    # 返回数据
    return e, mv, PV, SV, pressure, time
