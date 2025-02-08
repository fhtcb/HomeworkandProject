import numpy as np
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 加载训练数据
with open('train_feature.pkl', 'rb') as f:
    X_train = pickle.load(f)
y_train = np.load('train_labels.npy')

# 划分训练集和验证集
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# 训练随机森林模型
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 获取特征重要性
feature_importances = rf.feature_importances_

# 将特征重要性转换为 DataFrame
df_feature_importances = pd.DataFrame({
    'feature': range(X_train.shape[1]),
    'importance': feature_importances
})

# 按重要性排序
df_feature_importances = df_feature_importances.sort_values(by='importance', ascending=False)

# 归一化特征重要性（使用总和）
df_feature_importances['normalized_importance'] = df_feature_importances['importance'] / df_feature_importances['importance'].sum()

# 输出前20个最重要特征的序号及其重要性
print("Top 20 Feature Importances:")
print(df_feature_importances.head(20))