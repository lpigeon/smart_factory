import serial.tools.list_ports
import time

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
if ser is None:
    print("Arduino Uno를 찾을 수 없습니다.")
else:
    print("Arduino Uno와 연결되었습니다.")

def send_lamp_red(on_off):
    if on_off:
        ser.write("LAMP_RED=ON\n".encode())
    else:
        ser.write("LAMP_RED=OFF\n".encode())

try:
    while True:
        send_lamp_red(True)
        time.sleep(1.0)

        send_lamp_red(False)
        time.sleep(1.0)

except KeyboardInterrupt:
    send_lamp_red(False)
    ser.close()