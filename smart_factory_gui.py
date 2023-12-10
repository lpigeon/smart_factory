import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
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
        
        # 상태 변수 초기화
        self.normal_door_count = 0
        self.normal_bumper_count = 0
        self.normal_glass_count = 0
        self.broken_door_count = 0
        self.broken_bumper_count = 0
        self.broken_glass_count = 0
        
        # CSV 파일에서 데이터 읽어오기
        self.data = self.read_csv('./most_common_values.csv')
        self.data_text = "\n".join([f"{key}: {value}" for key, value in self.data.items()])
        
        self.datas = {
            'Normal Door': self.normal_door_count,
            'Normal Bumper': self.normal_bumper_count,
            'Normal Glass': self.normal_glass_count,
            'Broken Door': self.broken_door_count,
            'Broken Bumper': self.broken_bumper_count,
            'Broken Glass': self.broken_glass_count,
        }
        
        # GUI 초기화
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        main_layout = QVBoxLayout(self)
        
        # 제목 레이아웃
        title_layout = QHBoxLayout()
        
        # 제목 레이블 추가
        title_label = QLabel("Smart Factory GUI", self)
        font = title_label.font()
        font.setPointSize(font.pointSize() + 5)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        # 상단 레이아웃
        top_layout = QHBoxLayout()

        # 각 레이아웃에 프레임 추가
        video_layout_frame = QFrame(self)
        video_layout_frame.setFrameShape(QFrame.Box)
        video_layout = QVBoxLayout(video_layout_frame)

        data_layout_frame = QFrame(self)
        data_layout_frame.setFrameShape(QFrame.Box)
        data_layout = QVBoxLayout(data_layout_frame)

        graph_layout_frame = QFrame(self)
        graph_layout_frame.setFrameShape(QFrame.Box)
        graph_layout = QVBoxLayout(graph_layout_frame)

        # 첫 번째 레이아웃에 이미지 추가
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        video_layout.addWidget(self.video_label)

        # 두 번째 레이아웃에 데이터 추가

        self.status_label = QLabel("Status : Normal", self)
        font = self.status_label.font()
        font.setPointSize(font.pointSize() + 10)
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("background-color: green")
        data_layout.addWidget(self.status_label)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        data_layout.addWidget(self.image_label)
        
        # 세 번째 레이아웃에 그래프 추가
        self.graph_label = QLabel(self)
        self.graph_label.setAlignment(Qt.AlignCenter)
        self.create_pie_chart(self.datas)
        graph_layout.addWidget(self.graph_label)

        # 상단 레이아웃에 추가
        top_layout.addWidget(video_layout_frame, 1)
        top_layout.addWidget(data_layout_frame, 4)
        top_layout.addWidget(graph_layout_frame, 1)

        # 하단 레이아웃
        bottom_layout = QVBoxLayout()

        # 네 번째 레이아웃 (하나의 창)
        button_layout_frame = QFrame(self)
        button_layout_frame.setFrameShape(QFrame.Box)
        button_layout = QHBoxLayout(button_layout_frame)

        button_normalization = QPushButton("Normalization", self)
        button_stop = QPushButton("Stop", self)
        button_layout.addWidget(button_stop)
        button_layout.addWidget(button_normalization)

        
        # Connect button signals to functions
        button_normalization.clicked.connect(lambda: self.save_button_value(1))
        button_stop.clicked.connect(lambda: self.save_button_value(0))

        # 하단 레이아웃에 추가
        bottom_layout.addWidget(button_layout_frame)

        # 전체 레이아웃에 상단과 하단 레이아웃 추가
        main_layout.addLayout(title_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setFixedSize(1200, 600)
        self.setWindowTitle('Smart Factory GUI')

    def update_frame(self):
        # OpenCV 비디오 업데이트
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
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
        self.detect_list.append(class_name[2:].strip())

        if time.time() - self.start_time >= 3:
            most_common_value = max(self.detect_list, key=self.detect_list.count)
            
            # 상태별로 카운트 증가
            if most_common_value == "normal_door":
                self.normal_door_count += 1
            elif most_common_value == "normal_bumper":
                self.normal_bumper_count += 1
            elif most_common_value == "normal_glass":
                self.normal_glass_count += 1
            elif most_common_value == "broken_door":
                self.broken_door_count += 1
            elif most_common_value == "broken_bumper":
                self.broken_bumper_count += 1
            elif most_common_value == "broken_glass":
                self.broken_glass_count += 1
                
            self.save_to_csv(most_common_value)
            self.detect_list = []
            self.start_time = time.time()

        # GUI 업데이트
        self.update_image()
        self.update_pie_chart()

    def save_button_value(self, value):
            with open('./button_value.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([value])
                
    def save_to_csv(self, most_common_value):
        if most_common_value != "background":
            with open('./most_common_values.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Class", "Timestamp"])  # Header
                csv_writer.writerow([most_common_value, time.strftime("%Y-%m-%d %H:%M:%S")])
                
    def read_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Header skip
            data = Counter(row[0].strip() for row in reader)
        return data

    def create_pie_chart(self, data):
        # 0 값이 있는 항목을 제외하기 위해 딕셔너리 수정
        data = {key: value for key, value in data.items() if value != 0}

        if not data:
            # 모든 값이 0이면 하나의 세그먼트로 구성된 더미 차트를 생성
            data = {'데이터 없음': 1}

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
        if not self.detect_list:
            # self.detect_list가 비어 있으면 처리하지 않음
            return
        most_common_value = max(self.detect_list, key=self.detect_list.count)

        # 이미지를 불러옴
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, "img", f"{most_common_value}.png")
        image = cv2.imread(image_path)
        if image is not None:
            # 이미지를 QLabel의 크기에 맞게 조절
            image = cv2.resize(image, (self.image_label.width(), self.image_label.height()))
            bytes_per_line = 3 * image.shape[1]
            q_img = QImage(image.data, image.shape[1], image.shape[0], bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img.rgbSwapped())
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Image not detected")
        
        if most_common_value == "background":
            self.status_label.setText("Status: -")
            self.status_label.setStyleSheet("background-color: grey")
        elif most_common_value == "normal_bumper" or most_common_value == "normal_door" or most_common_value == "normal_glass":
            self.status_label.setText("Status: Normal")
            self.status_label.setStyleSheet("background-color: green")
        else:
            self.status_label.setText("Status: Abnormal")
            self.status_label.setStyleSheet("background-color: red")

    def update_pie_chart(self):
        datas = {
            'Normal Door': self.normal_door_count,
            'Normal Bumper': self.normal_bumper_count,
            'Normal Glass': self.normal_glass_count,
            'Broken Door': self.broken_door_count,
            'Broken Bumper': self.broken_bumper_count,
            'Broken Glass': self.broken_glass_count,
        }
        self.create_pie_chart(datas)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())