#!/usr/bin/env python3 


import serial
import time 

arduino = serial.Serial("/dev/ttyUSB0", 
baudrate=115200,
timeout=5, 
bytesize=serial.EIGHTBITS, 
parity=serial.PARITY_NONE, 
stopbits=serial.STOPBITS_ONE, 
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2)

n = 0

while True:
    try:
        cmd = str(n) + "|"
        if n == 0:
            arduino.write(cmd.encode())
            n = 1
            time.sleep(5)
        elif n == 1:
            arduino.write(cmd.encode())
            n = 0
            time.sleep(5)
    except Exception as e:
        print(e)
        arduino.close() 
