import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.datasets import mnist

# Загрузка датасета MNIST (цифры 0-9)
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Нормализация данных
x_train, x_test = x_train / 255.0, x_test / 255.0

# Добавление размерности для свёрточной сети
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Создание модели CNN
model = keras.Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(10, activation='softmax')  # 10 классов для цифр 0-9
])

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Сохранение модели
model.save("digits_model.h5")

# Оценка точности
loss, acc = model.evaluate(x_test, y_test)
print(f"Точность модели: {acc * 100:.2f}%")