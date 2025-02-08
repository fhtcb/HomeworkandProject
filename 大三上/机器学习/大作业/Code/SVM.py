import numpy as np
import pickle
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import cross_validate, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, make_scorer
from sklearn.multiclass import OneVsOneClassifier
import pandas as pd

# 加载训练数据
with open('train_feature.pkl', 'rb') as f:
    X_train = pickle.load(f)
y_train = np.load('train_labels.npy')

# 从 pca_100.pkl 文件中加载降维到100维的数据
with open('train_pca_100.pkl', 'rb') as f:
    X_train_pca_100 = pickle.load(f)

# 从 pca_1000.pkl 文件中加载降维到1000维的数据
with open('train_pca_1000.pkl', 'rb') as f:
    X_train_pca_1000 = pickle.load(f)

# 定义10折交叉验证
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# 定义评估指标
scoring = {
    'accuracy': 'accuracy',
    'precision': make_scorer(precision_score, average='macro'),
    'recall': make_scorer(recall_score, average='macro')
}

# 训练和评估模型
def train_and_evaluate(model, X, y, kf, scoring):
    scores = cross_validate(model, X, y, cv=kf, scoring=scoring)
    return {
        'accuracy': np.mean(scores['test_accuracy']),
        'precision': np.mean(scores['test_precision']),
        'recall': np.mean(scores['test_recall'])
    }

# 原始数据上的 LinearSVC
model_linear_svc = LinearSVC(max_iter=10000)
results_linear_svc = train_and_evaluate(model_linear_svc, X_train, y_train, kf, scoring)
print(f'LinearSVC - Original Data - Accuracy: {results_linear_svc["accuracy"]:.4f}')
print(f'LinearSVC - Original Data - Precision: {results_linear_svc["precision"]:.4f}')
print(f'LinearSVC - Original Data - Recall: {results_linear_svc["recall"]:.4f}')

# 降维到100维数据上的 LinearSVC
results_pca_100_linear_svc = train_and_evaluate(model_linear_svc, X_train_pca_100, y_train, kf, scoring)
print(f'LinearSVC - PCA 100 - Accuracy: {results_pca_100_linear_svc["accuracy"]:.4f}')
print(f'LinearSVC - PCA 100 - Precision: {results_pca_100_linear_svc["precision"]:.4f}')
print(f'LinearSVC - PCA 100 - Recall: {results_pca_100_linear_svc["recall"]:.4f}')

# 降维到1000维数据上的 LinearSVC
results_pca_1000_linear_svc = train_and_evaluate(model_linear_svc, X_train_pca_1000, y_train, kf, scoring)
print(f'LinearSVC - PCA 1000 - Accuracy: {results_pca_1000_linear_svc["accuracy"]:.4f}')
print(f'LinearSVC - PCA 1000 - Precision: {results_pca_1000_linear_svc["precision"]:.4f}')
print(f'LinearSVC - PCA 1000 - Recall: {results_pca_1000_linear_svc["recall"]:.4f}')

# 加载测试数据
with open('test_feature.pkl', 'rb') as f:
    X_test = pickle.load(f)

# 从 test_pca_100.pkl 文件中加载降维到100维的测试数据
with open('test_pca_100.pkl', 'rb') as f:
    X_test_pca_100 = pickle.load(f)

# 从 test_pca_1000.pkl 文件中加载降维到1000维的测试数据
with open('test_pca_1000.pkl', 'rb') as f:
    X_test_pca_1000 = pickle.load(f)

# 预测测试数据
model_linear_svc.fit(X_train, y_train)
y_test_pred_linear_svc = model_linear_svc.predict(X_test)



# 使用降维后的数据进行预测
model_linear_svc.fit(X_train_pca_100, y_train)
y_test_pred_pca_100_linear_svc = model_linear_svc.predict(X_test_pca_100)

model_linear_svc.fit(X_train_pca_1000, y_train)
y_test_pred_pca_1000_linear_svc = model_linear_svc.predict(X_test_pca_1000)

# 保存测试结果到CSV文件
df_linear_svc = pd.DataFrame({'ID': range(len(y_test_pred_linear_svc)), 'label': y_test_pred_linear_svc})
df_linear_svc.to_csv('files/original_svm.csv', index=False)

df_pca_100_linear_svc = pd.DataFrame({'ID': range(len(y_test_pred_pca_100_linear_svc)), 'label': y_test_pred_pca_100_linear_svc})
df_pca_100_linear_svc.to_csv('files/pca_100_svm.csv', index=False)

df_pca_1000_linear_svc = pd.DataFrame({'ID': range(len(y_test_pred_pca_1000_linear_svc)), 'label': y_test_pred_pca_1000_linear_svc})
df_pca_1000_linear_svc.to_csv('files/pca_1000_svm.csv', index=False)