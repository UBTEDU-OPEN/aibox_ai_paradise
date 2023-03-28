from typing import Union

from PyQt5 import QtWidgets
from socket import *
import threading
import json
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

HOST = '<broadcast>'
PORT_DATA = 9998
PORT_START = 9999
PORT_SEND = 20001
PORT_RECV = 20002
BUFSIZE = 1024
ADDR_WIFI = (HOST, PORT_SEND)
ADDR_AIBOX = ('10.42.0.255', PORT_SEND) #aibox热点广播地址

ADDR_DATA = (HOST, PORT_DATA)
ADDR_DATA_AIBOX= ('10.42.0.255', PORT_DATA)

ADDR_START = (HOST, PORT_START)
ADDR_START_AIBOX = ('10.42.0.255', PORT_START)
#连接超时设置为20s-
DEVICE_ALIVE_TIME = 20
#设备在线检测间隔1s
DEVICE_ALIVE_INTERVAL = 1
#广播包发送间隔1s
BRACASTER_INTERVAL = 3000


class DeviceDiscovery(QtCore.QObject):
    signal_write_msg = QtCore.pyqtSignal(object)

    def __init__(self, updSocket):
        super().__init__()
        self.udp_socket = updSocket
        self.address = None
        self.sever_th = None
        self.device_dist = {}
        self.timer_brocast = QTimer()
        self.timer_brocast.timeout.connect(self.udp_send_brocast)
        # self.alive_timer.start(DEVICE_ALIVE_INTERVAL)
        self.run_concurrency = True

    def udp_server_start(self):
        """
        开启UDP服务端方法
        :return:
        """
        self.sever_th = threading.Thread(target=self.udp_server_concurrency)
        self.sever_th.start()
        self.udp_client_start()
        print(f'listening {PORT_RECV}')

    def udp_server_concurrency(self):
        print('udp_server_concurrency start')
        while self.run_concurrency:
            #每1s查询所有设备生命周期
            time.sleep(DEVICE_ALIVE_INTERVAL)
            for key, value in list(self.device_dist.items()):
                self.device_dist[key] = value - DEVICE_ALIVE_INTERVAL
                if value - DEVICE_ALIVE_INTERVAL <= 0:
                    self.device_dist.pop(key)

            self.signal_write_msg.emit(self.device_dist)
            #发送到上层
            # print(f'device_dist:{self.device_dist}')
            try:
                # print('udp_server_concurrency while enter')
                recv_msg, recv_addr = self.udp_socket.recvfrom(1024)
                # print('udp_server_concurrency while get data')
                msg = recv_msg.decode()
                msg_dist = json.loads(msg)
                # print(f'msg:{msg}')
                devicefound = msg_dist["name"]
                # print(f'devicefound:{devicefound}')
                self.device_dist[devicefound] = DEVICE_ALIVE_TIME
            except (BlockingIOError, ConnectionResetError, UnicodeDecodeError):
                pass
        print('udp_server_concurrency end')


    def udp_client_start(self):
        self.timer_brocast.start(BRACASTER_INTERVAL)
    def udp_send_brocast(self):
        # print('udp_send begin')
        datajson = {
            'cmd': 'discovery',
            'port': PORT_RECV
        }
        # print('datajson:', datajson)
        datastr = json.dumps(datajson)
        # print('datastr:', datastr)
        self.udp_send_data(datastr, ADDR_WIFI)
        self.udp_send_data(datastr, ADDR_AIBOX)
        # print('udp_send end')

    def udp_send_posture_data(self, data):
        # print('udp_send_data:', data)
        self.udp_send_data(data, ADDR_DATA)
        self.udp_send_data(data, ADDR_DATA_AIBOX)


    def udp_send_start(self, data):
        print('udp_send_start:', data)
        self.udp_send_data(data, ADDR_START)
        self.udp_send_data(data, ADDR_START_AIBOX)


    def udp_send_data(self, data, address):
        try:
            self.udp_socket.sendto(data.encode(), address)
        except (BlockingIOError, ConnectionResetError, UnicodeDecodeError, OSError):
            pass

    def udp_close(self):
        print('udp_close begin')
        self.run_concurrency = False
        if self.sever_th.isAlive():
            self.sever_th.join()
        if self.timer_brocast.isActive():
            self.timer_brocast.stop()
        self.udp_socket.close()
        print('udp_close begin')

        # if self.alive_timer is not None:
        #     self.alive_timer.cancel()


def StartdiscoveryDevice(callback):
    udpCliSock = socket(AF_INET, SOCK_DGRAM)
    udpCliSock.setblocking(False)  # 将socket设置为非阻塞. 在创建socket对象后就进行该操作.
    udpCliSock.bind(('', PORT_RECV))
    udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    discovery = DeviceDiscovery(udpCliSock)
    discovery.signal_write_msg.connect(callback)
    discovery.udp_server_start()
    return discovery




