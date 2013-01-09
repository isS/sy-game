#coding=utf-8
__author__ = 'icestar'

from twisted.internet.protocol import ClientCreator, Protocol

from twisted.internet import reactor


import config



class ClientProtocol(Protocol):
    def sendCommand(self, command):
        print "invio", command
        self.transport.write(command)

    def dataReceived(self, data):
        print "DATA", data




class Connection:

    def __init__(self):
        self.host = config.Host
        self.port = config.Port


    def init(self):
        self.conn = ClientCreator(reactor, ClientProtocol)
        self.defer = self.conn.connectTCP(self.host, self.port)
        self.defer.addCallback(callback)


def callback(b):
    b.sendCommand("xxx")


# 单例
# 初始化网络
conn = Connection()
