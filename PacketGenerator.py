from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QRegExpValidator

import sys
import json

from ChoiceDialog import *

import PacketSender as PS

import QueueDialog as QD

STRINGS = ["Empty", "TCP", "UDP", "ICMP"]

# ProtocolSpinBox class is desined to add strings from global STRINGS to QSpinBox for user to choose the protocol
class ProtocolSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent):
        super(ProtocolSpinBox, self).__init__(parent)
        self.setStrings(STRINGS)

    def setStrings(self, strings):
        strings = list(strings)
        self._strings = tuple(strings)
        self._values = dict(zip(strings, range(len(strings))))
        self.setRange(0, len(strings)-1)

    def textFromValue(self, value):
        return self._strings[value]

# PacketGenerator is the main class
class PacketGenerator(object):
    ##
    # FUNCTIONS TO SETUP GUI
    ##

    def setupMain(self, PacketGenerator):
        self.Sender = PS.PacketSender()

        self.FrameParameters = {
            "IP"   : {},
            "TCP"  : {},
            "UDP"  : {},
            "ICMP" : {}
        }
        font = QtGui.QFont()
        font.setPointSize(12)

        self.CurrentPacket = ""

        PacketGenerator.setObjectName("PacketGenerator")
        PacketGenerator.resize(850, 650)
        self.centralwidget = QtWidgets.QWidget(PacketGenerator)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(5, 5, 840, 595))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.pushNewPacket = QtWidgets.QPushButton(self.frame)
        self.pushNewPacket.setGeometry(QtCore.QRect(80, 80, 160, 90))
        self.pushNewPacket.setFont(font)
        self.pushNewPacket.setObjectName("pushNew")
        self.pushNewPacket.clicked.connect(
            self.showIP
        )

        self.pushLoadPacket = QtWidgets.QPushButton(self.frame)
        self.pushLoadPacket.setGeometry(QtCore.QRect(600, 80, 160, 90))
        self.pushLoadPacket.setFont(font)
        self.pushLoadPacket.setObjectName("pushLoad")
        self.pushLoadPacket.clicked.connect(
            self.LoadPacket
        )
        self.pushLoadPacket.clicked.connect(
            self.showIP
        )

        self.pushNewQueue = QtWidgets.QPushButton(self.frame)
        self.pushNewQueue.setGeometry(QtCore.QRect(80, 430, 160, 90))
        self.pushNewQueue.setFont(font)
        self.pushNewQueue.setObjectName("pushNewQueue")
        self.pushNewQueue.clicked.connect(lambda _ = False, load = False:
            self.NewQueue(_, load)
        )

        self.pushLoadQueue = QtWidgets.QPushButton(self.frame)
        self.pushLoadQueue.setGeometry(QtCore.QRect(600, 430, 160, 90))
        self.pushLoadQueue.setFont(font)
        self.pushLoadQueue.setObjectName("pushLoadQueue")
        self.pushLoadQueue.clicked.connect(lambda _ = False, load = True :
            self.NewQueue(_, load)
        )


        PacketGenerator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PacketGenerator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 26))
        self.menubar.setObjectName("menubar")
        PacketGenerator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PacketGenerator)
        self.statusbar.setObjectName("statusbar")
        PacketGenerator.setStatusBar(self.statusbar)

        self.setupIP()
        self.setupTCP()
        self.setupUDP()
        self.setupICMP()

        self.retranslateUi(PacketGenerator)
        QtCore.QMetaObject.connectSlotsByName(PacketGenerator)

        self.showMain()

    def setupIP(self):
        self.frameIP = QtWidgets.QFrame(self.centralwidget)
        self.frameIP.setGeometry(QtCore.QRect(5, 5, 840, 595))
        self.frameIP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameIP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameIP.setObjectName("frameIP")

        self.textBrowserIP = QtWidgets.QTextBrowser(self.frameIP)
        self.textBrowserIP.setGeometry(QtCore.QRect(5, 320, 830, 260))
        self.textBrowserIP.setObjectName("textBrowserIP")
        self.textBrowserIP.setReadOnly(True)

        self.lineEdit_HeaderLength = QtWidgets.QLineEdit(self.frameIP)
        self.lineEdit_HeaderLength.setGeometry(QtCore.QRect(110, 5, 60, 20))
        self.lineEdit_HeaderLength.setText("")
        self.lineEdit_HeaderLength.setObjectName("lineEdit_HeaderLength")

        self.label_IP = QtWidgets.QLabel(self.frameIP)
        self.label_IP.setGeometry(QtCore.QRect(5, 5, 100, 20))
        self.label_IP.setObjectName("label_IP")

        self.label_IP_2 = QtWidgets.QLabel(self.frameIP)
        self.label_IP_2.setGeometry(QtCore.QRect(5, 40, 100, 20))
        self.label_IP_2.setObjectName("label_IP_2")

        self.lineEdit_Identification = QtWidgets.QLineEdit(self.frameIP)
        self.lineEdit_Identification.setGeometry(QtCore.QRect(110, 40, 60, 20))
        self.lineEdit_Identification.setObjectName("lineEdit_Identification")

        self.label_IP_3 = QtWidgets.QLabel(self.frameIP)
        self.label_IP_3.setGeometry(QtCore.QRect(5, 75, 100, 20))
        self.label_IP_3.setObjectName("label_IP_3")

        self.lineEdit_CheckSum_IP = QtWidgets.QLineEdit(self.frameIP)
        self.lineEdit_CheckSum_IP.setGeometry(QtCore.QRect(330, 75, 60, 20))
        self.lineEdit_CheckSum_IP.setObjectName("lineEdit_CheckSum_IP")

        self.label_IP_5 = QtWidgets.QLabel(self.frameIP)
        self.label_IP_5.setGeometry(QtCore.QRect(225, 5, 100, 20))
        self.label_IP_5.setObjectName("label_IP_5")

        self.lineEdit_TotalLength = QtWidgets.QLineEdit(self.frameIP)
        self.lineEdit_TotalLength.setGeometry(QtCore.QRect(330, 5, 60, 20))
        self.lineEdit_TotalLength.setObjectName("lineEdit_TotalLength")

        self.label_IP_6 = QtWidgets.QLabel(self.frameIP)
        self.label_IP_6.setGeometry(QtCore.QRect(225, 75, 100, 20))
        self.label_IP_6.setObjectName("label_IP_6")

        self.label_IP_7 = QtWidgets.QLabel(self.frameIP)
        self.label_IP_7.setGeometry(QtCore.QRect(225, 40, 100, 20))
        self.label_IP_7.setObjectName("label_IP_7")

        self.lineEdit_TTL = QtWidgets.QLineEdit(self.frameIP)
        self.lineEdit_TTL.setGeometry(QtCore.QRect(330, 40, 60, 20))
        self.lineEdit_TTL.setObjectName("lineEdit_TTL")

        self.spinBoxProtocol = ProtocolSpinBox(self.frameIP)
        self.spinBoxProtocol.setGeometry(QtCore.QRect(110, 75, 60, 20))
        self.spinBoxProtocol.setObjectName("spinBoxProtocol")
        self.spinBoxProtocol.lineEdit().setReadOnly(True)
        self.spinBoxProtocol.valueChanged.connect(
            self.ProtocolChanged
        )

        self.frameAddressIP = QtWidgets.QFrame(self.frameIP)
        self.frameAddressIP.setGeometry(QtCore.QRect(420, 5, 410, 90))
        self.frameAddressIP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAddressIP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameAddressIP.setObjectName("frameAddressIP")

        self.label_8_IP = QtWidgets.QLabel(self.frameAddressIP)
        self.label_8_IP.setGeometry(QtCore.QRect(10, 20, 100, 20))
        self.label_8_IP.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8_IP.setObjectName("label_8")

        self.label_9_IP = QtWidgets.QLabel(self.frameAddressIP)
        self.label_9_IP.setGeometry(QtCore.QRect(10, 60, 100, 20))
        self.label_9_IP.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9_IP.setObjectName("label_9")

        self.lineEdit_Source = QtWidgets.QLineEdit(self.frameAddressIP)
        self.lineEdit_Source.setGeometry(QtCore.QRect(120, 20, 200, 20))
        self.lineEdit_Source.setObjectName("lineEdit_Source")

        self.lineEdit_Destination = QtWidgets.QLineEdit(self.frameAddressIP)
        self.lineEdit_Destination.setGeometry(QtCore.QRect(120, 60, 200, 20))
        self.lineEdit_Destination.setObjectName("lineEdit_Destination")

        self.frameService = QtWidgets.QFrame(self.frameIP)
        self.frameService.setGeometry(QtCore.QRect(420, 100, 410, 90))
        self.frameService.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameService.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameService.setObjectName("frameService")

        self.checkBox_Reliability = QtWidgets.QCheckBox(self.frameService)
        self.checkBox_Reliability.setGeometry(QtCore.QRect(260, 70, 95, 20))
        self.checkBox_Reliability.setObjectName("checkBox_Reliability")

        self.checkBox_Throughput = QtWidgets.QCheckBox(self.frameService)
        self.checkBox_Throughput.setGeometry(QtCore.QRect(260, 40, 95, 20))
        self.checkBox_Throughput.setObjectName("checkBox_Throughput")

        self.checkBox_Delay = QtWidgets.QCheckBox(self.frameService)
        self.checkBox_Delay.setGeometry(QtCore.QRect(260, 10, 95, 20))
        self.checkBox_Delay.setObjectName("checkBox_Delay")

        self.lineEdit_Priority = QtWidgets.QLineEdit(self.frameService)
        self.lineEdit_Priority.setGeometry(QtCore.QRect(110, 60, 60, 20))
        self.lineEdit_Priority.setObjectName("lineEdit_Priority")

        self.label_IP_10 = QtWidgets.QLabel(self.frameService)
        self.label_IP_10.setGeometry(QtCore.QRect(50, 60, 50, 20))
        self.label_IP_10.setObjectName("label_IP_10")

        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_IP_4 = QtWidgets.QLabel(self.frameService)
        self.label_IP_4.setGeometry(QtCore.QRect(50, 20, 120, 20))
        self.label_IP_4.setFont(font)
        self.label_IP_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_IP_4.setObjectName("label_IP_4")

        self.frameFragmentation = QtWidgets.QFrame(self.frameIP)
        self.frameFragmentation.setGeometry(QtCore.QRect(420, 195, 410, 90))
        self.frameFragmentation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameFragmentation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFragmentation.setObjectName("frameFragmentation")

        self.checkBox_ReservedFragment = QtWidgets.QCheckBox(self.frameFragmentation)
        self.checkBox_ReservedFragment.setGeometry(QtCore.QRect(260, 20, 120, 20))
        self.checkBox_ReservedFragment.setObjectName("checkBox_ReservedFragment")

        self.checkBox_NoFragment = QtWidgets.QCheckBox(self.frameFragmentation)
        self.checkBox_NoFragment.setGeometry(QtCore.QRect(260, 45, 120, 20))
        self.checkBox_NoFragment.setObjectName("checkBox_NoFragment")

        self.checkBox_MoreFragment = QtWidgets.QCheckBox(self.frameFragmentation)
        self.checkBox_MoreFragment.setGeometry(QtCore.QRect(260, 70, 120, 20))
        self.checkBox_MoreFragment.setObjectName("checkBox_MoreFragment")

        self.lineEdit_Offset = QtWidgets.QLineEdit(self.frameFragmentation)
        self.lineEdit_Offset.setGeometry(QtCore.QRect(110, 60, 60, 20))
        self.lineEdit_Offset.setObjectName("lineEdit_Offset")

        self.label_IP_11 = QtWidgets.QLabel(self.frameFragmentation)
        self.label_IP_11.setGeometry(QtCore.QRect(50, 60, 50, 20))
        self.label_IP_11.setObjectName("label_IP_11")

        self.label_IP_12 = QtWidgets.QLabel(self.frameFragmentation)
        self.label_IP_12.setGeometry(QtCore.QRect(50, 20, 120, 20))
        self.label_IP_12.setFont(font)
        self.label_IP_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_IP_12.setObjectName("label_IP_12")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButtonMainMenu_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonMainMenu_IP.setGeometry(QtCore.QRect(20, 160, 120, 40))
        self.pushButtonMainMenu_IP.setFont(font)
        self.pushButtonMainMenu_IP.setObjectName("pushButtonMainMenu_IP")
        self.pushButtonMainMenu_IP.clicked.connect(
            self.showMain
        )

        self.pushButtonNext_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonNext_IP.setGeometry(QtCore.QRect(230, 160, 120, 40))
        self.pushButtonNext_IP.setFont(font)
        self.pushButtonNext_IP.setObjectName("pushButtonNext_IP")
        self.pushButtonNext_IP.clicked.connect(
            self.showNext
        )


        self.pushButtonSave_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonSave_IP.setGeometry(QtCore.QRect(20, 210, 120, 40))
        self.pushButtonSave_IP.setFont(font)
        self.pushButtonSave_IP.setObjectName("pushButton_Save_IP")
        self.pushButtonSave_IP.clicked.connect(
            self.SavePacket
        )

        self.pushButtonLoad_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonLoad_IP.setGeometry(QtCore.QRect(230, 210, 120, 40))
        self.pushButtonLoad_IP.setFont(font)
        self.pushButtonLoad_IP.setObjectName("pushButton_Load_IP")
        self.pushButtonLoad_IP.clicked.connect(
            self.LoadPacket
        )

        font.setPointSize(12)
        self.pushButtonPreview_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonPreview_IP.setGeometry(QtCore.QRect(5, 285, 90, 30))
        self.pushButtonPreview_IP.setFont(font)
        self.pushButtonPreview_IP.setObjectName("pushButton_Preview_IP")
        self.pushButtonPreview_IP.clicked.connect(
            self.PreviewPacket
        )

        font.setPointSize(8)
        self.pushButtonAutoCS_IP = QtWidgets.QPushButton(self.frameIP)
        self.pushButtonAutoCS_IP.setGeometry(QtCore.QRect(225, 105, 75, 20))
        self.pushButtonAutoCS_IP.setFont(font)
        self.pushButtonAutoCS_IP.setObjectName("pushButton_Preview_IP")
        self.pushButtonAutoCS_IP.clicked.connect(lambda state = True, elem = self.lineEdit_CheckSum_IP: 
            self.AutoCheckSum(state, elem)
        )
  
    def setupTCP(self):
        self.frameTCP = QtWidgets.QFrame(self.centralwidget)
        self.frameTCP.setGeometry(QtCore.QRect(5, 5, 840, 595))
        self.frameTCP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTCP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTCP.setObjectName("frameTCP")

        self.textEdit_Data_TCP = QtWidgets.QTextEdit(self.frameTCP)
        self.textEdit_Data_TCP.setGeometry(QtCore.QRect(5, 290, 830, 260))
        self.textEdit_Data_TCP.setObjectName("lineEdit_SourcePort")
        self.textEdit_Data_TCP.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.CheckFlagsTCP = QtWidgets.QFrame(self.frameTCP)
        self.CheckFlagsTCP.setGeometry(QtCore.QRect(570, 10, 260, 280))
        self.CheckFlagsTCP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CheckFlagsTCP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CheckFlagsTCP.setObjectName("CheckFlagsTCP")

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.checkBox_CWR = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_CWR.setGeometry(QtCore.QRect(20, 15, 80, 20))
        self.checkBox_CWR.setFont(font)
        self.checkBox_CWR.setObjectName("checkBox_CWR")
        self.checkBox_CWR.stateChanged.connect(lambda state = self.checkBox_CWR.isChecked(), 
                    elem = self.checkBox_CWR: self.TCPCheckHandler(state, elem))

        self.checkBox_ECN = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_ECN.setGeometry(QtCore.QRect(160, 15, 80, 20))
        self.checkBox_ECN.setFont(font)
        self.checkBox_ECN.setObjectName("checkBox_ECN")
        self.checkBox_ECN.stateChanged.connect(lambda state = self.checkBox_ECN.isChecked(), 
                    elem = self.checkBox_ECN: self.TCPCheckHandler(state, elem))

        self.checkBox_SYN = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_SYN.setGeometry(QtCore.QRect(20, 65, 80, 20))
        self.checkBox_SYN.setFont(font)
        self.checkBox_SYN.setObjectName("checkBox_SYN")
        self.checkBox_SYN.stateChanged.connect(lambda state = self.checkBox_SYN.isChecked(), 
                    elem = self.checkBox_SYN: self.TCPCheckHandler(state, elem))

        self.checkBox_ACK = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_ACK.setGeometry(QtCore.QRect(160, 65, 80, 20))
        self.checkBox_ACK.setFont(font)
        self.checkBox_ACK.setObjectName("checkBox_ACK")
        self.checkBox_ACK.stateChanged.connect(lambda state = self.checkBox_ACK.isChecked(), 
                    elem = self.checkBox_ACK: self.TCPCheckHandler(state, elem))

        self.checkBox_RST = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_RST.setGeometry(QtCore.QRect(20, 115, 80, 20))
        self.checkBox_RST.setFont(font)
        self.checkBox_RST.setObjectName("checkBox_RST")
        self.checkBox_RST.stateChanged.connect(lambda state = self.checkBox_RST.isChecked(), 
                    elem = self.checkBox_RST: self.TCPCheckHandler(state, elem))

        self.checkBox_URG = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_URG.setGeometry(QtCore.QRect(160, 115, 80, 20))
        self.checkBox_URG.setFont(font)
        self.checkBox_URG.setObjectName("checkBox_URG")
        self.checkBox_URG.stateChanged.connect(lambda state = self.checkBox_URG.isChecked(), 
                    elem = self.checkBox_URG: self.TCPCheckHandler(state, elem))

        self.checkBox_PSH = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_PSH.setGeometry(QtCore.QRect(20, 165, 80, 20))
        self.checkBox_PSH.setFont(font)
        self.checkBox_PSH.setObjectName("checkBox_PSH")
        self.checkBox_PSH.stateChanged.connect(lambda state = self.checkBox_PSH.isChecked(), 
                    elem = self.checkBox_PSH: self.TCPCheckHandler(state, elem))

        self.checkBox_FIN = QtWidgets.QCheckBox(self.CheckFlagsTCP)
        self.checkBox_FIN.setGeometry(QtCore.QRect(160, 165, 80, 20))
        self.checkBox_FIN.setFont(font)
        self.checkBox_FIN.setObjectName("checkBox_FIN")
        self.checkBox_FIN.stateChanged.connect(lambda state = self.checkBox_FIN.isChecked(), 
                    elem = self.checkBox_FIN: self.TCPCheckHandler(state, elem))

        self.lineEdit_SourcePort_TCP = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_SourcePort_TCP.setGeometry(QtCore.QRect(110, 5, 120, 20))
        self.lineEdit_SourcePort_TCP.setObjectName("lineEdit_SourcePort")

        self.label_TCP_1 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_1.setGeometry(QtCore.QRect(5, 5, 100, 20))
        self.label_TCP_1.setObjectName("label_TCP_1")

        self.label_TCP_2 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_2.setGeometry(QtCore.QRect(5, 40, 100, 20))
        self.label_TCP_2.setObjectName("label_TCP_2")

        self.lineEdit_DestPort_TCP = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_DestPort_TCP.setGeometry(QtCore.QRect(110, 40, 120, 20))
        self.lineEdit_DestPort_TCP.setObjectName("lineEdit_DestPort")

        self.label_TCP_3 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_3.setGeometry(QtCore.QRect(5, 75, 100, 20))
        self.label_TCP_3.setObjectName("label_TCP_3")

        self.lineEdit_TCPOffset = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_TCPOffset.setGeometry(QtCore.QRect(110, 75, 120, 20))
        self.lineEdit_TCPOffset.setObjectName("lineEdit_TCPOffset")

        self.label_TCP_4 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_4.setGeometry(QtCore.QRect(5, 110, 100, 20))
        self.label_TCP_4.setObjectName("label_TCP_4")

        self.lineEdit_WindowSize = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_WindowSize.setGeometry(QtCore.QRect(110, 110, 120, 20))
        self.lineEdit_WindowSize.setObjectName("lineEdit_WindowSize")

        self.lineEdit_CheckSum_TCP = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_CheckSum_TCP.setGeometry(QtCore.QRect(390, 110, 120, 20))
        self.lineEdit_CheckSum_TCP.setObjectName("lineEdit_CheckSum_TCP")

        self.label_TCP_5 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_5.setGeometry(QtCore.QRect(285, 5, 100, 20))
        self.label_TCP_5.setObjectName("label_TCP_5")

        self.lineEdit_Sequence = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_Sequence.setGeometry(QtCore.QRect(390, 5, 120, 20))
        self.lineEdit_Sequence.setObjectName("lineEdit_Sequence")

        self.label_TCP_6 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_6.setGeometry(QtCore.QRect(285, 75, 100, 20))
        self.label_TCP_6.setObjectName("label_TCP_6")

        self.label_TCP_7 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_7.setGeometry(QtCore.QRect(285, 40, 100, 20))
        self.label_TCP_7.setObjectName("label_TCP_7")

        self.label_TCP_8 = QtWidgets.QLabel(self.frameTCP)
        self.label_TCP_8.setGeometry(QtCore.QRect(285, 110, 100, 20))
        self.label_TCP_8.setObjectName("label_TCP_8")

        self.lineEdit_Urgent = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_Urgent.setGeometry(QtCore.QRect(390, 75, 120, 20))
        self.lineEdit_Urgent.setObjectName("lineEdit_Urgent")

        self.lineEdit_Acknolegement = QtWidgets.QLineEdit(self.frameTCP)
        self.lineEdit_Acknolegement.setGeometry(QtCore.QRect(390, 40, 120, 20))
        self.lineEdit_Acknolegement.setObjectName("lineEdit_Acknolegement")

        font = QtGui.QFont()
        font.setPointSize(14)

        self.pushButtonMainMenu_TCP = QtWidgets.QPushButton(self.frameTCP)
        self.pushButtonMainMenu_TCP.setGeometry(QtCore.QRect(5, 190, 120, 30))
        self.pushButtonMainMenu_TCP.setFont(font)
        self.pushButtonMainMenu_TCP.setObjectName("pushButtonMainMenu_TCP")
        self.pushButtonMainMenu_TCP.clicked.connect(
            self.showMain
        )

        self.pushButtonSend_TCP = QtWidgets.QPushButton(self.frameTCP)
        self.pushButtonSend_TCP.setGeometry(QtCore.QRect(190, 190, 120, 30))
        self.pushButtonSend_TCP.setFont(font)
        self.pushButtonSend_TCP.setObjectName("pushButtonSend_TCP")
        self.pushButtonSend_TCP.clicked.connect(
            self.SendPacket
        )

        self.pushButtonSave_TCP = QtWidgets.QPushButton(self.frameTCP)
        self.pushButtonSave_TCP.setGeometry(QtCore.QRect(5, 230, 120, 30))
        self.pushButtonSave_TCP.setFont(font)
        self.pushButtonSave_TCP.setObjectName("pushButtonSave_TCP")
        self.pushButtonSave_TCP.clicked.connect(
            self.SavePacket
        )

        self.pushButtonBack_TCP = QtWidgets.QPushButton(self.frameTCP)
        self.pushButtonBack_TCP.setGeometry(QtCore.QRect(190, 230, 120, 30))
        self.pushButtonBack_TCP.setFont(font)
        self.pushButtonBack_TCP.setObjectName("pushButtonBack_TCP")
        self.pushButtonBack_TCP.clicked.connect(
            self.showIP
        )

        font.setPointSize(8)
        self.pushButtonAutoCS_TCP = QtWidgets.QPushButton(self.frameTCP)
        self.pushButtonAutoCS_TCP.setGeometry(QtCore.QRect(285, 140, 75, 20))
        self.pushButtonAutoCS_TCP.setFont(font)
        self.pushButtonAutoCS_TCP.setObjectName("pushButton_Preview_TCP")
        self.pushButtonAutoCS_TCP.clicked.connect(lambda state = True, elem = self.lineEdit_CheckSum_TCP: 
            self.AutoCheckSum(state, elem)
        )

    def setupUDP(self):
        self.frameUDP = QtWidgets.QFrame(self.centralwidget)
        self.frameUDP.setGeometry(QtCore.QRect(5, 5, 840, 595))
        self.frameUDP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameUDP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameUDP.setObjectName("frameUDP")

        self.textEdit_Data_UDP = QtWidgets.QTextEdit(self.frameUDP)
        self.textEdit_Data_UDP.setGeometry(QtCore.QRect(5, 290, 830, 260))
        self.textEdit_Data_UDP.setObjectName("lineEdit_SourcePort")
        self.textEdit_Data_UDP.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)


        self.lineEdit_SourcePort_UDP = QtWidgets.QLineEdit(self.frameUDP)
        self.lineEdit_SourcePort_UDP.setGeometry(QtCore.QRect(110, 5, 120, 20))
        self.lineEdit_SourcePort_UDP.setObjectName("lineEdit_SourcePort")
        self.label_UDP_1 = QtWidgets.QLabel(self.frameUDP)
        self.label_UDP_1.setGeometry(QtCore.QRect(5, 5, 100, 20))
        self.label_UDP_1.setObjectName("label_UDP_1")
        self.label_UDP_2 = QtWidgets.QLabel(self.frameUDP)
        self.label_UDP_2.setGeometry(QtCore.QRect(5, 40, 100, 20))
        self.label_UDP_2.setObjectName("label_UDP_2")
        self.lineEdit_DestPort_UDP = QtWidgets.QLineEdit(self.frameUDP)
        self.lineEdit_DestPort_UDP.setGeometry(QtCore.QRect(110, 40, 120, 20))
        self.lineEdit_DestPort_UDP.setObjectName("lineEdit_DestPort")
        self.label_UDP_5 = QtWidgets.QLabel(self.frameUDP)
        self.label_UDP_5.setGeometry(QtCore.QRect(285, 5, 100, 20))
        self.label_UDP_5.setObjectName("label_UDP_5")
        self.lineEdit_Length = QtWidgets.QLineEdit(self.frameUDP)
        self.lineEdit_Length.setGeometry(QtCore.QRect(390, 5, 120, 20))
        self.lineEdit_Length.setObjectName("lineEdit_Length")
        self.label_UDP_7 = QtWidgets.QLabel(self.frameUDP)
        self.label_UDP_7.setGeometry(QtCore.QRect(285, 40, 100, 20))
        self.label_UDP_7.setObjectName("label_UDP_7")
        self.lineEdit_CheckSum_UDP = QtWidgets.QLineEdit(self.frameUDP)
        self.lineEdit_CheckSum_UDP.setGeometry(QtCore.QRect(390, 40, 120, 20))
        self.lineEdit_CheckSum_UDP.setObjectName("lineEdit_CheckSum_UDP")


        font = QtGui.QFont()
        font.setPointSize(14)

        self.pushButtonMainMenu_UDP = QtWidgets.QPushButton(self.frameUDP)
        self.pushButtonMainMenu_UDP.setGeometry(QtCore.QRect(5, 175, 120, 30))
        self.pushButtonMainMenu_UDP.setFont(font)
        self.pushButtonMainMenu_UDP.setObjectName("pushButtonMainMenu_UDP")
        self.pushButtonMainMenu_UDP.clicked.connect(
            self.showMain
        )


        self.pushButtonSave_UDP = QtWidgets.QPushButton(self.frameUDP)
        self.pushButtonSave_UDP.setGeometry(QtCore.QRect(190, 175, 120, 30))
        self.pushButtonSave_UDP.setFont(font)
        self.pushButtonSave_UDP.setObjectName("pushButtonSave_UDP")
        self.pushButtonSave_UDP.clicked.connect(
            self.SavePacket
        )

        self.pushButtonSend_UDP = QtWidgets.QPushButton(self.frameUDP)
        self.pushButtonSend_UDP.setGeometry(QtCore.QRect(5, 230, 120, 30))
        self.pushButtonSend_UDP.setFont(font)
        self.pushButtonSend_UDP.setObjectName("pushButtonSend_UDP")
        self.pushButtonSend_UDP.clicked.connect(
            self.SendPacket
        )

        self.pushButtonBack_UDP = QtWidgets.QPushButton(self.frameUDP)
        self.pushButtonBack_UDP.setGeometry(QtCore.QRect(190, 230, 120, 30))
        self.pushButtonBack_UDP.setFont(font)
        self.pushButtonBack_UDP.setObjectName("pushButtonBack_UDP")
        self.pushButtonBack_UDP.clicked.connect(
            self.showIP
        )

        font.setPointSize(8)
        self.pushButtonAutoCS_UDP = QtWidgets.QPushButton(self.frameUDP)
        self.pushButtonAutoCS_UDP.setGeometry(QtCore.QRect(285, 60, 75, 20))
        self.pushButtonAutoCS_UDP.setFont(font)
        self.pushButtonAutoCS_UDP.setObjectName("pushButton_Preview_UDP")
        self.pushButtonAutoCS_UDP.clicked.connect(lambda state = True, elem = self.lineEdit_CheckSum_UDP: 
            self.AutoCheckSum(state, elem)
        )
      
    def setupICMP(self):
        self.frameICMP = QtWidgets.QFrame(self.centralwidget)
        self.frameICMP.setGeometry(QtCore.QRect(5, 5, 840, 595))
        self.frameICMP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameICMP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameICMP.setObjectName("frameICMP")

        font = QtGui.QFont()
        font.setPointSize(14)

        self.pushButtonMainMenu_ICMP = QtWidgets.QPushButton(self.frameICMP)
        self.pushButtonMainMenu_ICMP.setGeometry(QtCore.QRect(20, 140, 120, 40))
        self.pushButtonMainMenu_ICMP.setFont(font)
        self.pushButtonMainMenu_ICMP.setObjectName("pushButtonMainMenu_ICMP")
        self.pushButtonMainMenu_ICMP.clicked.connect(
            self.showMain
        )

        self.pushButtonSave_ICMP = QtWidgets.QPushButton(self.frameICMP)
        self.pushButtonSave_ICMP.setGeometry(QtCore.QRect(230, 140, 120, 40))
        self.pushButtonSave_ICMP.setFont(font)
        self.pushButtonSave_ICMP.setObjectName("pushButton_Save_ICMP")
        self.pushButtonSave_ICMP.clicked.connect(
            self.SavePacket
        )

        self.pushButton_Send_ICMP = QtWidgets.QPushButton(self.frameICMP)
        self.pushButton_Send_ICMP.setGeometry(QtCore.QRect(20, 210, 120, 40))
        self.pushButton_Send_ICMP.setFont(font)
        self.pushButton_Send_ICMP.setObjectName("pushButton_Send_ICMP")
        self.pushButton_Send_ICMP.clicked.connect(
            self.SendPacket
        )

        self.pushButtonBack_ICMP = QtWidgets.QPushButton(self.frameICMP)
        self.pushButtonBack_ICMP.setGeometry(QtCore.QRect(230, 210, 120, 40))
        self.pushButtonBack_ICMP.setFont(font)
        self.pushButtonBack_ICMP.setObjectName("pushButtonBack_ICMP")
        self.pushButtonBack_ICMP.clicked.connect(
            self.showIP
        )

        self.label_ICMP = QtWidgets.QLabel(self.frameICMP)
        self.label_ICMP.setGeometry(QtCore.QRect(470, 0, 60, 35))
        self.label_ICMP.setFont(font)
        self.label_ICMP.setObjectName("label")

        self.frameType_ICMP = QtWidgets.QFrame(self.frameICMP)
        self.frameType_ICMP.setGeometry(QtCore.QRect(20, 10, 200, 120))
        self.frameType_ICMP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameType_ICMP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameType_ICMP.setObjectName("frameType_ICMP")

        font.setPointSize(11)
        self.label_ICMP_3 = QtWidgets.QLabel(self.frameType_ICMP)
        self.label_ICMP_3.setGeometry(QtCore.QRect(50, 10, 100, 20))
        self.label_ICMP_3.setFont(font)
        self.label_ICMP_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ICMP_3.setObjectName("label_ICMP_3")
        font.setPointSize(14)

        self.radioButton_EchoRequest = QtWidgets.QRadioButton(self.frameType_ICMP)
        self.radioButton_EchoRequest.setGeometry(QtCore.QRect(10, 50, 101, 20))
        self.radioButton_EchoRequest.setObjectName("radioButton_EchoRequest")
        
        self.radioButton_EchoReply = QtWidgets.QRadioButton(self.frameType_ICMP)
        self.radioButton_EchoReply.setGeometry(QtCore.QRect(10, 90, 101, 20))
        self.radioButton_EchoReply.setObjectName("radioButton_EchoReply")

        self.label_ICMP_2 = QtWidgets.QLabel(self.frameICMP)
        self.label_ICMP_2.setGeometry(QtCore.QRect(230, 40, 60, 20))
        self.label_ICMP_2.setObjectName("label_ICMP_2")

        self.lineEdit_CheckSum_ICMP = QtWidgets.QLineEdit(self.frameICMP)
        self.lineEdit_CheckSum_ICMP.setGeometry(QtCore.QRect(300, 40, 80, 20))
        self.lineEdit_CheckSum_ICMP.setObjectName("lineEdit_CheckSum_ICMP")

        self.textEdit_Data_ICMP = QtWidgets.QTextEdit(self.frameICMP)
        self.textEdit_Data_ICMP.setGeometry(QtCore.QRect(470, 30, 360, 260))
        self.textEdit_Data_ICMP.setText("")
        self.textEdit_Data_ICMP.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.textEdit_Data_ICMP.setObjectName("textEdit_Data_ICMP")

        font.setPointSize(8)
        self.pushButtonAutoCS_ICMP = QtWidgets.QPushButton(self.frameICMP)
        self.pushButtonAutoCS_ICMP.setGeometry(QtCore.QRect(230, 65, 75, 20))
        self.pushButtonAutoCS_ICMP.setFont(font)
        self.pushButtonAutoCS_ICMP.setObjectName("pushButton_Preview_ICMP")
        self.pushButtonAutoCS_ICMP.clicked.connect(lambda state = True, elem = self.lineEdit_CheckSum_ICMP: 
            self.AutoCheckSum(state, elem)
        )

    def retranslateUi(self, PacketGenerator):
        _translate = QtCore.QCoreApplication.translate
        PacketGenerator.setWindowTitle(_translate("PacketGenerator", "PacketGenerator"))
        self.pushNewPacket.setText(_translate("PacketGenerator", "New Packet"))
        self.pushLoadPacket.setText(_translate("PacketGenerator", "Load Packet"))
        self.pushNewQueue.setText(_translate("PacketGenerator", "New Queue"))
        self.pushLoadQueue.setText(_translate("PacketGenerator", "Load Queue"))

        self.checkBox_CWR.setText(_translate("PacketGenerator", "CWR"))
        self.checkBox_ECN.setText(_translate("PacketGenerator", "ECN"))
        self.checkBox_SYN.setText(_translate("PacketGenerator", "SYN"))
        self.checkBox_ACK.setText(_translate("PacketGenerator", "ACK"))
        self.checkBox_RST.setText(_translate("PacketGenerator", "RST"))
        self.checkBox_URG.setText(_translate("PacketGenerator", "URG"))
        self.checkBox_PSH.setText(_translate("PacketGenerator", "PSH"))
        self.checkBox_FIN.setText(_translate("PacketGenerator", "FIN"))
        self.label_TCP_1.setText(_translate("PacketGenerator", "Source Port:"))
        self.label_TCP_2.setText(_translate("PacketGenerator", "Destination Port:"))
        self.label_TCP_3.setText(_translate("PacketGenerator", "Data:"))
        self.label_TCP_4.setText(_translate("PacketGenerator", "Window Size:"))
        self.label_TCP_5.setText(_translate("PacketGenerator", "Sequence:"))
        self.label_TCP_6.setText(_translate("PacketGenerator", "Urgent:"))
        self.label_TCP_7.setText(_translate("PacketGenerator", "Acknolegement:"))
        self.label_TCP_8.setText(_translate("PacketGenerator", "CheckSum:"))
        self.pushButtonMainMenu_TCP.setText(_translate("PacketGenerator", "MENU"))
        self.pushButtonSave_TCP.setText(_translate("PacketGenerator", "SAVE"))
        self.pushButtonSend_TCP.setText(_translate("PacketGenerator", "SEND"))
        self.pushButtonBack_TCP.setText(_translate("PacketGenerator", "BACK"))
        self.pushButtonAutoCS_TCP.setText(_translate("PacketGenerator", "Auto"))

        self.label_UDP_1.setText(_translate("PacketGenerator", "Source Port:"))
        self.label_UDP_2.setText(_translate("PacketGenerator", "Destination Port:"))
        self.label_UDP_5.setText(_translate("PacketGenerator", "Length:"))
        self.label_UDP_7.setText(_translate("PacketGenerator", "CheckSum:"))
        self.pushButtonMainMenu_UDP.setText(_translate("PacketGenerator", "MENU"))
        self.pushButtonSave_UDP.setText(_translate("PacketGenerator", "SAVE"))
        self.pushButtonSend_UDP.setText(_translate("PacketGenerator", "SEND"))
        self.pushButtonBack_UDP.setText(_translate("PacketGenerator", "BACK"))
        self.pushButtonAutoCS_UDP.setText(_translate("PacketGenerator", "Auto"))

        self.label_IP.setText(_translate("PacketGenerator", "Header Length:"))
        self.label_IP_2.setText(_translate("PacketGenerator", "Identification:"))
        self.label_IP_3.setText(_translate("PacketGenerator", "Protocol:"))
        self.label_IP_5.setText(_translate("PacketGenerator", "Total Length:"))
        self.label_IP_6.setText(_translate("PacketGenerator", "CheckSum:"))
        self.label_IP_7.setText(_translate("PacketGenerator", "TTL:"))
        self.label_8_IP.setText(_translate("PacketGenerator", "Source IP:"))
        self.label_9_IP.setText(_translate("PacketGenerator", "Destination IP:"))
        self.checkBox_Reliability.setText(_translate("PacketGenerator", "Reliability"))
        self.checkBox_Throughput.setText(_translate("PacketGenerator", "Throughput"))
        self.checkBox_Delay.setText(_translate("PacketGenerator", "Delay"))
        self.label_IP_10.setText(_translate("PacketGenerator", "Priority:"))
        self.label_IP_4.setText(_translate("PacketGenerator", "Type of Service"))
        self.checkBox_MoreFragment.setText(_translate("PacketGenerator", "More Fragments"))
        self.checkBox_NoFragment.setText(_translate("PacketGenerator", "Do not Fragment"))
        self.checkBox_ReservedFragment.setText(_translate("PacketGenerator", "Reserved Bit"))
        self.label_IP_11.setText(_translate("PacketGenerator", "Offset:"))
        self.label_IP_12.setText(_translate("PacketGenerator", "Fragmentation"))
        self.pushButtonMainMenu_IP.setText(_translate("PacketGenerator", "MENU"))
        self.pushButtonSave_IP.setText(_translate("PacketGenerator", "SAVE"))
        self.pushButtonNext_IP.setText(_translate("PacketGenerator", "NEXT"))
        self.pushButtonLoad_IP.setText(_translate("PacketGenerator", "LOAD"))
        self.pushButtonPreview_IP.setText(_translate("PacketGenerator", "Preview"))
        self.pushButtonAutoCS_IP.setText(_translate("PacketGenerator", "Auto"))

        self.pushButtonMainMenu_ICMP.setText(_translate("PacketGenerator", "MENU"))
        self.pushButtonSave_ICMP.setText(_translate("PacketGenerator", "SAVE"))
        self.pushButton_Send_ICMP.setText(_translate("PacketGenerator", "SEND"))
        self.pushButtonBack_ICMP.setText(_translate("PacketGenerator", "BACK"))
        self.label_ICMP.setText(_translate("PacketGenerator", "Data:"))
        self.label_ICMP_3.setText(_translate("PacketGenerator", "ICMP Type"))
        self.radioButton_EchoRequest.setText(_translate("PacketGenerator", "Echo request"))
        self.radioButton_EchoReply.setText(_translate("PacketGenerator", "Echo reply"))
        self.label_ICMP_2.setText(_translate("PacketGenerator", "CheckSum"))
        self.pushButtonAutoCS_ICMP.setText(_translate("PacketGenerator", "Auto"))

    ##
    #
    ##

    ##
    # FUNCTIONS TO SHOW GUI PARTS
    ##


    def showMain(self):
        self.FrameParameters["IP"]['Protocol'] = ""
        self.frameTCP.hide()
        self.frameUDP.hide()
        self.frame.show()
        self.frameIP.hide()
        self.frameICMP.hide()

    def showIP(self):
        self.FrameParameters["IP"]['Protocol'] = self.spinBoxProtocol.textFromValue(
            self.spinBoxProtocol.value())

        self.frameTCP.hide()
        self.frameUDP.hide()
        self.frame.hide()
        self.frameICMP.hide()

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   # Part of the regular expression
        ipRegex = QtCore.QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, parent = None)   

        self.lineEdit_Source.setValidator(ipValidator)
        self.lineEdit_Destination.setValidator(ipValidator)

        self.frameIP.show()

    def showNext(self):
        if self.FrameParameters["IP"]['Protocol'] == "TCP":
            self.showTCP()
        elif self.FrameParameters["IP"]['Protocol'] == "UDP":
            self.showUDP()
        elif self.FrameParameters["IP"]['Protocol'] == "ICMP":
            self.showICMP()
        elif self.FrameParameters["IP"]['Protocol'] == "Empty":
            self.SendPacket()
        else:
            return

    def showTCP(self):
        self.FrameParameters["IP"]['Protocol'] = "TCP"
        self.frameTCP.show()
        self.frameUDP.hide()
        self.frame.hide()
        self.frameIP.hide()
        self.frameICMP.hide()
    
    def showUDP(self):
        self.FrameParameters["IP"]['Protocol'] = "UDP"
        self.frameTCP.hide()
        self.frameUDP.show()
        self.frame.hide()
        self.frameIP.hide()
        self.frameICMP.hide()

    def showICMP(self):
        self.FrameParameters["IP"]['Protocol'] = "ICMP"
        self.frameTCP.hide()
        self.frameUDP.hide()
        self.frame.hide()
        self.frameIP.hide()
        self.frameICMP.show()
        self.radioButton_EchoRequest.setChecked(True)

    ##
    #
    ##

    ##
    # FUNCTIONS TO GET PACKET PARAMETERS FROM GUI TO DICT
    ##

    def FetchParameters(self):
        self.FetchParametersIP()
        
        if self.FrameParameters["IP"]['Protocol'] == "TCP":
            self.FetchParametersTCP()
        elif self.FrameParameters["IP"]['Protocol'] == "UDP":
            self.FetchParametersUDP()
        elif self.FrameParameters["IP"]['Protocol'] == "ICMP":
            self.FetchParametersICMP()

    def FetchParametersIP(self):

        self.FrameParameters["IP"]['Protocol']      = self.spinBoxProtocol.textFromValue(
            self.spinBoxProtocol.value())
        
        self.FrameParameters["IP"]['Source']      = self.lineEdit_Source.text()
        self.FrameParameters["IP"]['Destination']        = self.lineEdit_Destination.text()

        self.FrameParameters["IP"]['Header']        = self.lineEdit_HeaderLength.text()
        self.FrameParameters["IP"]['Identification']= self.lineEdit_Identification.text()
        self.FrameParameters["IP"]['CheckSumIP']    = self.lineEdit_CheckSum_IP.text()
        self.FrameParameters["IP"]['TotalLength']   = self.lineEdit_TotalLength.text()
        self.FrameParameters["IP"]['TTL']           = self.lineEdit_TTL.text()

        self.FrameParameters["IP"]['Priority']      = self.lineEdit_Priority.text()
        self.FrameParameters["IP"]['Offset']        = self.lineEdit_Offset.text()

        self.FrameParameters["IP"]['Service']       = ""
        if self.checkBox_Delay.isChecked():
            self.FrameParameters["IP"]['Service'] += "Delay"
        if self.checkBox_Throughput.isChecked():
            self.FrameParameters["IP"]['Service'] += "Throughput"
        if self.checkBox_Reliability.isChecked():
            self.FrameParameters["IP"]['Service'] += "Reliability"
        
        self.FrameParameters["IP"]['Fragmentation'] = ""
        if self.checkBox_ReservedFragment.isChecked():
            self.FrameParameters["IP"]['Fragmentation'] += "Reserved"
        if self.checkBox_NoFragment.isChecked():
            self.FrameParameters["IP"]['Fragmentation'] += "NoFragment"
        if self.checkBox_MoreFragment.isChecked():
            self.FrameParameters["IP"]['Fragmentation'] += "MoreFragment"
    
    def FetchParametersTCP(self):
        self.FrameParameters["TCP"]['Source']       = self.lineEdit_SourcePort_TCP.text()
        self.FrameParameters["TCP"]['Destination']  = self.lineEdit_DestPort_TCP.text()
        self.FrameParameters["TCP"]['TCPOffset']    = self.lineEdit_TCPOffset.text()
        self.FrameParameters["TCP"]['Window']       = self.lineEdit_WindowSize.text()
        self.FrameParameters["TCP"]['Sequence']     = self.lineEdit_Sequence.text()
        self.FrameParameters["TCP"]['Acknolegement']= self.lineEdit_Acknolegement.text()
        self.FrameParameters["TCP"]['CheckSumTCP']  = self.lineEdit_CheckSum_TCP.text()
        self.FrameParameters["TCP"]['Urgent']       = self.lineEdit_Urgent.text()
        self.FrameParameters["TCP"]['DataTCP']      = self.textEdit_Data_TCP.toPlainText()

    def FetchParametersUDP(self):
        self.FrameParameters["UDP"]['Source']       = self.lineEdit_SourcePort_UDP.text()
        self.FrameParameters["UDP"]['Destination']  = self.lineEdit_DestPort_UDP.text()
        self.FrameParameters["UDP"]['Length']       = self.lineEdit_Length.text()
        self.FrameParameters["UDP"]['CheckSumUDP']  = self.lineEdit_CheckSum_UDP.text()
        self.FrameParameters["UDP"]['DataUDP']      = self.textEdit_Data_UDP.toPlainText()
    
    def FetchParametersICMP(self):
        self.FrameParameters["ICMP"]['CheckSumICMP']= self.lineEdit_CheckSum_ICMP.text()
        self.FrameParameters["ICMP"]['DataICMP']    = self.textEdit_Data_ICMP.toPlainText()

        self.FrameParameters["ICMP"]['TypeICMP']    = ""

        if self.radioButton_EchoReply.isChecked():
            self.FrameParameters["ICMP"]['TypeICMP']= "EchoReply"
        elif self.radioButton_EchoRequest.isChecked():
            self.FrameParameters["ICMP"]['TypeICMP']= "EchoRequest"

    ##
    #
    ##

    ##
    # FUNCTIONS TO OPERATE WITH PACKETS
    ##

    def SavePacket(self):
        self.FetchParameters()
        
        dialog_app = QtWidgets.QDialog()
        DialogWindow = SaveDialog()
        DialogWindow.setupUi(dialog_app, 
            self.FrameParameters.copy())
        dialog_app.exec()

    def ShowPacket(self):
        self.lineEdit_HeaderLength.setText(
            self.FrameParameters["IP"].get('Header',         ""))
        self.lineEdit_Identification.setText(
            self.FrameParameters["IP"].get('Identification', ""))
        self.lineEdit_CheckSum_IP.setText(
            self.FrameParameters["IP"].get('CheckSumIP',     ""))
        self.lineEdit_TotalLength.setText(
            self.FrameParameters["IP"].get('TotalLength',    ""))
        self.lineEdit_TTL.setText(
            self.FrameParameters["IP"].get('TTL',            ""))
        
        self.lineEdit_Priority.setText(
            self.FrameParameters["IP"].get('Priority',       ""))
        self.lineEdit_Offset.setText(
            self.FrameParameters["IP"].get('Offset',         ""))
        
        self.lineEdit_Source.setText(
            self.FrameParameters["IP"].get('Source',       ""))
        self.lineEdit_Destination.setText(
            self.FrameParameters["IP"].get('Destination',         ""))
        
        if self.FrameParameters["IP"].get('Protocol', "") == "":
            self.spinBoxProtocol.setValue(0)
        else:
            self.spinBoxProtocol.setValue(
                STRINGS.index(self.FrameParameters["IP"]['Protocol'])
            )
        

        if "NoFragment" in self.FrameParameters["IP"].get('Fragmentation',   ""):
            self.checkBox_NoFragment.setChecked(True)
        if "MoreFragment" in self.FrameParameters["IP"].get('Fragmentation', ""):
            self.checkBox_MoreFragment.setChecked(True)
        if "Reserved" in self.FrameParameters["IP"].get('Fragmentation',     ""):
            self.checkBox_ReservedFragment.setChecked(True)
        

        if "Delay" in self.FrameParameters["IP"].get('Service',              ""):
            self.checkBox_Delay.setChecked(True)
        if "Througput" in self.FrameParameters["IP"].get('Service',          ""):
            self.checkBox_Throughput.setChecked(True)
        if "Reliability" in self.FrameParameters["IP"].get('Service',        ""):
            self.checkBox_Reliability.setChecked(True)


        if   self.FrameParameters["IP"]['Protocol'] == "TCP":
            self.lineEdit_SourcePort_TCP.setText(
                self.FrameParameters["TCP"].get('Source',       ""))
            self.lineEdit_DestPort_TCP.setText(
                self.FrameParameters["TCP"].get('Destination',  ""))
            self.lineEdit_TCPOffset.setText(
                self.FrameParameters["TCP"].get('TCPOffset',    ""))
            self.lineEdit_WindowSize.setText(
                self.FrameParameters["TCP"].get('Window',       ""))
            self.lineEdit_Sequence.setText(
                self.FrameParameters["TCP"].get('Sequence',     ""))
            self.lineEdit_Acknolegement.setText(
                self.FrameParameters["TCP"].get('Acknolegement',""))
            self.lineEdit_CheckSum_TCP.setText(
                self.FrameParameters["TCP"].get('CheckSumTCP',  ""))
            self.lineEdit_Urgent.setText(
                self.FrameParameters["TCP"].get('Urgent',       ""))
            self.textEdit_Data_TCP.setText(
                self.FrameParameters["TCP"].get('DataTCP',      ""))

            self.checkBox_CWR.setCheckState(
                self.FrameParameters["TCP"].get('CWR',          False))
            self.checkBox_ECN.setCheckState(
                self.FrameParameters["TCP"].get('CWR',          False))
            self.checkBox_SYN.setCheckState(
                self.FrameParameters["TCP"].get('SYN',          False))
            self.checkBox_ACK.setCheckState(
                self.FrameParameters["TCP"].get('ACK',          False))
            self.checkBox_URG.setCheckState(
                self.FrameParameters["TCP"].get('URG',          False))
            self.checkBox_PSH.setCheckState(
                self.FrameParameters["TCP"].get('PSH',          False))
            self.checkBox_RST.setCheckState(
                self.FrameParameters["TCP"].get('RST',          False))
            self.checkBox_FIN.setCheckState(
                self.FrameParameters["TCP"].get('FIN',          False))

        elif self.FrameParameters["IP"]['Protocol'] == "UDP":
            self.lineEdit_SourcePort_UDP.setText(
                self.FrameParameters["UDP"].get('Source',      ""))
            self.lineEdit_DestPort_UDP.setText(
                self.FrameParameters["UDP"].get('Destination', ""))
            self.lineEdit_Length.setText(
                self.FrameParameters["UDP"].get('Length',      ""))
            self.lineEdit_CheckSum_UDP.setText(
                self.FrameParameters["UDP"].get('CheckSumUDP', ""))
            self.textEdit_Data_UDP.setText(
                self.FrameParameters["UDP"].get('DataUDP',     ""))

        elif self.FrameParameters["IP"]['Protocol'] == "ICMP":
            self.lineEdit_CheckSum_ICMP.setText(
                self.FrameParameters["ICMP"].get('CheckSumICMP', ""))
            self.textEdit_Data_ICMP.setText(
                self.FrameParameters["ICMP"].get('DataICMP',     ""))
        
            if self.FrameParameters["ICMP"].get('TypeICMP', "") == "EchoRequest":
                self.radioButton_EchoRequest.setChecked(True)
            else:
                self.radioButton_EchoReply.setChecked(True)
            
    def LoadPacket(self):
        dialog_app = QtWidgets.QDialog()
        DialogWindow = LoadDialog()
        DialogWindow.setupUi(dialog_app)
        if dialog_app.exec() == 1:
            filename = DialogWindow.GetName()
        else:
            return
        
        self.CurrentPacket = filename
        with open(filename, "r") as file:
            self.FrameParameters = json.load(file)
        
        self.ShowPacket()

    def SendPacket(self):
        self.FetchParameters()

        if not self.ValidateParameters():
            return
        
        self.Sender.FormPacket(params = self.FrameParameters)
        ifs = self.Sender.GetInterfaces()

        dialog_app = QtWidgets.QDialog()
        SendWindow = SendDialog()
        SendWindow.setupUi(dialog_app, ifs.keys())
        if dialog_app.exec() == 1:
            self.Sender.SendPacket(SendWindow.GetName())
        else:
            return
    
    ##
    #
    ##

    ##
    #SIDE FUNCTIONS
    ##

    # ValidateParameters() is used to check if user set neccessary parameters (Src and Dst)
    def ValidateParameters(self):
        if self.FrameParameters["IP"]['Source'] == "" or self.FrameParameters["IP"]['Destination'] == "":
            CallErrorBox("You must set source and destination IP!")
            return False

        if self.FrameParameters["IP"]['Protocol'] == "ICMP":
            if self.radioButton_EchoReply.isChecked() == self.radioButton_EchoRequest.isChecked():
                CallErrorBox("You must choose an ICMP type!")
                return False
        elif self.FrameParameters["IP"]['Protocol'] == "TCP":
            if self.FrameParameters["TCP"]['Source'] == "" or self.FrameParameters["TCP"]['Destination'] == "":
                CallErrorBox("You must set source and destination ports!")
                return False
        elif self.FrameParameters["IP"]['Protocol'] == "UDP":
            if self.FrameParameters["UDP"]['Source'] == "" or self.FrameParameters["UDP"]['Destination'] == "":
                CallErrorBox("You must set source and destination ports!")
                return False
        
        return True

    # PreviewPacket()) is used to form the packet and show it
    def PreviewPacket(self):
        self.FetchParameters()
        self.Sender.FormPacket(params = self.FrameParameters)
        packet = self.Sender.GetPacket()
        self.textBrowserIP.setText(packet)

    # AutoCheckSum() automatically fills the checksum field
    def AutoCheckSum(self, _, label):
        self.FetchParameters()
        self.Sender.FormPacket(params = self.FrameParameters)
        checksum = self.Sender.UpdateCheckSum(
            self.FrameParameters["IP"]['Protocol'])
        
        label.setText(checksum)

    # TCPCheckHandler() reacts to TCP flag changes
    def TCPCheckHandler(self, state, elem):
        if state == 0:
            self.FrameParameters["TCP"][elem.text()] = False
        else:
            self.FrameParameters["TCP"][elem.text()] = True
        pass
    
    # ProtocolChanged() reacts to IP protocol changes
    def ProtocolChanged(self):
        self.FrameParameters["IP"]['Protocol'] = self.spinBoxProtocol.textFromValue(
            self.spinBoxProtocol.value())

    # NewQueue() is used to create new packet queue (Starts a dialog window)
    def NewQueue(self, _, load):
        dialog_app = QtWidgets.QDialog()
        QWindow = QD.QueueDialog()
        QWindow.setupUi(dialog_app, state = False, load = load)
        dialog_app.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_app = QtWidgets.QMainWindow()
    ui = PacketGenerator()
    ui.setupMain(main_app)
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()