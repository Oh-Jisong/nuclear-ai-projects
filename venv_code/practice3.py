import numpy as np

def softmax(z: np.ndarray) -> np.ndarray:
    z = z - np.max(z)              # overflow 방지
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z)

def mse_per_sample(p: np.ndarray, y: np.ndarray) -> float:
    # 슬라이드 지시: "Square each element and sum them up to get a single value."
    return float(np.sum((p - y) ** 2))

def run(W: np.ndarray, b: np.ndarray, X: np.ndarray, Y: np.ndarray, name: str):
    print(f"\n===== {name} =====")
    losses = []

    for i, x in enumerate(X):
        scores = W @ x + b
        p = softmax(scores)
        loss = mse_per_sample(p, Y[i])
        losses.append(loss)

        print(f"x={x.astype(int)}  f(x)={scores}  p={np.round(p, 4)}  y={Y[i].astype(int)}  mse={loss:.6f}")

    losses = np.array(losses)
    print(f"per-sample mse: {np.round(losses, 6)}")
    print(f"mean mse: {losses.mean():.6f}")
    print(f"sum  mse: {losses.sum():.6f}")

def main():
    # 입력 4개 (Practice 1-1/1-2 그대로)
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=float)

    # 정답 one-hot (슬라이드 표 그대로)
    Y = np.array([
        [1, 0],
        [0, 1],
        [0, 1],
        [0, 1]
    ], dtype=float)

    # b는 Practice 1-1에서 쓰던 값(슬라이드에 있던 그 값)
    b = np.array([0.5, -0.5], dtype=float)

    # W 3가지 비교 (슬라이드 아래 줄)
    W1  = np.array([[ 1, 1],
                    [-1,-1]], dtype=float)

    Wp  = np.array([[ 1, 1],
                    [-1,-0.9]], dtype=float)

    Wpp = np.array([[ 1, 1],
                    [-1,-1.1]], dtype=float)

    run(W1,  b, X, Y, "W")
    run(Wp,  b, X, Y, "W'")
    run(Wpp, b, X, Y, "W''")

if __name__ == "__main__":
    main()
