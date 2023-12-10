import cv2
import time
import serial.tools.list_ports
import threading
from keras.models import load_model
import numpy as np
import csv
from collections import Counter

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
        
def read_csv(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        row = next(csv_reader)
        most_common_value = row["Class"]
    return most_common_value

def read_button_value(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row = next(csv_reader)
        button_value = int(row[0])
    return button_value

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


def move_robot_arm(servo_1_angle, servo_2_angle, servo_3_angle):
    time.sleep(1)
    send_conveyor_speed(0)
    print("물건이동시작")

    print("1.물건 잡음")
    send_servo_1_angle(127)
    send_servo_2_angle(180)
    send_servo_3_angle(107)
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
    send_servo_2_angle(servo_2_angle)
    send_servo_3_angle(95)
    time.sleep(2.0)

    print("4.물건 내림")
    send_servo_1_angle(servo_1_angle)
    send_servo_2_angle(servo_2_angle)
    send_servo_3_angle(servo_3_angle)
    time.sleep(2.0)
    send_catch_on_off(False)
    time.sleep(2.0)

    print("5.원위치")
    send_servo_1_angle(80)
    send_servo_2_angle(180)
    send_servo_3_angle(100)
    time.sleep(2.0)
        
# Arduino Uno와 연결합니다.
ser = connect_to_arduino_uno()

most_common_value_file = "most_common_values.csv"
most_common_value = ""

send_servo_1_angle(80)
send_servo_2_angle(180)
send_servo_3_angle(100)
send_catch_on_off(False)

button_value = 1

# 쓰레드를 시작합니다.
t1 = threading.Thread(target=serial_read_thread)
t1.daemon = True
t1.start()

time.sleep(2.0)
print("start")
serial_receive_data = ""
image_detect_on_off = False

send_lamp_green(True)
send_lamp_yellow(False)
send_lamp_red(False)
                
while True:
    if button_value == 1:
        button_value = read_button_value("button_value.csv")
        # 투입쪽에 물건이 들어오면 컨베이어 동작
        if "PS_3=ON" in serial_receive_data:
            send_lamp_green(True)
            send_lamp_yellow(False)
            send_lamp_red(False)
            send_conveyor_speed(255)
            print(serial_receive_data)
        # 중앙센서 검출
        elif "PS_2=ON" in serial_receive_data:
            send_conveyor_speed(0)
            time.sleep(2)
            print(serial_receive_data)
            serial_receive_data = ""
            image_detect_on_off = True
            send_conveyor_speed(255)
        elif "PS_2=OFF" in serial_receive_data:
            print(serial_receive_data)
            serial_receive_data = ""
            image_detect_on_off = False
        # 출구에서 물건이 들어오면
        elif "PS_1=ON" in serial_receive_data:
            print(serial_receive_data)
            serial_receive_data = ""
            
            for _ in range(10):
                most_common_value = read_csv(most_common_value_file)
            print("검출된 객체는:",most_common_value)
            
            if "normal_door" in most_common_value or "normal_bumper" in most_common_value or "normal_glass" in most_common_value:
                send_lamp_green(True)
                send_lamp_yellow(False)
                send_lamp_red(False)
                move_robot_arm(130, 50, 95)
            elif "broken_door" in most_common_value:
                send_lamp_green(False)
                send_lamp_yellow(True)
                send_lamp_red(False)
                move_robot_arm(130, 80, 95)
            elif "broken_bumper" in most_common_value:
                send_lamp_green(False)
                send_lamp_yellow(True)
                send_lamp_red(False)
                move_robot_arm(130, 110, 95)
            elif "broken_glass" in most_common_value:
                send_lamp_green(False)
                send_lamp_yellow(True)
                send_lamp_red(False)
                move_robot_arm(130, 135, 84)
            else:
                print("알수없는 물건입니다.")
                send_conveyor_speed(0)
            
        # 출구에서 물건이 나가면 컨베이어 멈춤
        elif "PS_1=OFF" in serial_receive_data:
            print(serial_receive_data)
            serial_receive_data = ""
            send_conveyor_speed(0)
    elif button_value == 0:
        send_lamp_green(False)
        send_lamp_yellow(False)
        send_lamp_red(True)
        send_conveyor_speed(0)
        
        