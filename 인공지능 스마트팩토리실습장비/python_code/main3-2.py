import serial
import time

# 시리얼 포트와 통신 속도를 설정합니다.
port = '/dev/cu.usbmodem1301'  # 시리얼 포트 번호에 따라 변경하세요.
baudrate = 9600  # 통신 속도에 따라 변경하세요.

# 시리얼 포트와 연결합니다.
ser = serial.Serial(port, baudrate)

def send_lamp_red(on_off):
    if on_off:
        ser.write("LAMP_RED=ON\n".encode())
    else:
        ser.write("LAMP_RED=OFF\n".encode())

def send_lamp_yellow(on_off):
    if on_off:
        ser.write("LAMP_YELLOW=ON\n".encode())
    else:
        ser.write("LAMP_YELLOW=OFF\n".encode())

def send_lamp_green(on_off):
    if on_off:
        ser.write("LAMP_GREEN=ON\n".encode())
    else:
        ser.write("LAMP_GREEN=OFF\n".encode())

try:
    while True:
        send_lamp_red(True)
        send_lamp_yellow(False)
        send_lamp_green(False)
        print("빨간색 LAMP 켜짐")
        time.sleep(1.0)

        send_lamp_red(False)
        send_lamp_yellow(True)
        send_lamp_green(False)
        print("노란색 LAMP 켜짐")
        time.sleep(1.0)

        send_lamp_red(False)
        send_lamp_yellow(False)
        send_lamp_green(True)
        print("녹색 LAMP 켜짐")
        time.sleep(1.0)

except KeyboardInterrupt:
    send_lamp_red(False)
    send_lamp_yellow(False)
    send_lamp_green(False)
    # 시리얼 포트를 닫습니다.
    ser.close()