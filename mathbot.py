import sys
import cv2
import numpy as np
import tensorflow as tf
import sympy as sp
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

# Загрузка предобученной модели
model = tf.keras.models.load_model("digits_model.h5")

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    return cv2.resize(thresh, (28, 28)).reshape(1, 28, 28, 1) / 255.0

def recognize_expression(image):
    # Разбиваем изображение на отдельные символы (упрощенно)
    # В продакшене нужно использовать сегментацию
    processed = preprocess_image(image)
    predictions = model.predict(processed)
    recognized_text = str(np.argmax(predictions))  # Получаем распознанный символ
    return recognized_text

def calculate_expression(expression):
    try:
        return str(sp.simplify(expression))
    except Exception:
        return "Ошибка"

class HandwrittenCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handwritten Calculator")
        self.setGeometry(100, 100, 400, 500)
        
        self.canvas = QPixmap(300, 300)
        self.canvas.fill(Qt.GlobalColor.white)
        
        self.label = QLabel()
        self.label.setPixmap(self.canvas)
        
        self.result_label = QLabel("Результат: ")
        
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_canvas)
        
        self.recognize_button = QPushButton("Рассчитать")
        self.recognize_button.clicked.connect(self.process_image)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.recognize_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.last_point = QPoint()
        self.drawing = False
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas)
            pen = QPen(Qt.GlobalColor.black, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.label.setPixmap(self.canvas)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
    
    def clear_canvas(self):
        self.canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(self.canvas)
        self.result_label.setText("Результат: ")
    
    def process_image(self):
        image = self.canvas.toImage()
        buffer = image.bits().asstring(image.sizeInBytes())

        img_array = np.frombuffer(buffer, dtype=np.uint8).reshape((300, 300, 4))
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
        
        expression = recognize_expression(img_array)
        result = calculate_expression(expression)
        self.result_label.setText(f"Результат: {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandwrittenCalculator()
    window.show()
    sys.exit(app.exec())