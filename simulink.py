import numpy as np
import matplotlib.pyplot as plt

def run_simulation(mv_input, pressure_input, e, coefficient_P_pressure, coefficient_P, coefficient_I, coefficient_D, Ts):
    # 检查数据
    t = mv_input[:, 0]  # 时间
    mv = mv_input[:, 1]  # mv 值

    pressure = pressure_input[:, 1]  # 提取压力数据
    
    # 计算前馈 mv
    mv_feedforward = pressure * coefficient_P_pressure  # 前馈 mv = 压力 * 比例系数
    
    # 使用传入的误差 e 进行 PID 控制
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

    # 计算离散微分（模拟 Simulink 中的 Discrete Derivative）
    mv_pid_derivative = np.zeros_like(mv_pid)
    for i in range(1, len(mv_pid)):
        mv_pid_derivative[i] = (mv_pid[i] - mv_pid[i-1]) / Ts  # 离散微分公式

    # **离散积分模块**（Forward Euler方法）作用于 mv_pid_derivative
    mv_pid_derivative_integrated = np.zeros_like(mv_pid_derivative)
    mv_pid_derivative_integrated[0] = 78.1  # 初始条件设为 78.1
    for i in range(1, len(mv_pid_derivative)):
        mv_pid_derivative_integrated[i] = mv_pid_derivative_integrated[i-1] + mv_pid_derivative[i] * Ts  # 离散积分

    # 最终的 mv 是前馈 mv 和积分后的 PID 微分相加
    mv_final = mv_feedforward + mv_pid_derivative_integrated  # 使用积分后的 PID 微分

    # 绘图
    plt.figure()
    plt.plot(t, mv, label='Original MV Input', color='g')
    plt.plot(t, mv_feedforward, label='Feedforward MV', color='b', linestyle='--')
    plt.plot(t, mv_pid, label='PID MV', color='r', linestyle='-.')
    plt.plot(t, mv_pid_derivative, label='PID Derivative MV', color='m', linestyle=':')
    plt.plot(t, mv_pid_derivative_integrated, label='PID Derivative Integrated MV', color='c', linestyle='-')
    plt.plot(t, mv_final, label='Final MV (Feedforward + Integrated PID Derivative)', color='k', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('MV')
    plt.title('Simulink Model Output (MV Input & Feedforward MV & PID MV & PID Derivative & Integrated PID Derivative)')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
    
    return mv_input, mv_feedforward, mv_pid, mv_pid_derivative, mv_pid_derivative_integrated, mv_final
