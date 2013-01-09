#coding=utf-8
__author__ = 'icestar'


from PyQt4.QtGui import QTabWidget, QTabBar, QWidget, QHBoxLayout, QMenu, QToolButton, QIcon
from PyQt4.QtCore import pyqtSignal, Qt

class CentralWidget(QTabWidget):

    def __init__(self, parent = None):
        super(QTabWidget, self).__init__(parent)

        self.__createTabBar()
        self.__createCornerWidget()

        widget = QWidget(self)
        self.addTab(widget,"")

        self.setTabsClosable(True)              #是否可以关闭
        self.setTabShape(QTabWidget.Triangular) #标签的形状
        self.setMovable(True)                   #标签是否可以动
        self.setTabPosition(QTabWidget.South)   #标签的位置
        self.setUsesScrollButtons(True)  #标签超出时宽度时可以左右滚动


        self.tabCloseRequested.connect(self.closeTab)


    def __createTabBar(self):
        self.__tabbar = QTabBar(self)
        self.setTabBar(self.__tabbar)

    def __createCornerWidget(self):
        self.__rightCornerWidget = QWidget(self)
        self.__rightCornerWidgetLayout = QHBoxLayout(self.__rightCornerWidget)
        self.__rightCornerWidgetLayout.setMargin(0)
        self.__rightCornerWidgetLayout.setSpacing(0)

        self.__navigationMenu = QMenu(self)
        #        self.__navigationMenu.aboutToShow.connect(self.__showNavigationMenu)
        #        self.__navigationMenu.triggered.connect(self.__navigationMenuTriggered)

        self.__navigationButton = QToolButton(self)
        self.__navigationButton.setIcon(QIcon("resource/Solid Iron Chest.ico"))
        self.__navigationButton.setToolTip("显示导航菜单")
        self.__navigationButton.setPopupMode(QToolButton.InstantPopup)
        self.__navigationButton.setMenu(self.__navigationMenu)
        self.__navigationButton.setEnabled(True)
        self.__rightCornerWidgetLayout.addWidget(self.__navigationButton)


        self.__closeButton = QToolButton(self)
        self.__closeButton.setIcon(QIcon("resource/Solid Iron Chest.ico"))
        self.__closeButton.setToolTip("关闭当前视图")
        self.__closeButton.setEnabled(True)
        self.__closeButton.clicked[bool].connect(self.addEmptyTab)
        self.__rightCornerWidgetLayout.addWidget(self.__closeButton)

        self.setCornerWidget(self.__rightCornerWidget, Qt.TopRightCorner)

    def addEmptyTab(self):
        widget = QWidget(self)
        self.addTab(widget,"")

    def closeTab(self, index):
        self.removeTab(index)

    def nextTab(self):
        """
        Public slot used to show the next tab.
        """
        ind = self.currentIndex() + 1
        if ind == self.count():
            ind = 0

        self.setCurrentIndex(ind)
        self.currentWidget().setFocus()

    def prevTab(self):
        """
        Public slot used to show the previous tab.
        """
        ind = self.currentIndex() - 1
        if ind == -1:
            ind = self.count() - 1

        self.setCurrentIndex(ind)
        self.currentWidget().setFocus()

