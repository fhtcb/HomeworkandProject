import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, log_loss, make_scorer
from sklearn.decomposition import PCA
import pandas as pd

# 加载训练数据
with open('train_feature.pkl', 'rb') as f:
    X_train = pickle.load(f)
y_train = np.load('train_labels.npy')

with open('train_pca_100.pkl', 'rb') as f:
    X_train_pca_100 = pickle.load(f)

with open('train_pca_1000.pkl', 'rb') as f:
    X_train_pca_1000 = pickle.load(f)

# 定义10折交叉验证
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# 定义评估指标
scoring = {
    'accuracy': 'accuracy',
    'precision': make_scorer(precision_score, average='macro'),
    'recall': make_scorer(recall_score, average='macro'),
    'loss': make_scorer(log_loss, needs_proba=True)
}

# 训练使用 saga 求解器的逻辑回归模型
model_saga = LogisticRegression(max_iter=1000, solver='saga', n_jobs=-1)
scores_saga = cross_validate(model_saga, X_train, y_train, cv=kf, scoring=scoring)
print(f'SAGA Solver - Accuracy: {np.mean(scores_saga["test_accuracy"]):.4f}')
print(f'SAGA Solver - Precision: {np.mean(scores_saga["test_precision"]):.4f}')
print(f'SAGA Solver - Recall: {np.mean(scores_saga["test_recall"]):.4f}')
print(f'SAGA Solver - Loss: {np.mean(scores_saga["test_loss"]):.4f}')

# 训练使用 liblinear 求解器的逻辑回归模型
model_liblinear = LogisticRegression(max_iter=1000, solver='liblinear')
scores_liblinear = cross_validate(model_liblinear, X_train, y_train, cv=kf, scoring=scoring)
print(f'Liblinear Solver - Accuracy: {np.mean(scores_liblinear["test_accuracy"]):.4f}')
print(f'Liblinear Solver - CPrecision: {np.mean(scores_liblinear["test_precision"]):.4f}')
print(f'Liblinear Solver - Recall: {np.mean(scores_liblinear["test_recall"]):.4f}')
print(f'Liblinear Solver - Loss: {np.mean(scores_liblinear["test_loss"]):.4f}')

# 训练经过 PCA 处理后使用 saga 求解器的逻辑回归模型
model_pca_100_saga = LogisticRegression(max_iter=1000, solver='saga', n_jobs=-1)
scores_pca_100_saga = cross_validate(model_pca_100_saga, X_train_pca_100, y_train, cv=kf, scoring=scoring)
print(f'PCA 100 + SAGA Solver - Accuracy: {np.mean(scores_pca_100_saga["test_accuracy"]):.4f}')
print(f'PCA 100 + SAGA Solver - Precision: {np.mean(scores_pca_100_saga["test_precision"]):.4f}')
print(f'PCA 100 + SAGA Solver - Recall: {np.mean(scores_pca_100_saga["test_recall"]):.4f}')
print(f'PCA 100 + SAGA Solver - Loss: {np.mean(scores_pca_100_saga["test_loss"]):.4f}')

# 训练经过 PCA 处理后使用 liblinear 求解器的逻辑回归模型
model_pca_100_liblinear = LogisticRegression(max_iter=1000, solver='liblinear')
scores_pca_100_liblinear = cross_validate(model_pca_100_liblinear, X_train_pca_100, y_train, cv=kf, scoring=scoring)
print(f'PCA 100 + Liblinear Solver - Accuracy: {np.mean(scores_pca_100_liblinear["test_accuracy"]):.4f}')
print(f'PCA 100 + Liblinear Solver - Precision: {np.mean(scores_pca_100_liblinear["test_precision"]):.4f}')
print(f'PCA 100 + Liblinear Solver - Recall: {np.mean(scores_pca_100_liblinear["test_recall"]):.4f}')
print(f'PCA 100 + Liblinear Solver - Loss: {np.mean(scores_pca_100_liblinear["test_loss"]):.4f}')

# 训练经过 PCA 处理后使用 saga 求解器的逻辑回归模型
model_pca_1000_saga = LogisticRegression(max_iter=1000, solver='saga', n_jobs=-1)
scores_pca_1000_saga = cross_validate(model_pca_1000_saga, X_train_pca_1000, y_train, cv=kf, scoring=scoring)
print(f'PCA 1000 + SAGA Solver - Accuracy: {np.mean(scores_pca_1000_saga["test_accuracy"]):.4f}')
print(f'PCA 1000 + SAGA Solver - Precision: {np.mean(scores_pca_1000_saga["test_precision"]):.4f}')
print(f'PCA 1000 + SAGA Solver - Recall: {np.mean(scores_pca_1000_saga["test_recall"]):.4f}')
print(f'PCA 1000 + SAGA Solver - Loss: {np.mean(scores_pca_1000_saga["test_loss"]):.4f}')

# 训练经过 PCA 处理后使用 liblinear 求解器的逻辑回归模型
model_pca_1000_liblinear = LogisticRegression(max_iter=1000, solver='liblinear')
scores_pca_1000_liblinear = cross_validate(model_pca_1000_liblinear, X_train_pca_1000, y_train, cv=kf, scoring=scoring)
print(f'PCA 1000 + Liblinear Solver - Accuracy: {np.mean(scores_pca_1000_liblinear["test_accuracy"]):.4f}')
print(f'PCA 1000 + Liblinear Solver - Precision: {np.mean(scores_pca_1000_liblinear["test_precision"]):.4f}')
print(f'PCA 1000 + Liblinear Solver - Recall: {np.mean(scores_pca_1000_liblinear["test_recall"]):.4f}')
print(f'PCA 1000 + Liblinear Solver - Loss: {np.mean(scores_pca_1000_liblinear["test_loss"]):.4f}')

# 加载测试数据
with open('test_feature.pkl', 'rb') as f:
    X_test = pickle.load(f)

with open('test_pca_100.pkl', 'rb') as f:
    X_test_pca_100 = pickle.load(f)

with open('test_pca_1000.pkl', 'rb') as f:
    X_test_pca_1000 = pickle.load(f)

# 预测测试数据
model_saga.fit(X_train, y_train)
y_test_pred_saga = model_saga.predict(X_test)

model_liblinear.fit(X_train, y_train)
y_test_pred_liblinear = model_liblinear.predict(X_test)

model_pca_100_saga.fit(X_train_pca_100, y_train)
y_test_pred_pca_100_saga = model_pca_100_saga.predict(X_test_pca_100)

model_pca_100_liblinear.fit(X_train_pca_100, y_train)
y_test_pred_pca_100_liblinear = model_pca_100_liblinear.predict(X_test_pca_100)

model_pca_1000_saga.fit(X_train_pca_1000, y_train)
y_test_pred_pca_1000_saga = model_pca_1000_saga.predict(X_test_pca_1000)

model_pca_1000_liblinear.fit(X_train_pca_1000, y_train)
y_test_pred_pca_1000_liblinear = model_pca_1000_liblinear.predict(X_test_pca_1000)

# 保存测试结果到CSV文件
df_saga = pd.DataFrame({'ID': range(len(y_test_pred_saga)), 'label': y_test_pred_saga})
df_saga.to_csv('files/original_LR_saga.csv', index=False)

df_liblinear = pd.DataFrame({'ID': range(len(y_test_pred_liblinear)), 'label': y_test_pred_liblinear})
df_liblinear.to_csv('files/original_LR_liblinear.csv', index=False)

df_pca_100_saga = pd.DataFrame({'ID': range(len(y_test_pred_pca_100_saga)), 'label': y_test_pred_pca_100_saga})
df_pca_100_saga.to_csv('files/pca_100_LR_saga.csv', index=False)

df_pca_100_liblinear = pd.DataFrame({'ID': range(len(y_test_pred_pca_100_liblinear)), 'label': y_test_pred_pca_100_liblinear})
df_pca_100_liblinear.to_csv('files/pca_100_LR_liblinear.csv', index=False)

df_pca_1000_saga = pd.DataFrame({'ID': range(len(y_test_pred_pca_1000_saga)), 'label': y_test_pred_pca_1000_saga})
df_pca_1000_saga.to_csv('files/pca_1000_LR_saga.csv', index=False)

df_pca_1000_liblinear = pd.DataFrame({'ID': range(len(y_test_pred_pca_1000_liblinear)), 'label': y_test_pred_pca_1000_liblinear})
df_pca_1000_liblinear.to_csv('files/pca_1000_LR_liblinear.csv', index=False)