# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from wx.lib.pubsub import Publisher

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 413)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 2)
        self.DirButton = QtWidgets.QPushButton(self.centralwidget)
        self.DirButton.setObjectName("DirButton")
        self.gridLayout.addWidget(self.DirButton, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.TaskBrowser_1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.TaskBrowser_1.setObjectName("TaskBrowser_1")
        self.gridLayout.addWidget(self.TaskBrowser_1, 4, 0, 1, 1)
        self.TaskBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.TaskBrowser_2.setObjectName("TaskBrowser_2")
        self.gridLayout.addWidget(self.TaskBrowser_2, 4, 1, 1, 1)
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadButton.setObjectName("DownloadButton")
        self.gridLayout.addWidget(self.DownloadButton, 4, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        Publisher().subscribe(self.updateDisplay, "update")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "File Address:"))
        self.lineEdit.setText(_translate("MainWindow", "File directory......"))
        self.DirButton.setText(_translate("MainWindow", "Dir View"))
        self.label_2.setText(_translate("MainWindow", "Task A:"))
        self.label_3.setText(_translate("MainWindow", "Task B:"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
