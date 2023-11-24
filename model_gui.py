import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import csv
from collections import Counter
import matplotlib.pyplot as plt
from keras.models import load_model
import time
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # GUI 초기화
        self.initUI()

        # OpenCV 카메라 초기화
        self.cap = cv2.VideoCapture(0)  # 0은 기본 카메라

        # 딥러닝 모델 및 레이블 로드
        self.model = load_model("./model/keras_model.h5", compile=False)
        self.class_names = open("./model/labels.txt", "r").readlines()

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 업데이트

        # 변수 초기화
        self.start_time = time.time()
        self.detect_list = []

    def initUI(self):
        # 레이아웃 설정
        layout = QHBoxLayout(self)
        image_layout = QVBoxLayout()
        data_layout = QVBoxLayout()
        graph_layout = QVBoxLayout()

        # QLabel 초기화
        self.video_label = QLabel(self)
        image_layout.addWidget(self.video_label)

        self.image_label = QLabel(self)
        image_layout.addWidget(self.image_label)

        # CSV 파일에서 데이터 읽어오기
        data = self.read_csv('./most_common_values.csv')
        data_text = "\n".join([f"{key}: {value}" for key, value in data.items()])
        self.data_label = QLabel(data_text, self)
        data_layout.addWidget(self.data_label)

        # 맷플롯립을 사용하여 원형 그래프 생성
        self.graph_label = QLabel(self)
        self.create_pie_chart(data)
        graph_layout.addWidget(self.graph_label)

        # 레이아웃에 추가
        layout.addLayout(image_layout, 4)
        layout.addLayout(data_layout, 1)
        layout.addLayout(graph_layout, 1)

        self.setWindowTitle('OpenCV and PyQt Example')
        self.setGeometry(100, 100, 800, 600)

    def update_frame(self):
        # OpenCV 비디오 업데이트
        ret, frame = self.cap.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img.rgbSwapped())
            self.video_label.setPixmap(pixmap)

        # 딥러닝 모델 예측
        image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        print("Class:", class_name[2:], end="")

        # 데이터 리스트에 클래스 추가
        self.detect_list.append(class_name[2:])

        if time.time() - self.start_time >= 3:
            most_common_value = max(self.detect_list, key=self.detect_list.count)
            self.save_to_csv(most_common_value)
            self.detect_list = []
            self.start_time = time.time()

        # GUI 업데이트
        self.update_image()
        self.update_data_label()

    def read_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Header skip
            data = Counter(row[0].strip() for row in reader)
        return data

    def create_pie_chart(self, data):
        fig, ax = plt.subplots()
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image)
        self.graph_label.setPixmap(pixmap)

    def update_image(self):
        most_common_value = max(self.detect_list, key=self.detect_list.count)
        print(most_common_value)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, "img", f"{most_common_value}.png")
        image = cv2.imread(image_path)
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img.rgbSwapped())
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.clear()

    def update_data_label(self):
        data = self.read_csv('./most_common_values.csv')
        data_text = "\n".join([f"{key}: {value}" for key, value in data.items()])
        self.data_label.setText(data_text)

    def save_to_csv(self, most_common_value):
        with open('./most_common_values.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Class", "Timestamp"])  # Header
            csv_writer.writerow([most_common_value, time.strftime("%Y-%m-%d %H:%M:%S")])
            print("Saved to CSV file")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
