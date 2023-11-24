import cv2
from pyzbar import pyzbar
from datetime import datetime
import time
import serial.tools.list_ports
import threading

def detect_qr_code(frame):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 이미지에서 QR 코드를 검출
    qrcodes = pyzbar.decode(gray)

    # QR 코드 주위에 사각형 그리기
    for qr in qrcodes:
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # QR 코드의 데이터 출력
        qr_data = qr.data.decode("utf-8")
        #qr_type = qr.type
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if qrcodes:
        return frame,qr_data
    else:
        return frame,None

# 웹캠 열기
cap = cv2.VideoCapture(0)


# Arduino Uno를 찾아서 시리얼 포트에 연결합니다.
def connect_to_arduino_uno():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino Uno" in port.description:
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
qr_save = False
while True:
    # 투입쪽에 물건이 들어오면 컨베이어 동작
    if "PS_3=ON" in serial_receive_data:
        send_conveyor_speed(255)
        print(serial_receive_data)
    # 중앙센서 검출
    elif "PS_2=ON" in serial_receive_data:
        print(serial_receive_data)
        serial_receive_data = ""
        qr_save = True
    # 출구에서 물건이 나가면 컨베이어 멈춤
    elif "PS_1=OFF" in serial_receive_data:
        print(serial_receive_data)
        serial_receive_data = ""
        send_conveyor_speed(0)
    
    # 프레임 읽기
    ret, frame = cap.read()

    # QR 코드 검출
    frame,qr_data = detect_qr_code(frame)

    if qr_save and qr_data:
        qr_save = False
        if int(qr_data[2]) % 2 == 0 :
            print(qr_data,"값은 짝수 입니다.")
        else:
            print(qr_data,"값은 홀수 입니다.")

    # 화면에 출력
    cv2.imshow("QR Code Detection", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

send_conveyor_speed(0)
ser.close()
cap.release()
cv2.destroyAllWindows()