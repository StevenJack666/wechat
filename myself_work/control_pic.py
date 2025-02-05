
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'

# 假设我们有一组子组数据
subgroup_data = np.random.normal(100, 5, (20, 5))  # 20个子组，每个子组5个数据点

# 计算每个子组的范围（最大值与最小值之差）
subgroup_ranges = np.max(subgroup_data, axis=1) - np.min(subgroup_data, axis=1)

# 计算中心线（平均范围）
center_line = np.mean(subgroup_ranges)

# 计算控制限（这里使用3倍标准差）
std_dev = np.std(subgroup_ranges)
upper_control_limit = center_line + 3 * std_dev
lower_control_limit = center_line - 3 * std_dev

# 绘制R控制图
plt.figure(figsize=(10, 5))
plt.plot(subgroup_ranges, marker='o', linestyle='-', color='blue')
plt.axhline(center_line, color='green', linestyle='-', label='中心线')
# 绘制控制限
plt.axhline(y=upper_control_limit, color='red', linestyle='--', label='UCL')
plt.axhline(y=lower_control_limit, color='red', linestyle='--', label='LCL')

plt.legend()
plt.xlabel('子组编号')
plt.ylabel('范围')
plt.title('R Control Chart')
plt.show()