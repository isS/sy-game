#-*- coding:UTF-8 -*-
__author__ = 'icestar'


from PyQt4.QtGui import *

from controller.NetworkThread import Network

class NetworkTestWidget(QDialog):

    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        self.resize(600, 400)


        baseLayout = QVBoxLayout(self)

        layout0 = QHBoxLayout(self)
        self.addrLable = QLabel("地址:", self)
        self.numLable = QLabel("个数:", self)
        self.addrEdit = QLineEdit(self)
        self.numEdit = QLineEdit(self)
        self.numEdit.setMaximumSize(40, 25)
        self.connButton = QPushButton("连接服务", self)
        self.closeButton = QPushButton("关闭连接", self)
        layout0.addWidget(self.addrLable)
        layout0.addWidget(self.addrEdit)
        layout0.addWidget(self.numLable)
        layout0.addWidget(self.numEdit)
        layout0.addWidget(self.connButton)
        layout0.addWidget(self.closeButton)

        baseLayout.addLayout(layout0)

        self.log = QTextEdit(self)
        baseLayout.addWidget(self.log)

        layout1 = QHBoxLayout(self)
        self.sendButton = QPushButton("发送",self)
        self.inputEdit = QLineEdit(self)
        layout1.addWidget(self.inputEdit)
        layout1.addWidget(self.sendButton)
        baseLayout.addLayout(layout1)

        self.setLayout(baseLayout)

        self.connButton.clicked.connect(self.connect)
        self.closeButton.clicked.connect(self.close)
        self.sendButton.clicked.connect(self.send)

        #
        self.addrEdit.setText("127.0.0.1:9080")
        self.numEdit.setText("3")
        #数据
        self.networks = {}

    def connect(self):
        self.addrEdit.setEnabled(False)
        self.numEdit.setEnabled(False)

        try:
            address = self.addrEdit.text()
            num = int(self.numEdit.text())

            address = address.split(":")
            ip = address[0]
            port = int(address[1])

            self.clearNetworks()
            print("关闭所有并新建连接")
            for i in range(num):
                net = Network(ip, port, i )
                net.out.connect(self.update)
                self.networks[i] = net
                net.start()


        except Exception as e:
            QMessageBox.warning(self, "警告",str(e))


    def clearNetworks(self):
        for key in self.networks:
            self.networks[key].close()

        self.networks.clear()


    def close(self):
        self.addrEdit.setEnabled(True)
        self.numEdit.setEnabled(True)

        self.clearNetworks()

    def send(self):
        for key in self.networks:
            self.networks[key].send(self.inputEdit.text())


    def update(self, msg):
        self.log.append(msg)


