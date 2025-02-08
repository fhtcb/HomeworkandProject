import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pickle

# 从文件中加载训练数据
with open('train_feature.pkl', 'rb') as f:
    X = pickle.load(f)

y = np.load('train_labels.npy')

# 使用t-SNE将数据降维到二维
tsne = TSNE(n_components=2, random_state=0, init='random')

# 可视化label为1~10的数据
mask_1_10 = (y >= 1) & (y <= 10)
X_tsne_1_10 = tsne.fit_transform(X[mask_1_10])
y_1_10 = y[mask_1_10]

plt.figure(figsize=(8, 6))
for i in range(1, 11):
    plt.scatter(X_tsne_1_10[y_1_10 == i, 0], X_tsne_1_10[y_1_10 == i, 1], label=f'Class {i}')
plt.xlabel('t-SNE feature 1')
plt.ylabel('t-SNE feature 2')
plt.title('t-SNE visualization of training data (labels 1-10)')
plt.legend()
plt.show()

# 可视化label为11~20的数据
mask_11_20 = (y >= 11) & (y <= 20)
X_tsne_11_20 = tsne.fit_transform(X[mask_11_20])
y_11_20 = y[mask_11_20]

plt.figure(figsize=(8, 6))
for i in range(11, 21):
    plt.scatter(X_tsne_11_20[y_11_20 == i, 0], X_tsne_11_20[y_11_20 == i, 1], label=f'Class {i}')
plt.xlabel('t-SNE feature 1')
plt.ylabel('t-SNE feature 2')
plt.title('t-SNE visualization of training data (labels 11-20)')
plt.legend()
plt.show()