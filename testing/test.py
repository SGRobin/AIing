import time

import serial

s = serial.Serial("COM5", 9600, timeout=2, exclusive=True)
print(s.isOpen())
messege = "hello! {};\n"
try:
    base_angles = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
    s.write(bytearray(base_angles))

    time.sleep(0.03)
finally:
    s.close()
