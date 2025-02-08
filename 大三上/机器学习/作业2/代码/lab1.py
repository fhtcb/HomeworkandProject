import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gammaln

# 定义维度和样本数量
dimensions = [1000, 500, 100, 3]
N = 10000

# 创建一个图形
plt.figure(figsize=(12, 8))

for d in dimensions:
    # 生成高斯分布的随机数据
    data = np.random.randn(N, d)
    
    # 计算每个样本与原点的距离
    distances = np.linalg.norm(data, axis=1)
    
    # 绘制距离的分布函数
    plt.hist(distances, bins=100, density=True, alpha=0.6, label=f'd={d}')
    
    # 计算并绘制概率密度函数
    y = np.linspace(1e-10, np.max(distances), 1000)  # 避免从零开始
    log_pdf = (d-1) * np.log(y) - y**2 / 2 - (d/2 - 1) * np.log(2) - gammaln(d/2)
    pdf = np.exp(log_pdf)
    plt.plot(y, pdf, linewidth=2)

# 添加图例和标签
plt.title('Distribution of distances from the origin')
plt.xlabel('Distances')
plt.ylabel('Density')
plt.legend()
plt.show()