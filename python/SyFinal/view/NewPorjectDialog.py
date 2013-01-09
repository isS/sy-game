#coding=utf-8
__author__ = 'icestar'

from PyQt4.QtGui import *
from PyQt4 import QtCore

class NewProjectDialog(QDialog):

    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        self.resize(302, 104)
        self.setSizeGripEnabled(True)
        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.editProjectName = QLineEdit(self)
        self.editProjectName.setObjectName("editProjectName")
        self.horizontalLayout.addWidget(self.editProjectName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(self)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.editPath = QLineEdit(self)
        self.editPath.setObjectName(("editPath"))
        self.horizontalLayout_2.addWidget(self.editPath)
        self.buttonBrowse = QPushButton(self)
        self.buttonBrowse.setMaximumSize(QtCore.QSize(30, 16777215))
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.horizontalLayout_2.addWidget(self.buttonBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.buttonOk = QPushButton(self)
        self.buttonOk.setObjectName("buttonOk")
        self.horizontalLayout_3.addWidget(self.buttonOk)
        self.buttonCancel = QPushButton(self)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout_3.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.setWindowTitle("新建项目")
        self.label.setText("项目：")
        self.label_2.setText("路径：")
        self.buttonBrowse.setText("...")
        self.buttonOk.setText("确定")
        self.buttonCancel.setText("取消")


        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self.reject)
        QtCore.QObject.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.accept)
        self.buttonBrowse.clicked.connect(self.browse)

    def browse(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "获取路径", self.editPath.text(), options)
        if directory:
            self.editPath.setText(directory)

    @staticmethod
    def newProjct():
        dlg = NewProjectDialog()
        result = dlg. exec_()
        if result == QDialog.Accepted :
            return True, (dlg.editProjectName.text(), dlg.editPath.text())
        else:
            return False, None



