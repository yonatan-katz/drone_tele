#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:24:22 2018

@author: yonic
"""

import socket
import sys

BIND_IP = "192.168.14.62"
BIND_PORT = 6060

def handle_tele_message(data):
    teapotPacket  = []
    q = range(4)
    for j in xrange(15):
        teapotPacket.append(ord(data[j]))
    q[0] = ((teapotPacket[2] << 8) | teapotPacket[3]) / 16384.0
    q[1] = ((teapotPacket[4] << 8) | teapotPacket[5]) / 16384.0
    q[2] = ((teapotPacket[6] << 8) | teapotPacket[7]) / 16384.0
    q[3] = ((teapotPacket[8] << 8) | teapotPacket[9]) / 16384.0
    height = teapotPacket[10] * 5
    for i in range(4):
        if (q[i] >= 2):
            q[i] = -4 + q[i]

    print("Height:{}".format(height))
    print("q[0]:{}".format(q[0]))
    print("q[1]:{}".format(q[1]))
    print("q[2]:{}".format(q[2]))
    print("q[3]:{}".format(q[3]))
    
    

        
    
   


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (BIND_IP, BIND_PORT)    
    sock.bind(server_address)
    
    while True:
        data, address = sock.recvfrom(4096)
        print("Got data len:{}".format(len(data)),data.__class__)
        handle_tele_message(data)
        
        
        
        
if __name__=="__main__":
    main()
    