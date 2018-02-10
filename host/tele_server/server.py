#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:24:22 2018

@author: yonic
"""

import socket
import sys
import serial
import threading
import copy

BIND_IP = "192.168.14.62"
BIND_PORT = 6060

STOP_EVENT = threading.Event()


Q_LOCK = threading.Lock()
QUATERNION = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]#height and Quaternion a,b,c,d

J_LOCK = threading.Lock()
JOYSTICK_STATE = [0.0,0.0,0.0,0.0] #gas vertical and horizontal, pos vertical and horizontal

def handle_udp_tele_message(data):
    teapotPacket  = []
    q = range(4)
    for j in xrange(15):
        teapotPacket.append(ord(data[j]))
    q[0] = ((teapotPacket[2] << 8) | teapotPacket[3]) / 16384.0
    q[1] = ((teapotPacket[4] << 8) | teapotPacket[5]) / 16384.0
    q[2] = ((teapotPacket[6] << 8) | teapotPacket[7]) / 16384.0
    q[3] = ((teapotPacket[8] << 8) | teapotPacket[9]) / 16384.0
    height = teapotPacket[10] * 5
    
    
    Q_LOCK.acquire()
    QUATERNION[0] = height
    for i in range(4):
        if (q[i] >= 2):
            q[i] = -4 + q[i]
        
        QUATERNION[i+1] = q[i]
    
    Q_LOCK.release()        


def udp_channel(bind_ip,bind_port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (bind_ip, bind_port)    
    sock.bind(server_address)
    
    while not STOP_EVENT.is_set():
        data, address = sock.recvfrom(4096)
        #print("Got data len:{}".format(len(data)),data.__class__)
        handle_udp_tele_message(data)
        

def handle_serial_message(data):
    J_LOCK.acquire()
    for i in xrange(len(data)):
        JOYSTICK_STATE[i] = data[i]
    J_LOCK.release()
        
        
def serial_channel(port):
    
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = None          #block read        
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False    #disable hardware (DSR/DTR) flow control


    try: 
        ser.open()
    except Exception, e:
            print "error open serial port: " + str(e)
            exit(1) 
    
    DOLLAR=36
    state = "start"
    D = []
    while not STOP_EVENT.is_set():        
        ch = ord(ser.read(1))        
        if ch==DOLLAR:
            state = "$"        
        elif ch==2 and state == "$":
            state="DATA"
            
        elif state=="DATA":
            D.append(ch*3)
            if len(D) == 4:
                handle_serial_message(D)
                D = []
                state = "start"    
        
        
        
if __name__=="__main__":    
    from time import sleep
    
    #serial_channel()
    serial_tele = threading.Thread(target=serial_channel, args=("/dev/ttyUSB0",))
    udp_tele = threading.Thread(target=udp_channel, args=(BIND_IP,BIND_PORT))
    
    serial_tele.setDaemon(True)
    serial_tele.start()
    
    udp_tele.setDaemon(True)
    udp_tele.start()
    
    j = []
    q = []
    try:
        while True:
            Q_LOCK.acquire()
            q = copy.copy(QUATERNION)
            Q_LOCK.release()
            
            J_LOCK.acquire()
            j = copy.copy(JOYSTICK_STATE)
            J_LOCK.release()
            sleep(0.02) #sleep 20 miliseconds
            
            print(QUATERNION)
            print(JOYSTICK_STATE)
    except:
        global STOP_EVENT
        print("Stop working threads!")
        STOP_EVENT.set()
        
        
    