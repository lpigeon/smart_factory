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

def send_catch_on_off(on_off):
    if on_off:
        ser.write("CATCH=ON\n".encode())
    else:
        ser.write("CATCH=OFF\n".encode())

send_catch_on_off(False)

try:
    while True:
        catch_on_off = int(input("1(물건잡음) 또는 0(물건놓음) 을 입력하세요:"))
        send_catch_on_off(catch_on_off)


except KeyboardInterrupt:
    send_catch_on_off(False)
    ser.close()