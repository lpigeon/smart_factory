import cv2
import time
import serial.tools.list_ports
import threading
from keras.models import load_model
import numpy as np


# 모델불러오기
np.set_printoptions(suppress=True)
model = load_model(r"./converted_keras/keras_model.h5", compile=False)
class_names = open(r"./converted_keras/labels.txt", "r", encoding="utf-8").readlines()

# 웹캠 열기
cap = cv2.VideoCapture(0)

# Arduino Uno를 찾아서 시리얼 포트에 연결합니다.
def connect_to_arduino_uno():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "IOUSBHostDevice" in port.description:
            try:
                ser = serial.Serial(port.device, baudrate=9600)
                return ser
            except serial.SerialException:
                pass
    return None

serial_receive_data = ""
# 시리얼통신 수신 쓰레드 함수
def serial_read_thread():
    global serial_receive_data
    while True:
        read_data = ser.readline().decode()
        serial_receive_data = read_data

#컨베이어벨트 제어
def send_conveyor_speed(speed):
    if 0 <= speed <=255:
        ser.write(f"CV_MOTOR={speed}\n".encode())
    else:
        print("0~255사이의 값을 입력하세요")

# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

# 쓰레드를 시작합니다.
t1 = threading.Thread(target=serial_read_thread)
t1.daemon = True
t1.start()


time.sleep(2.0)
print("start")
serial_receive_data = ""
image_detect_on_off = False
while True:
    # 투입쪽에 물건이 들어오면 컨베이어 동작
    if "PS_3=ON" in serial_receive_data:
        send_conveyor_speed(255)
        print(serial_receive_data)
    # 중앙센서 검출
    elif "PS_2=ON" in serial_receive_data:
        print(serial_receive_data)
        serial_receive_data = ""
        time.sleep(0.8)
        image_detect_on_off = True
    elif "PS_2=OFF" in serial_receive_data:
        print(serial_receive_data)
        serial_receive_data = ""
        image_detect_on_off = False
    # 출구에서 물건이 나가면 컨베이어 멈춤
    elif "PS_1=OFF" in serial_receive_data:
        print(serial_receive_data)
        serial_receive_data = ""
        send_conveyor_speed(0)
        
    # 프레임 읽기
    ret, frame = cap.read()

    # 화면에 출력
    cv2.imshow("image", frame)

    #이미지를 저장
    if image_detect_on_off:
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        cv2.imshow("detect image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

send_conveyor_speed(0)
ser.close()
cap.release()
cv2.destroyAllWindows()
