import keras
import numpy as np

model = keras.models.load_model('model.keras')

model.summary()

X = np.array([[0,0], [0,1], [1,0], [1,1]], dtype = np.float32)

p = model.predict(X, verbose = 0)

p_final = model.predict(X , verbose = 0)
y_hat = np.argmax(p_final, axis = 1)

W = model.layers[0].get_weights()[0]
b = model.layers[0].get_weights()[1]

print(f"\n 최종 W: \n{W.T}")
print(f"    최종 b: {b}")
print(f"\n 예측 확률 : \n{p_final}")
print(y_hat)