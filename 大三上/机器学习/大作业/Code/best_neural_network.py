import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 加载训练数据
with open('train_feature.pkl', 'rb') as f:
    X_train = pickle.load(f)
y_train = np.load('train_labels.npy')

# 划分验证集
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# 构建神经网络模型
model = Sequential([
    Dense(512, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.7),
    Dense(256, activation='relu'),
    Dropout(0.7),
    Dense(128, activation='relu'),
    Dropout(0.7),
    Dense(20, activation='softmax')  
])

# 编译模型
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 训练模型
history = model.fit(X_train, y_train, epochs=60, batch_size=32, validation_data=(X_val, y_val))

# 验证模型
y_val_pred = np.argmax(model.predict(X_val), axis=1)
val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred, average='macro')
val_recall = recall_score(y_val, y_val_pred, average='macro')
val_loss = history.history['val_loss'][-1]

print(f'Validation Accuracy: {val_accuracy:.4f}')
print(f'Validation Precision: {val_precision:.4f}')
print(f'Validation Recall: {val_recall:.4f}')
print(f'Validation Loss: {val_loss:.4f}')

# 加载测试数据
with open('test_feature.pkl', 'rb') as f:
    X_test = pickle.load(f)

# 预测测试数据
y_test_pred = np.argmax(model.predict(X_test), axis=1)

# 保存测试结果到CSV文件
df = pd.DataFrame({'ID': range(len(y_test_pred)), 'label': y_test_pred})
df.to_csv('files/best_nn.csv', index=False)