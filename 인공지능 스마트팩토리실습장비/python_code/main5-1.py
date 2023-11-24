import serial.tools.list_ports
import threading

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

try:
    while True:
        # 투입쪽에 물건이 들어오면 컨베이어 동작
        if "PS_3=ON" in serial_receive_data:
            send_conveyor_speed(255)
            print(serial_receive_data)
            serial_receive_data = ""

        # 출구쪽센서에 물건이 들어오면 컨베이어 멈춤
        elif "PS_1=ON" in serial_receive_data:
            send_conveyor_speed(0)
            print(serial_receive_data)
            serial_receive_data = ""

except KeyboardInterrupt:
    send_conveyor_speed(0)
    ser.close()