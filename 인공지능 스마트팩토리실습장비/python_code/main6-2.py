import serial.tools.list_ports
import time

# Arduino Uno를 찾아서 시리얼 포트에 연결합니다.
def connect_to_arduino_uno():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port)
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

def send_catch_on_off(on_off):
    if on_off:
        ser.write("CATCH=ON\n".encode())
    else:
        ser.write("CATCH=OFF\n".encode())


send_servo_1_angle(80)
send_servo_2_angle(180)
send_servo_3_angle(100)
send_catch_on_off(False)

try:
    while True:
        start = input("아무글자 숫자를 입력하면 시작합니다.")

        print("1.물건 잡음")
        send_servo_1_angle(130)
        send_servo_2_angle(180)
        send_servo_3_angle(95)
        time.sleep(1.0)
        send_catch_on_off(True)
        time.sleep(2.0)

        print("2.물건 올림")
        send_servo_1_angle(80)
        send_servo_2_angle(180)
        send_servo_3_angle(95)
        time.sleep(2.0)

        print("3.물건 이동")
        send_servo_1_angle(80)
        send_servo_2_angle(90)
        send_servo_3_angle(95)
        time.sleep(2.0)

        print("4.물건 내림")
        send_servo_1_angle(130)
        send_servo_2_angle(90)
        send_servo_3_angle(95)
        time.sleep(2.0)
        send_catch_on_off(False)
        time.sleep(2.0)

        print("5.원위치")
        send_servo_1_angle(80)
        send_servo_2_angle(180)
        send_servo_3_angle(100)
        time.sleep(2.0)
        

except KeyboardInterrupt:
    send_servo_1_angle(80)
    send_servo_2_angle(180)
    send_servo_3_angle(100)
    send_catch_on_off(False)
    ser.close()