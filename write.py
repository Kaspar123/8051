import serial
import time

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

running = True

while running:
    ser.write('OOID'.encode())
    time.sleep(0.1)
    msg = [ser.read() for _ in range(ser.inWaiting())]