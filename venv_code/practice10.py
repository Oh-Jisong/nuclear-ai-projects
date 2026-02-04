import keras
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock

df = stock.get_index_ohlcv("20000101", "20260203", "1001")  # 1001 = KOSPI
data = df["종가"].values.astype(float)

print("Data length:", len(data))

# KOSPI 종가 시각화
plt.figure(figsize=(12, 4))
plt.plot(df.index, data)
plt.title("KOSPI (2000 ~ 2026)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.show()

# Log transform
data = np.log(data)

# Normalize
mean, std = np.mean(data), np.std(data)
data = (data - mean) / std