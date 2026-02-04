import numpy as np

# given
W = np.array([[ 1,  1],
              [-1, -1]])
b = np.array([ 0.5, -0.5])

# (X1, X2) from the table
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# f(x) = Wx + b  (각 샘플별로 점수 2개가 나옴)
F = X @ W.T + b          # shape: (4, 2)

# y_hat = argmax(f(x))
y_hat = np.argmax(F, axis=1)

print("X:\n", X)
print("\nf(x)=Wx+b:\n", F)
print("\ny_hat (argmax):\n", y_hat)