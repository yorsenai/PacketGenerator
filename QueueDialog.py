import json
from glob import glob
import time

from PyQt5.QtWidgets import QTableWidget
from PyQt5 import QtCore, QtWidgets, QtGui

from ChoiceDialog import LoadQueueDialog, SendDialog, CallErrorBox, comboItem
import PacketSender as PS

class TableWidget(QTableWidget):
    def __init__(self, parent):
        super(TableWidget, self).__init__(1, 3, parent = parent)
        self.packets = glob("*.P")
        self.packets.append("-")
        self.setHorizontalHeaderLabels(['Packet', 'Amount', 'Delay'])
        self.setColumnWidth(4, 100)
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(150)

        combo = comboItem(self, self.packets)
        self.setCellWidget(0, 0, combo)
        line = QtWidgets.QLineEdit(self)
        line.setText("0")
        self.setCellWidget(0, 1, line)
        line = QtWidgets.QLineEdit(self)
        line.setText("0")
        self.setCellWidget(0, 2 ,line)
    
    def GetPackets(self):
        return self.packets


class QueueDialog(object):
    def setupUi(self, Dialog, state, load):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 600)

        self.tableWidget = TableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 700, 500))
        self.tableWidget.setObjectName("tableWidget")
        

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 100, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")


        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(750, 50, 120, 40))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonSave.clicked.connect(
            self.SaveQueue
        )

        self.pushButtonLoad = QtWidgets.QPushButton(Dialog)
        self.pushButtonLoad.setGeometry(QtCore.QRect(750, 120, 120, 40))
        self.pushButtonLoad.setObjectName("pushButtonLoad")
        self.pushButtonLoad.clicked.connect(
            self.LoadQueue
        )


        self.pushButtonSend = QtWidgets.QPushButton(Dialog)
        self.pushButtonSend.setGeometry(QtCore.QRect(750, 190, 120, 40))
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.pushButtonSend.clicked.connect(
            self.SendQueue
        )

        self.pushButtonDel = QtWidgets.QPushButton(Dialog)
        self.pushButtonDel.setGeometry(QtCore.QRect(750, 450, 120, 40))
        self.pushButtonDel.setObjectName("pushButtonDel")
        self.pushButtonDel.clicked.connect(lambda :
            self.DeleteRow(_ = True)
        )


        self.pushButtonAdd = QtWidgets.QPushButton(Dialog)
        self.pushButtonAdd.setGeometry(QtCore.QRect(750, 510, 120, 40))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonAdd.clicked.connect(lambda :
            self.AddNewRow(_ = True)
        )

        self.lineEditName = QtWidgets.QLineEdit(Dialog)
        self.lineEditName.setGeometry(QtCore.QRect(130, 10, 100, 30))
        self.lineEditName.setObjectName("lineEditName")

        self.retranslateUi(Dialog)

        if load:
            self.LoadQueue()

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Name:"))
        self.pushButtonSave.setText(_translate("Dialog", "SAVE"))
        self.pushButtonLoad.setText(_translate("Dialog", "LOAD"))
        self.pushButtonSend.setText(_translate("Dialog", "SEND"))
        self.pushButtonDel.setText(_translate("Dialog", "Delete Row"))
        self.pushButtonAdd.setText(_translate("Dialog", "Add Row"))
    
    def AddNewRow(self, _, packet  = "-", amount  = "0", delay  = "0"):
        self.tableWidget.insertRow( self.tableWidget.rowCount() )

        combo = comboItem(self.tableWidget, self.tableWidget.GetPackets())
        combo.setCurrentText(packet)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, combo)

        line = QtWidgets.QLineEdit(self.tableWidget)
        line.setText(amount)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 1, line)

        line = QtWidgets.QLineEdit(self.tableWidget)
        line.setText(delay)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 2, line)
    
    def DeleteRow(self, _):
        # self.tableWidget.removeRow(
        #     self.tableWidget.rowCount()
        # )
        # pass
        cnt = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(cnt-1)
    
    def SaveQueue(self):
        queue = []
        for i in range(self.tableWidget.rowCount()):
            entry = {}
            widget = self.tableWidget.cellWidget(i, 0)
            if isinstance(widget, comboItem):
                entry['packet'] = widget.currentText()

            widget = self.tableWidget.cellWidget(i, 1)
            if isinstance(widget, QtWidgets.QLineEdit):
                entry['amount'] = widget.text()

            widget = self.tableWidget.cellWidget(i, 2)
            if isinstance(widget, QtWidgets.QLineEdit):
                entry['delay'] = widget.text()
            queue.append(entry)
        
        if self.lineEditName.text() == "":
            name = "default_queue.Q"
        else:
            if not ".Q" in self.lineEditName.text():
                CallErrorBox("File name must have '.Q' format")
                return
            else:
                name = self.lineEditName.text()
    
        with open(name, "w") as file:
            json.dump(queue, file)
    
    def LoadQueue(self):
        dialog_app = QtWidgets.QDialog()
        DialogWindow = LoadQueueDialog()
        DialogWindow.setupUi(dialog_app)
        if dialog_app.exec() == 1:
            filename = DialogWindow.GetName()
        else:
            return
        self.tableWidget.setRowCount(0)
        with open(filename, "r") as file:
            entrys = json.load(file)
        
        for elem in entrys:
            self.AddNewRow(_ = True, packet = elem.get('packet', "-"),
                amount=elem.get('amount', "0"), delay=elem.get('delay', "-"))
    

    def SendQueue(self):
        Sender = PS.PacketSender()
        ifs = Sender.GetInterfaces()

        dialog_app = QtWidgets.QDialog()
        SendWindow = SendDialog()
        SendWindow.setupUi(dialog_app, ifs.keys())
        if dialog_app.exec() != 1:
            return
        for i in range(self.tableWidget.rowCount()):

            widget = self.tableWidget.cellWidget(i, 0)
            if isinstance(widget, comboItem):
                packet = widget.currentText()

            widget = self.tableWidget.cellWidget(i, 1)
            if isinstance(widget, QtWidgets.QLineEdit):
                amount = widget.text()
            
            widget = self.tableWidget.cellWidget(i, 2)
            if isinstance(widget, QtWidgets.QLineEdit):
                delay = widget.text()
            for _ in range(int(amount)):
                Sender.FormPacket(filename = packet)
                Sender.SendPacket(SendWindow.GetName())
                time.sleep(int(delay))
