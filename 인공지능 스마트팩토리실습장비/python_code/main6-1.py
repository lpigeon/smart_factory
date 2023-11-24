import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk

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

send_catch_on_off(False)

def on_servo_1_button_click():
    angle = int(servo_1_scale.get())
    send_servo_1_angle(angle)

def on_servo_2_button_click():
    angle = int(servo_2_scale.get())
    send_servo_2_angle(angle)

def on_servo_3_button_click():
    angle = int(servo_3_scale.get())
    send_servo_3_angle(angle)

def on_pump_on_button_click():
    send_catch_on_off(True)

def on_pump_off_button_click():
    send_catch_on_off(False)


root = tk.Tk()
root.title("Servo Motor Control")

# 슬라이드 바와 버튼을 포함한 프레임 생성 및 배치
servo_1_frame = ttk.Frame(root)
servo_1_frame.pack(pady=10)

servo_1_scale = ttk.Scale(servo_1_frame, from_=60, to=130, length=200)
servo_1_scale.set(80)
servo_1_scale.pack(side=tk.LEFT)

servo_1_value = tk.StringVar()
servo_1_value_label = ttk.Label(servo_1_frame, textvariable=servo_1_value)
servo_1_value_label.pack(side=tk.LEFT, padx=10)

servo_1_button = ttk.Button(servo_1_frame, text="Servo 1(높이)", command=on_servo_1_button_click)
servo_1_button.pack(side=tk.LEFT, padx=10)

servo_2_frame = ttk.Frame(root)
servo_2_frame.pack(pady=10)

servo_2_scale = ttk.Scale(servo_2_frame, from_=0, to=180, length=200)
servo_2_scale.set(180)
servo_2_scale.pack(side=tk.LEFT)

servo_2_value = tk.StringVar()
servo_2_value_label = ttk.Label(servo_2_frame, textvariable=servo_2_value)
servo_2_value_label.pack(side=tk.LEFT, padx=10)

servo_2_button = ttk.Button(servo_2_frame, text="Servo 2(회전)", command=on_servo_2_button_click)
servo_2_button.pack(side=tk.LEFT, padx=10)

servo_3_frame = ttk.Frame(root)
servo_3_frame.pack(pady=10)

servo_3_scale = ttk.Scale(servo_3_frame, from_=30, to=120, length=200)
servo_3_scale.set(100)
servo_3_scale.pack(side=tk.LEFT)

servo_3_value = tk.StringVar()
servo_3_value_label = ttk.Label(servo_3_frame, textvariable=servo_3_value)
servo_3_value_label.pack(side=tk.LEFT, padx=10)

servo_3_button = ttk.Button(servo_3_frame, text="Servo 3(길이)", command=on_servo_3_button_click)
servo_3_button.pack(side=tk.LEFT, padx=10)

# PUMP ON 버튼을 포함한 프레임 생성 및 배치
pump_on_frame = ttk.Frame(root)
pump_on_frame.pack(pady=10)

pump_on_button = ttk.Button(pump_on_frame, text="PUMP ON", command=on_pump_on_button_click)
pump_on_button.pack(side=tk.LEFT, padx=10)

# PUMP OFF 버튼을 포함한 프레임 생성 및 배치
pump_off_frame = ttk.Frame(root)
pump_off_frame.pack(pady=10)

pump_off_button = ttk.Button(pump_off_frame, text="PUMP OFF", command=on_pump_off_button_click)
pump_off_button.pack(side=tk.LEFT, padx=10)

# 슬라이드 바 값의 변화를 표시하는 함수
def update_slider_values():
    servo_1_value.set(int(servo_1_scale.get()))
    servo_2_value.set(int(servo_2_scale.get()))
    servo_3_value.set(int(servo_3_scale.get()))
    root.after(100, update_slider_values)

update_slider_values()

# GUI 크기를 조정합니다.
root.geometry("400x250")

root.mainloop()