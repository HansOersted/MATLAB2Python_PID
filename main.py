import numpy as np
from plot_figures_latest import plot_figures_latest
import matplotlib.pyplot as plt
from simulink import run_simulation

# Step 1: 导入数据并绘图
e, mv, PV, SV, pressure, time = plot_figures_latest()

# 数据输入模拟，按 Simulink 方式
n = 12000
t = np.arange(0, n * 10, 10)  # 每隔10秒，从0开始，列向量

# 数据喂给 Simulink 模型
e_input = np.column_stack((t, e[:n]))  # [时间, e值]
mv_input = np.column_stack((t, mv[:n]))  # [时间, mv值]
PV_input = np.column_stack((t, PV[:n]))
SV_input = np.column_stack((t, SV[:n]))

# 提取 pressure 输入数据
pressure_input = np.column_stack((t, pressure[:n]))

# 设置 PID 参数
coefficient_P = 1.111
coefficient_I = 0.0025
coefficient_D = 0.889
coefficient_P_pressure = -20  # 前馈系数
Ts = 10  # 采样时间

# Step 2: 调用 Simulink 模拟脚本并运行
simulink_output, mv_feedforward, mv_pid, mv_final = run_simulation(mv_input, pressure_input, coefficient_P_pressure, coefficient_P, coefficient_I, coefficient_D, Ts)

# Step 3: 绘制结果
plt.figure()
plt.plot(time, PV, '-b', label='PV')
plt.plot(time, SV, '--r', label='SV')
plt.plot(time, mv, '-.g', label='MV')
plt.plot(time, mv_feedforward, ':k', label='Feedforward MV')  # 绘制前馈 mv
plt.plot(time, mv_pid, '--m', label='PID MV')  # 绘制 PID mv
plt.plot(time, mv_final, '-k', label='Final MV (Feedforward + PID)')  # 绘制最终 mv
plt.xlabel('时间')
plt.ylabel('值')
plt.title('TIC3011 PV / SV / MV 变化曲线')
plt.legend(loc='best')
plt.grid(True)
plt.show()
