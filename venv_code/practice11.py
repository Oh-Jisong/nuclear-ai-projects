import keras
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock

############################################################
# 1) Load KOSPI data
############################################################
df = stock.get_index_ohlcv("20000101", "20260203", "1001")  # 1001 = KOSPI
data = df["종가"].values.astype(float)

print("Data length:", len(data))

"""
# KOSPI 종가 시각화
plt.figure(figsize=(12, 4))
plt.plot(df.index, data)
plt.title("KOSPI (2000 ~ 2026)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.show()
"""

############################################################
# 2) Preprocess (log + normalize)
############################################################
data = np.log(data)

mean, std = np.mean(data), np.std(data)
data = (data - mean) / std

############################################################
# 3) Create sequences (faster version)
############################################################
seq_length = 120

def create_sequences(dataset, seq_len):
    n = len(dataset) - seq_len
    xs = np.empty((n, seq_len), dtype=np.float32)
    ys = np.empty((n,), dtype=np.float32)

    for i in range(n):
        xs[i] = dataset[i:i + seq_len]
        ys[i] = dataset[i + seq_len]

    return xs, ys

X, y = create_sequences(data, seq_length)

############################################################
# 4) Train-test split
############################################################
train_ratio = 0.8
train_size = int(train_ratio * len(X))

X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size:], y[train_size:]

print("Train set size:", X_train.shape, y_train.shape)
print("Test set size:", X_test.shape, y_test.shape)

############################################################
# 5) GRU Model
############################################################
print("\nTraining GRU...")

# GRU 입력: (samples, timesteps, features) -> reshape 필요
X_train_gru = X_train.reshape(-1, seq_length, 1)
X_test_gru = X_test.reshape(-1, seq_length, 1)

gru = keras.Sequential([
    keras.layers.Input(shape=(seq_length, 1)),
    keras.layers.GRU(64, return_sequences=True),
    keras.layers.GRU(64),
    keras.layers.Dense(1),
])

gru.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss='mse'
)

gru.fit(X_train_gru, y_train, epochs= 10, batch_size=64, verbose =2)

'''
############################################################
# 6) Visualization
############################################################

# Test set prediction
y_pred = gru.predict(X_test_gru)

# Flatten (shape 맞추기)
y_test_plot = y_test.flatten()
y_pred_plot = y_pred.flatten()

# Plot
plt.figure(figsize=(12, 5))
plt.plot(y_test_plot, label="True")
plt.plot(y_pred_plot, label="Prediction")
plt.title("GRU Prediction vs True (Normalized Log Price)")
plt.xlabel("Time step")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.show()
'''

gru.save('model.keras')