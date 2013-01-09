#coding=utf-8
__author__ = 'icestar'

import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QDir

from view.WinMain import WinMain
from controller.Project import Project

from cache import PixmapCache

class Application:

    def __init__(self):
        self.app = QApplication(sys.argv)

        # 图片资源路径
        PixmapCache.addSearchPath("res")

        self.project = Project()
        self.win = WinMain( self.project )





    def start(self):
        self.win.show()
        sys.exit(self.app.exec_())


