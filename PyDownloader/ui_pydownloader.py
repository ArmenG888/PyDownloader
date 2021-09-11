# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pydownloaderoPlSit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 423)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setGeometry(QRect(0, 0, 640, 423))
        self.frame.setMouseTracking(False)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(56,58,89);\n"
"	color: rgb(220, 220, 220);\n"
"	border-radius: 10px\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.ip_label = QLabel(self.frame)
        self.ip_label.setObjectName(u"ip_label")
        self.ip_label.setGeometry(QRect(160, 140, 81, 31))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(12)
        self.ip_label.setFont(font)
        self.title = QLabel(self.frame)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(160, 20, 351, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(40)
        self.title.setFont(font1)
        self.title.setStyleSheet(u"color: rgb(254,121,199);")
        self.port_label = QLabel(self.frame)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setGeometry(QRect(200, 180, 41, 31))
        self.port_label.setFont(font)
        self.start_server_button = QPushButton(self.frame)
        self.start_server_button.setObjectName(u"start_server_button")
        self.start_server_button.setGeometry(QRect(250, 220, 151, 41))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(20)
        font2.setBold(False)
        font2.setWeight(50)
        self.start_server_button.setFont(font2)
        self.start_server_button.setAutoFillBackground(False)
        self.start_server_button.setStyleSheet(u"background-color: rgb(98,114,250);")
        self.start_server_button.setFlat(False)
        self.ip_entry = QLineEdit(self.frame)
        self.ip_entry.setObjectName(u"ip_entry")
        self.ip_entry.setGeometry(QRect(250, 140, 151, 31))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(14)
        self.ip_entry.setFont(font3)
        self.port_entry = QLineEdit(self.frame)
        self.port_entry.setObjectName(u"port_entry")
        self.port_entry.setGeometry(QRect(250, 180, 151, 31))
        self.port_entry.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.start_server_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ip_label.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"PyDownloader", None))
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.start_server_button.setText(QCoreApplication.translate("MainWindow", u"Start Server", None))
    # retranslateUi

