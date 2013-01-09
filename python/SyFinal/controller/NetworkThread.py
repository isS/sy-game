#-*- coding:UTF-8 -*-
__author__ = 'icestar'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import socket
import time

class Network(QThread):

    out = pyqtSignal(str)

    def __init__(self,   addres, port, id = 0 ):
        super(QThread, self).__init__()
        self.working = True
        self.connected = False
        self.addres = addres
        self.port = port
        self.id = id

        self.buf = ""


    def initSocket(self, ip, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            self.out.emit("%s -> 连接成功...\n"%(self.id))
            self.connected = True
        except Exception as e:
            self.out.emit("%s -> 连接失败...%s\n"%(self.id, str(e)))
            self.working = False
            self.connected = False

    def close(self):
        self.working = False
        self.wait()
        self.out.emit("%s -> 关闭...\n"%self.id)

    def log(self, msg):
        self.out.emit("%s -> %s"%self.id, msg)

    def logLine(self, msg):
        self.out.emit("%s -> %s \n"%(self.id, msg))

    def decodeMsg(self, msg):
        self.logLine(msg)

    def encodeMsg(self, msg):
        return msg+'\n'

    def send(self, msg):
        if self.connected:
            msg = self.encodeMsg(msg)
            self.socket.send(msg.encode('utf-8'))
            self.logLine("发送数据 : " + msg)



    def run(self):

        self.initSocket(self.addres, self.port)

        while self.working:
            data = self.socket.recv(4096)
            data = data.decode('utf-8')
            self.buf += data

            while self.buf.count('\n') > 0:
                index = self.buf.index('\n')
                msg = self.buf[:index]
                self.decodeMsg(msg)
                self.buf = self.buf[index+len('\n') : ]


        self.connected = False
        self.socket.close()
        self.logLine("断开连接!")

