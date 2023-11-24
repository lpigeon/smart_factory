import serial.tools.list_ports
import threading
import time

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

# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

# 쓰레드를 시작합니다.
t1 = threading.Thread(target=serial_read_thread)
t1.daemon = True
t1.start()

number = 1
start_time = time.time()
try:
    while True:
        if serial_receive_data:
            print(serial_receive_data)
            serial_receive_data = ""
        
        # 1초에 한번씩 동작
        current_time = time.time()
        if current_time - start_time >= 1:
            start_time = current_time
            ser.write(f"VR_{number}=?\n".encode())
            number = number + 1
            if number > 3:
                number = 1
            
except KeyboardInterrupt:
    ser.close()