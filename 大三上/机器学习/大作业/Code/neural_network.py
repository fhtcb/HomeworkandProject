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

# 划分训练集和验证集
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# 构建神经网络模型（无 Dropout）
def create_model(input_shape, activation):
    model = Sequential([
        Dense(512, activation=activation, input_shape=(input_shape,)),
        Dense(256, activation=activation),
        Dense(128, activation=activation),
        Dense(20, activation='softmax')  # 假设有20个类别
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# 构建神经网络模型（有 Dropout）
def create_model_with_dropout(input_shape, activation):
    model = Sequential([
        Dense(512, activation=activation, input_shape=(input_shape,)),
        Dropout(0.5),
        Dense(256, activation=activation),
        Dropout(0.5),
        Dense(128, activation=activation),
        Dropout(0.5),
        Dense(20, activation='softmax')  # 假设有20个类别
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# 训练和评估模型
def train_and_evaluate(X_train, y_train, X_val, y_val, activation, use_dropout=False):
    if use_dropout:
        model = create_model_with_dropout(X_train.shape[1], activation)
    else:
        model = create_model(X_train.shape[1], activation)
    
    history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_val, y_val))
    
    y_val_pred = np.argmax(model.predict(X_val), axis=1)
    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_precision = precision_score(y_val, y_val_pred, average='macro')
    val_recall = recall_score(y_val, y_val_pred, average='macro')
    val_loss = history.history['val_loss'][-1]
    
    print(f'Validation Accuracy ({activation}, Dropout={use_dropout}): {val_accuracy:.4f}')
    print(f'Validation Precision ({activation}, Dropout={use_dropout}): {val_precision:.4f}')
    print(f'Validation Recall ({activation}, Dropout={use_dropout}): {val_recall:.4f}')
    print(f'Validation Loss ({activation}, Dropout={use_dropout}): {val_loss:.4f}')
    
    return model

# 训练使用 ReLU 激活函数的模型（无 Dropout）
print("Training on original data with ReLU activation (no Dropout):")
model_relu = train_and_evaluate(X_train, y_train, X_val, y_val, 'relu')

# 训练使用 Sigmoid 激活函数的模型（无 Dropout）
print("Training on original data with Sigmoid activation (no Dropout):")
model_sigmoid = train_and_evaluate(X_train, y_train, X_val, y_val, 'sigmoid')

# 训练使用 Tanh 激活函数的模型（无 Dropout）
print("Training on original data with Tanh activation (no Dropout):")
model_tanh = train_and_evaluate(X_train, y_train, X_val, y_val, 'tanh')

# 训练使用 ReLU 激活函数的模型（有 Dropout）
print("Training on original data with ReLU activation (with Dropout):")
model_relu_dropout = train_and_evaluate(X_train, y_train, X_val, y_val, 'relu', use_dropout=True)

# 训练使用 Sigmoid 激活函数的模型（有 Dropout）
print("Training on original data with Sigmoid activation (with Dropout):")
model_sigmoid_dropout = train_and_evaluate(X_train, y_train, X_val, y_val, 'sigmoid', use_dropout=True)

# 训练使用 Tanh 激活函数的模型（有 Dropout）
print("Training on original data with Tanh activation (with Dropout):")
model_tanh_dropout = train_and_evaluate(X_train, y_train, X_val, y_val, 'tanh', use_dropout=True)

# 加载测试数据
with open('test_feature.pkl', 'rb') as f:
    X_test = pickle.load(f)

# 预测测试数据
y_test_pred_relu = np.argmax(model_relu.predict(X_test), axis=1)
y_test_pred_sigmoid = np.argmax(model_sigmoid.predict(X_test), axis=1)
y_test_pred_tanh = np.argmax(model_tanh.predict(X_test), axis=1)

y_test_pred_relu_dropout = np.argmax(model_relu_dropout.predict(X_test), axis=1)
y_test_pred_sigmoid_dropout = np.argmax(model_sigmoid_dropout.predict(X_test), axis=1)
y_test_pred_tanh_dropout = np.argmax(model_tanh_dropout.predict(X_test), axis=1)

# 保存测试结果到CSV文件
df_relu = pd.DataFrame({'ID': range(len(y_test_pred_relu)), 'label': y_test_pred_relu})
df_relu.to_csv('files/original_FC_relu.csv', index=False)

df_sigmoid = pd.DataFrame({'ID': range(len(y_test_pred_sigmoid)), 'label': y_test_pred_sigmoid})
df_sigmoid.to_csv('files/original_FC_sigmoid.csv', index=False)

df_tanh = pd.DataFrame({'ID': range(len(y_test_pred_tanh)), 'label': y_test_pred_tanh})
df_tanh.to_csv('files/original_FC_tanh.csv', index=False)

df_relu_dropout = pd.DataFrame({'ID': range(len(y_test_pred_relu_dropout)), 'label': y_test_pred_relu_dropout})
df_relu_dropout.to_csv('files/original_FC_relu_dropout.csv', index=False)

df_sigmoid_dropout = pd.DataFrame({'ID': range(len(y_test_pred_sigmoid_dropout)), 'label': y_test_pred_sigmoid_dropout})
df_sigmoid_dropout.to_csv('files/original_FC_sigmoid_dropout.csv', index=False)

df_tanh_dropout = pd.DataFrame({'ID': range(len(y_test_pred_tanh_dropout)), 'label': y_test_pred_tanh_dropout})
df_tanh_dropout.to_csv('files/original_FC_tanh_dropout.csv', index=False)