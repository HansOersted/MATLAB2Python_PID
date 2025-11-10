import numpy as np
import matplotlib.pyplot as plt

def run_simulation(mv_input, pressure_input, coefficient_P_pressure, coefficient_P, coefficient_I, coefficient_D, Ts):
    # 检查数据
    t = mv_input[:, 0]  # 时间
    mv = mv_input[:, 1]  # mv 值

    pressure = pressure_input[:, 1]  # 提取压力数据
    
    # 计算前馈 mv
    mv_feedforward = pressure * coefficient_P_pressure  # 前馈 mv = 压力 * 比例系数
    
    # 计算跟踪误差 e = SV - PV
    # 在这里，e = SV - PV。假设你已经从其他数据中获取了 SV 和 PV，或者直接在数据文件中给出。
    # 注意：你需要正确读取并提供 SV 和 PV 数据，这里假设你已经从 CSV 里导入了 SV 和 PV。
    # 假设你有 SV 和 PV 数据，这里我直接用 mv_input 的第二列作为例子
    # 在实际情况中，SV 和 PV 应该是分别从你的数据中提取出来的
    e = mv_input[:, 1]  # 这里仅用 mv_input 的第二列作为误差 e（你可以替换为实际的跟踪误差计算）

    integral = np.zeros_like(e)
    derivative = np.zeros_like(e)
    mv_pid = np.zeros_like(e)

    for i in range(1, len(e)):
        # 积分
        integral[i] = integral[i-1] + coefficient_I * e[i] * Ts

        # 微分
        derivative[i] = coefficient_D * (e[i] - e[i-1]) / Ts

        # 比例
        P_term = coefficient_P * e[i]

        # 总和
        mv_pid[i] = P_term + integral[i] + derivative[i]

    # 最终的 mv 是前馈 mv 和 PID mv 相加
    mv_final = mv_feedforward + mv_pid

    # 绘图
    plt.figure()
    plt.plot(t, mv, label='Original MV Input', color='g')
    plt.plot(t, mv_feedforward, label='Feedforward MV', color='b', linestyle='--')
    plt.plot(t, mv_pid, label='PID MV', color='r', linestyle='-.')
    plt.plot(t, mv_final, label='Final MV (Feedforward + PID)', color='k', linestyle=':')
    plt.xlabel('Time')
    plt.ylabel('MV')
    plt.title('Simulink Model Output (MV Input & Feedforward MV & PID MV)')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
    
    return mv_input, mv_feedforward, mv_pid, mv_final
