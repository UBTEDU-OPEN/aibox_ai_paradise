#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import time

HOST = '<broadcast>'
PORT = 9999
BUFSIZE = 1024

ADDR = (HOST, PORT)

class DeviceDiscovery:
    def __init__(self, updSocket):
        self.udp_socket = updSocket
        self.address = None
        self.sever_th = None
        self.device_list = []
        self.device_dist = {}
        self.alive_timer = threading.Timer(1, self.keepDeviceAlive)


udpCliSock = socket(AF_INET, SOCK_DGRAM)
udpCliSock.bind(('', 0))
udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    data = raw_input('please input cmd >')
    if not data:
        break
    udpCliSock.sendto(data, ADDR)
    time.sleep(2)
    udpCliSock.sendto(data, ADDR)
    time.sleep(3)
    udpCliSock.sendto(data, ADDR)
    time.sleep(1)

udpCliSock.close()