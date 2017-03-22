# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 513)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 6, 0, 1, 5)
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadButton.setObjectName("DownloadButton")
        self.gridLayout.addWidget(self.DownloadButton, 13, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 7, 0, 1, 3)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 4, 0, 1, 5)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.DirButton = QtWidgets.QPushButton(self.centralwidget)
        self.DirButton.setObjectName("DirButton")
        self.gridLayout.addWidget(self.DirButton, 7, 4, 1, 1)
        self.TaskBrowser_1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.TaskBrowser_1.setObjectName("TaskBrowser_1")
        self.gridLayout.addWidget(self.TaskBrowser_1, 11, 0, 3, 1)
        self.clearconf = QtWidgets.QPushButton(self.centralwidget)
        self.clearconf.setObjectName("clearconf")
        self.gridLayout.addWidget(self.clearconf, 12, 4, 1, 1)
        self.confacl = QtWidgets.QPushButton(self.centralwidget)
        self.confacl.setObjectName("confacl")
        self.gridLayout.addWidget(self.confacl, 11, 4, 1, 1)
        self.aclsignal = QtWidgets.QLabel(self.centralwidget)
        self.aclsignal.setText("")
        self.aclsignal.setObjectName("aclsignal")
        self.gridLayout.addWidget(self.aclsignal, 9, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.label_4.setText(_translate("MainWindow", "Download Link B"))
        self.lineEdit.setText(_translate("MainWindow", "File directory......"))
        self.label_2.setText(_translate("MainWindow", "Task:"))
        self.label.setText(_translate("MainWindow", "Download Link A"))
        self.DirButton.setText(_translate("MainWindow", "Dir View"))
        self.clearconf.setText(_translate("MainWindow", "Clear ACL"))
        self.confacl.setText(_translate("MainWindow", "Conf ACL"))

