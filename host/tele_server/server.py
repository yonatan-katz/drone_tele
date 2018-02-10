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


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (BIND_IP, BIND_PORT)    
    sock.bind(server_address)
    
    while True:
        data, address = sock.recvfrom(4096)
        print("Got data len:{}".format(len(data)))
        
        
if __name__=="__main__":
    main()