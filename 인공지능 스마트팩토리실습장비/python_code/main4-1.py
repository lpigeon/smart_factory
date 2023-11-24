import serial.tools.list_ports

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

try:
    while True:
        data = ser.readline().decode() # 시리얼 통신으로 데이터를 읽고 문자열로 변환합니다.
        print(data)
except KeyboardInterrupt:
    ser.close()