import numpy as np

def softmax(z):
    # z: (C,) 또는 (N,C)
    z = np.array(z, dtype=float)

    if z.ndim == 1:
        z = z - np.max(z)              # 안정화
        exp_z = np.exp(z)
        return exp_z / np.sum(exp_z)
    else:
        z = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def main():
    W = np.array([
        [ 1,  1],
        [-1, -1]
    ], dtype=float)

    b = np.array([0.5, -0.5], dtype=float)

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=float)

    # 1) scores = Wx + b
    scores = X @ W.T + b

    # 2) softmax 확률 p (여기서 exp 들어감)
    probs = softmax(scores)

    # 3) 예측 (scores로 해도 되고 probs로 해도 결과는 같음)
    y_hat = np.argmax(scores, axis=1)      # 또는 np.argmax(probs, axis=1)

    # (선택) one-hot 변환
    num_classes = W.shape[0]
    y_hat_onehot = np.eye(num_classes)[y_hat]

    print("W:\n", W)
    print("b:\n", b)
    print("\nX (x1, x2):\n", X)

    print("\n--- scores = W x + b ---")
    for i, x in enumerate(X):
        print(f"x={x} -> scores={scores[i]}")

    print("\n--- probs = softmax(scores) (exp 사용) ---")
    for i, x in enumerate(X):
        print(f"x={x} -> probs={probs[i]}")

    print("\n--- y_hat ---")
    for i, x in enumerate(X):
        print(f"x={x} -> y_hat={y_hat[i]} -> onehot={y_hat_onehot[i]}")

if __name__ == "__main__":
    main()