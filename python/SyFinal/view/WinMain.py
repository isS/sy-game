#coding=utf-8
__author__ = 'icestar'

import os
from PyQt4.QtGui import *
from PyQt4 import QtCore

from view.CentralWidget import CentralWidget

from view.NewPorjectDialog import NewProjectDialog
from view.NetworkTestWidget import NetworkTestWidget

from cache import PixmapCache
import Prefrences

class WinMain(QMainWindow):



    def __init__(self, project):
        super(QMainWindow, self).__init__()
        self.setObjectName("WinMain")
        self.setWindowTitle("最终幻想")
        self.resize(763, 536)
        self.setWindowIcon(PixmapCache.getIcon("chest.ico"))

        self.project = project

        self.createAction()
        self.createToolBar()
        self.createCentralWidget()
        self.createDockWindow()
        self.createStatusBar()


    def createAction(self):
        self.actionNewProject = QAction(PixmapCache.getIcon(Prefrences.icons['action_new_project']), "新建项目", self)
        self.actionNewProject.setText("新建项目")

        self.actionNetworkTest = QAction(PixmapCache.getIcon(Prefrences.icons['action_network_test']), "网络测试", self)
        self.actionNetworkTest.setText("网络测试")


        self.actionNewProject.triggered.connect(self.newProject)
        self.actionNetworkTest.triggered.connect(self.networkTest)


    def createToolBar(self):
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolbar.addAction(self.actionNewProject)

        toolbar.addSeparator()

        toolbar.addAction(self.actionNetworkTest)


        self.addToolBar(toolbar)

    def createCentralWidget(self):
        self.centralWidget = CentralWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)

    def createDockWindow(self):
        self.dockProject = QDockWidget("项目", self)
        self.dockProject.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        tempWidget = QListWidget(self.dockProject)
        self.dockProject.setWidget(tempWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockProject)

    def createStatusBar(self):
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

    # 加载方案
    def loadProject(self):
        pass

    # 新建方案
    def newProject(self):
        ok, result = NewProjectDialog.newProjct()
        if ok :
            path = result[1] + "/" + result[0] + ".sygp"
            if not os.path.exists(result[1]):
                QMessageBox.warning(self, "警告", "路径不存在！")
            elif os.path.exists(path) :
                QMessageBox.warning(self, "警告", "路径已经存在！")



    def networkTest(self):
        dlg = NetworkTestWidget(self)
        dlg.show()




'''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(763, 536)
        MainWindow.setWindowTitle("最终幻想")

        #icon
        iconWindow = QtGui.QIcon("resource/Solid Iron Chest.ico")
        iconAnimation = QtGui.QIcon("resource/Alliance Banner.ico")
        iconEffect =QtGui.QIcon("resource/Horde Banner.ico")

        #win main
        MainWindow.setWindowIcon(iconWindow)

        #        mapView = MapView.MapView(MainWindow) #主控件
        #        mainLayout = QtGui.QHBoxLayout()
        #        mainLayout.set


        self.centralWidget = Ui_TabWidget.TabWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)



        #action
        #动画action
        self.animationAction = QtGui.QAction(MainWindow)
        self.animationAction.setIcon(iconAnimation)
        self.animationAction.setText("动画")
        self.animationAction.setToolTip("动画编辑器")
        self.animationAction.setShortcut("Ctrl+Alt+A")
        self.animationAction.setObjectName("animationAction")

        #特效action
        self.effectAction = QtGui.QAction(MainWindow)
        self.effectAction.setIcon(iconEffect)
        #self.effectAction.setText(QtGui.QApplication.translate("MainWindow", "特效", None, QtGui.QApplication.UnicodeUTF8))
        self.effectAction.setText("特效")
        self.effectAction.setToolTip(QtGui.QApplication.translate("MainWindow", "特效编辑器", None, QtGui.QApplication.UnicodeUTF8))
        self.effectAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+E", None, QtGui.QApplication.UnicodeUTF8))
        self.effectAction.setObjectName("effectAction")

        #网络模拟器
        self.networkAction = QtGui.QAction(MainWindow)
        self.networkAction.setIcon(iconEffect)
        self.networkAction.setText(QtGui.QApplication.translate("MainWindow", "网络", None, QtGui.QApplication.UnicodeUTF8))
        self.networkAction.setToolTip(QtGui.QApplication.translate("MainWindow", "网络模拟器", None, QtGui.QApplication.UnicodeUTF8))
        self.networkAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+N", None, QtGui.QApplication.UnicodeUTF8))
        self.networkAction.setObjectName("effectAction")


        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setText(QtGui.QApplication.translate("MainWindow", "项目", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setObjectName("action_2")
        self.action_4 = QtGui.QAction(MainWindow)
        self.action_4.setText(QtGui.QApplication.translate("MainWindow", "场景", None, QtGui.QApplication.UnicodeUTF8))
        self.action_4.setObjectName("action_4")
        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setText(QtGui.QApplication.translate("MainWindow", "实体", None, QtGui.QApplication.UnicodeUTF8))
        self.action_6.setObjectName("action_6")
        self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setText(QtGui.QApplication.translate("MainWindow", "组件", None, QtGui.QApplication.UnicodeUTF8))
        self.action_7.setObjectName("action_7")
        self.action_8 = QtGui.QAction(MainWindow)
        self.action_8.setText(QtGui.QApplication.translate("MainWindow", "脚本", None, QtGui.QApplication.UnicodeUTF8))
        self.action_8.setObjectName("action_8")
        self.action_10 = QtGui.QAction(MainWindow)
        self.action_10.setText(QtGui.QApplication.translate("MainWindow", "关闭项目", None, QtGui.QApplication.UnicodeUTF8))
        self.action_10.setObjectName("action_10")
        self.action_11 = QtGui.QAction(MainWindow)
        self.action_11.setText(QtGui.QApplication.translate("MainWindow", "关闭", None, QtGui.QApplication.UnicodeUTF8))
        self.action_11.setObjectName("action_11")
        self.action_13 = QtGui.QAction(MainWindow)
        self.action_13.setText(QtGui.QApplication.translate("MainWindow", "关闭", None, QtGui.QApplication.UnicodeUTF8))
        self.action_13.setObjectName("action_13")
        self.action_14 = QtGui.QAction(MainWindow)
        self.action_14.setText(QtGui.QApplication.translate("MainWindow", "打开", None, QtGui.QApplication.UnicodeUTF8))
        self.action_14.setObjectName("action_14")


        #ToolBar
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addAction(self.animationAction)
        #self.toolBar.addSeparator()                     #分割条
        self.toolBar.addAction(self.effectAction)
        self.toolBar.addAction(self.networkAction)


        #Menu
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 763, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "文件(&F)", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setObjectName("menu")
        self.menu_2 = QtGui.QMenu(self.menu)
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "新建", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setObjectName("menu_2")
        self.menu_2.addAction(self.action_2)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_4)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_6)
        self.menu_2.addAction(self.action_7)
        self.menu_2.addAction(self.action_8)
        self.menu.addAction(self.menu_2.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.action_14)
        self.menuBar.addAction(self.menu.menuAction())
        MainWindow.setMenuBar(self.menuBar)

        #状态条
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        #dock
        self.createDockWindow(MainWindow)

        self.retranslateUi(MainWindow)
        self.animationAction.triggered.connect(self.onAnimationTriggered)
        self.effectAction.triggered.connect(self.onEffectTriggered)
        #QtCore.QObject.connect(self.toolBar, QtCore.SIGNAL(_fromUtf8("actionTriggered(QAction*)")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def createDockWindow(self, mainWindow):
        self.dockProject = QtGui.QDockWidget("项目", mainWindow)
        self.dockProject.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        tempWidget = QtGui.QListWidget(self.dockProject)
        self.dockProject.setWidget(tempWidget)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockProject)



    def onAnimationTriggered(self):
        print("animation")

    def onEffectTriggered(self):
        print("effect")

'''


