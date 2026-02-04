import numpy as np
import tensorflow as tf

def main():
    # -----------------------------
    # 1) 데이터 (슬라이드 표 그대로)
    # -----------------------------
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=np.float32)

    Y = np.array([
        [1, 0],
        [0, 1],
        [0, 1],
        [0, 1]
    ], dtype=np.float32)

    X_tf = tf.constant(X, dtype=tf.float32)  # (4,2)
    Y_tf = tf.constant(Y, dtype=tf.float32)  # (4,2)

    # -----------------------------
    # 2) 파라미터 초기값 (사진 그대로)
    # -----------------------------
    w_tf = tf.Variable([[1, 1],
                        [-1, -1]], dtype=tf.float32)      # (2,2)
    b_tf = tf.Variable([0.5, -0.5], dtype=tf.float32)     # (2,)

    learning_rate = 0.1
    epochs = 4000

    # -----------------------------
    # 3) 학습 루프 (사진 코드 그대로)
    # -----------------------------
    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            tape.watch([w_tf, b_tf])

            # f = XW^T + b   (X:(N,2), W:(2,2) -> transpose_b=True로 W^T)
            f = tf.matmul(X_tf, w_tf, transpose_b=True) + b_tf  # (4,2)

            # p = softmax(f)
            p = tf.nn.softmax(f)  # (4,2)

            # mse = mean((p - Y)^2)
            mse = tf.reduce_mean((p - Y_tf) ** 2)

        grads = tape.gradient(mse, [w_tf, b_tf])
        w_tf.assign_sub(learning_rate * grads[0])
        b_tf.assign_sub(learning_rate * grads[1])

        if (epoch + 1) % 200 == 0:
            print(f"Epoch {epoch+1:4d} | MSE = {mse.numpy():.6f}")

    # -----------------------------
    # 4) 최종 결과 확인 (scores, prob, y_hat)
    # -----------------------------
    print("\n===== Training Done =====")
    print("W =\n", w_tf.numpy())
    print("b =\n", b_tf.numpy())

    f_final = tf.matmul(X_tf, w_tf, transpose_b=True) + b_tf
    p_final = tf.nn.softmax(f_final)
    y_hat = tf.argmax(p_final, axis=1)

    print("\n--- Final outputs ---")
    for i in range(X.shape[0]):
        print(
            f"x={X[i].astype(int)} | "
            f"f={f_final[i].numpy()} | "
            f"p={np.round(p_final[i].numpy(), 4)} | "
            f"y_true={Y[i].astype(int)} | "
            f"y_hat={int(y_hat[i].numpy())}"
        )

if __name__ == "__main__":
    main()