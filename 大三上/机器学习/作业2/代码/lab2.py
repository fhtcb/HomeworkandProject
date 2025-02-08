import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 定义维度和样本数量
dimensions = [5, 10, 20, 30]
N = 1000

# 存储模型方差
variances = []

for d in dimensions:
    # 生成随机数据
    X = np.random.randn(N, d)
    y = X[:, 0] * X[:, 1] * X[:, 2] + X[:, 2]**3 + np.random.randn(N)  # 目标变量包含一些噪声
    
    # 分割数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 使用三次多项式进行回归
    poly = PolynomialFeatures(degree=3)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    # 计算模型在测试集上的预测方差
    y_pred = model.predict(X_test_poly)
    variance = np.var(y_pred - y_test)
    variances.append(variance)

# 打印每个维度对应的模型方差
for d, var in zip(dimensions, variances):
    print(f" Model variance in dimension {d}: {var}")