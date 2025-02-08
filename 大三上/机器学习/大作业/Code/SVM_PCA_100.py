import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, make_scorer
import pandas as pd

# 加载降维到100维的训练数据
with open('train_pca_100.pkl', 'rb') as f:
    X_train_pca_100 = pickle.load(f)
y_train = np.load('train_labels.npy')

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

# 使用多项式核函数（degree=2）的 SVC
model_poly_svc_2 = SVC(kernel='poly', degree=2, max_iter=10000)
results_poly_svc_2 = train_and_evaluate(model_poly_svc_2, X_train_pca_100, y_train, kf, scoring)
print(f'SVC with Polynomial Kernel (degree=2) - PCA 100 - Accuracy: {results_poly_svc_2["accuracy"]:.4f}')
print(f'SVC with Polynomial Kernel (degree=2) - PCA 100 - Precision: {results_poly_svc_2["precision"]:.4f}')
print(f'SVC with Polynomial Kernel (degree=2) - PCA 100 - Recall: {results_poly_svc_2["recall"]:.4f}')

# 使用多项式核函数（degree=3）的 SVC
model_poly_svc_3 = SVC(kernel='poly', degree=3, max_iter=10000)
results_poly_svc_3 = train_and_evaluate(model_poly_svc_3, X_train_pca_100, y_train, kf, scoring)
print(f'SVC with Polynomial Kernel (degree=3) - PCA 100 - Accuracy: {results_poly_svc_3["accuracy"]:.4f}')
print(f'SVC with Polynomial Kernel (degree=3) - PCA 100 - Precision: {results_poly_svc_3["precision"]:.4f}')
print(f'SVC with Polynomial Kernel (degree=3) - PCA 100 - Recall: {results_poly_svc_3["recall"]:.4f}')

# 使用高斯核函数的 SVC
model_rbf_svc = SVC(kernel='rbf', max_iter=10000)
results_rbf_svc = train_and_evaluate(model_rbf_svc, X_train_pca_100, y_train, kf, scoring)
print(f'SVC with RBF Kernel - PCA 100 - Accuracy: {results_rbf_svc["accuracy"]:.4f}')
print(f'SVC with RBF Kernel - PCA 100 - Precision: {results_rbf_svc["precision"]:.4f}')
print(f'SVC with RBF Kernel - PCA 100 - Recall: {results_rbf_svc["recall"]:.4f}')

# 加载降维到100维的测试数据
with open('test_pca_100.pkl', 'rb') as f:
    X_test_pca_100 = pickle.load(f)

# 预测测试数据
model_poly_svc_3.fit(X_train_pca_100, y_train)
y_test_pred_poly_svc_3 = model_poly_svc_3.predict(X_test_pca_100)

model_poly_svc_2.fit(X_train_pca_100, y_train)
y_test_pred_poly_svc_2 = model_poly_svc_2.predict(X_test_pca_100)

model_rbf_svc.fit(X_train_pca_100, y_train)
y_test_pred_rbf_svc = model_rbf_svc.predict(X_test_pca_100)

# 保存测试结果到CSV文件
df_poly_svc_3 = pd.DataFrame({'ID': range(len(y_test_pred_poly_svc_3)), 'label': y_test_pred_poly_svc_3})
df_poly_svc_3.to_csv('files/pca_100_poly_svc_3.csv', index=False)

df_poly_svc_2 = pd.DataFrame({'ID': range(len(y_test_pred_poly_svc_2)), 'label': y_test_pred_poly_svc_2})
df_poly_svc_2.to_csv('files/pca_100_poly_svc_2.csv', index=False)

df_rbf_svc = pd.DataFrame({'ID': range(len(y_test_pred_rbf_svc)), 'label': y_test_pred_rbf_svc})
df_rbf_svc.to_csv('files/pca_100_rbf_svc.csv', index=False)