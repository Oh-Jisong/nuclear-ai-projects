import numpy as np

def main():
    # Given (from slide)
    W = np.array([
        [ 1,  1],
        [-1, -1]
    ], dtype=float)              # shape (2, 2)

    b = np.array([0.5, -0.5], dtype=float)  # shape (2,)

    # Given x1, x2 (표에 있는 4가지 조합 전부 계산)
    # (x1, x2) = (0,0), (0,1), (1,0), (1,1)
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=float)              # shape (4, 2)

    # f(x) = W x + b
    # X가 (N,2) 이므로: scores = X @ W.T + b  -> (N,2)
    scores = X @ W.T + b

    # y-hat = argmax(scores)
    y_hat = np.argmax(scores, axis=1)

    # (선택) one-hot 변환
    num_classes = W.shape[0]
    y_hat_onehot = np.eye(num_classes)[y_hat]

    print("W:\n", W)
    print("b:\n", b)
    print("\nX (x1, x2):\n", X)

    print("\n--- f(x) = W x + b (scores) ---")
    for i, x in enumerate(X):
        print(f"x={x} -> scores={scores[i]} -> y_hat={y_hat[i]} -> onehot={y_hat_onehot[i]}")

if __name__ == "__main__":
    main()