import serial.tools.list_ports
import time

# Arduino Uno를 찾아서 시리얼 포트에 연결합니다.
def connect_to_arduino_uno():
    ports = serial.tools.list_ports.comports()
    print(ports)
    for port in ports:
        print(port.description)
        if "IOUSBHostDevice" in port.description:
            try:
                ser = serial.Serial(port.device, baudrate=9600)
                return ser
            except serial.SerialException:
                pass
    return None

# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

def send_conveyor_speed(speed):
    if 0 <= speed <=255:
        ser.write(f"CV_MOTOR={speed}\n".encode())
    else:
        print("0~255사이의 값을 입력하세요")

try:
    while True:
        send_conveyor_speed(0)
        print("속도: 0")
        time.sleep(3.0)

        send_conveyor_speed(150)
        print("속도: 150")
        time.sleep(3.0)

        send_conveyor_speed(255)
        print("속도: 255")
        time.sleep(3.0)

except KeyboardInterrupt:
    send_conveyor_speed(0)
    ser.close()