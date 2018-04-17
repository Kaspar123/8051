# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:51:45 2018

@author: kaspar
"""

import serial, time

SERIALPORT = '/dev/ttyUSB0'
BAUDRATE = 19200

DATA1 = '\x2f\x30\x30\x49\x44\x45\x44\x0d'
DATA2 = '\x2f\x30\x30\x43\x43\x45\x32\x42\x0d' 

ser = serial.Serial(SERIALPORT, BAUDRATE)
ser.timeout = 2

if ser.isOpen():
    ser.write(DATA1)
    ser.write(DATA1)
    ser.write(DATA2)
    
    while True:
        response = ser.readline()
        print(response)
        print('')
        