import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

############################################################
# Load CIFAR-10
############################################################
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# print(x_train.shape)

# CIFAR-10 클래스 이름
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# 샘플 이미지 시각화
idx = 8
# plt.imshow(x_train[idx])
# plt.title(f"Label: {y_train[idx][0]} ({class_names[y_train[idx][0]]})")
# plt.axis("off")
# plt.show()

# Normalize (CIFAR-10 통계값 사용)
mean = np.array([0.4914, 0.4822, 0.4465])
std  = np.array([0.2023, 0.1994, 0.2010])

x_train = (x_train.astype("float32") / 255.0 - mean) / std
x_test  = (x_test.astype("float32") / 255.0 - mean) / std

y_train = y_train.flatten()
y_test  = y_test.flatten()

############################################################
# Simple Fully Connected Network (FCN) Model
############################################################

flatten = keras.layers.Flatten()
print(flatten(x_train).shape)  # (50000, 3072)

fcn = keras.Sequential([
    keras.layers.Flatten(input_shape=(32, 32, 3)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10),
])

# Hyperparameters
batch_size = 64
learning_rate = 0.001
num_epochs = 100

fcn.compile(
    optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

fcn.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=num_epochs,
    validation_data=(x_test, y_test),
    callbacks=[early_stopping],
    verbose=1
)