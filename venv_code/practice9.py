import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

############################################################
# 1) Load CIFAR-10
############################################################
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# CIFAR-10 클래스 이름
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

############################################################
# 2) Normalize (CIFAR-10 통계값 사용)
############################################################
mean = np.array([0.4914, 0.4822, 0.4465])
std  = np.array([0.2023, 0.1994, 0.2010])

x_train = (x_train.astype("float32") / 255.0 - mean) / std
x_test  = (x_test.astype("float32") / 255.0 - mean) / std

y_train = y_train.flatten()
y_test  = y_test.flatten()

############################################################
# 3) Hyperparameters
############################################################
batch_size = 64
learning_rate = 0.001
num_epochs = 100

############################################################
# 4) Early Stopping
############################################################
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

############################################################
# 5) FCN Model
############################################################
flatten = keras.layers.Flatten()
print(flatten(x_train).shape)  # (50000, 3072)

fcn = keras.Sequential([
    keras.layers.Flatten(input_shape=(32, 32, 3)),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10),
])

fcn.compile(
    optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

print("\n==== FCN Training ====")
fcn.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=num_epochs,
    validation_data=(x_test, y_test),
    callbacks=[early_stopping],
    verbose=1
)

############################################################
# 6) CNN Model
############################################################
cnn = keras.Sequential([
    keras.layers.Conv2D(32, 3, padding='same', activation='relu', input_shape=(32, 32, 3)),
    keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(2),
    keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
    keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(10),
])

cnn.compile(
    optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

print("\n==== CNN Training ====")
cnn.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=num_epochs,
    validation_data=(x_test, y_test),
    callbacks=[early_stopping],
    verbose=1
)