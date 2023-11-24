import serial.tools.list_ports
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

# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

def send_servo_1_angle(angle=80):
    if 60 <= angle <= 130:
        ser.write(f"SERVO_1={angle}\n".encode())
    else:
        print("60~130사이의 값을 입력하세요")

def send_servo_2_angle(angle=180):
    if 0 <= angle <= 180:
        ser.write(f"SERVO_2={angle}\n".encode())
    else:
        print("0~180사이의 값을 입력하세요")

def send_servo_3_angle(angle=100):
    if 30 <= angle <= 120:
        ser.write(f"SERVO_3={angle}\n".encode())
    else:
        print("30~120사이의 값을 입력하세요")

send_servo_1_angle()
send_servo_2_angle()
send_servo_3_angle()

try:
    while True:
        angle = int(input("서보1번의 각도를 입력하세요(60~130)"))
        send_servo_1_angle(angle)

        angle = int(input("서보2번의 각도를 입력하세요(0~180)"))
        send_servo_2_angle(angle)

        angle = int(input("서보3번의 각도를 입력하세요(30~120)"))
        send_servo_3_angle(angle)


except KeyboardInterrupt:
    send_servo_1_angle()
    time.sleep(1.0)
    send_servo_2_angle()
    time.sleep(1.0)
    send_servo_3_angle()
    time.sleep(1.0)
    ser.close()