import serial
import time

# 시리얼 포트와 통신 속도를 설정합니다.
port = '/dev/cu.usbmodem1101'  # 시리얼 포트 번호에 따라 변경하세요.
baudrate = 9600  # 통신 속도에 따라 변경하세요.

# 시리얼 포트와 연결합니다.
ser = serial.Serial(port, baudrate)

try:
    while True:
        ser.write("LAMP_RED=ON\n".encode())
        ser.write("LAMP_YELLOW=OFF\n".encode())
        ser.write("LAMP_GREEN=OFF\n".encode())
        print("빨간색 LAMP 켜짐")
        time.sleep(1.0)

        ser.write("LAMP_RED=OFF\n".encode())
        ser.write("LAMP_YELLOW=ON\n".encode())
        ser.write("LAMP_GREEN=OFF\n".encode())
        print("노란색 LAMP 켜짐")
        time.sleep(1.0)

        ser.write("LAMP_RED=OFF\n".encode())
        ser.write("LAMP_YELLOW=OFF\n".encode())
        ser.write("LAMP_GREEN=ON\n".encode())
        print("녹색 LAMP 켜짐")
        time.sleep(1.0)

except KeyboardInterrupt:
    ser.write("LAMP_RED=OFF\n".encode())
    ser.write("LAMP_YELLOW=OFF\n".encode())
    ser.write("LAMP_GREEN=OFF\n".encode())
    # 시리얼 포트를 닫습니다.
    ser.close()