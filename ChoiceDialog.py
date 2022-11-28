from PyQt5 import QtCore, QtWidgets

import json
from glob import glob

def CallErrorBox(message : str):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setWindowTitle("ERROR")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


class comboItem(QtWidgets.QComboBox):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.setStyleSheet('font-size: 14px')
        self.addItems(items)
        self.currentIndexChanged.connect(self.getComboValue)

    def getComboValue(self):
        return self.currentText()

class SuperDialog():
    def setupUi(self, Dialog, items = None):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 200)

        self.result = ""

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 130, 120, 40))
        self.pushButton.setObjectName("pushButton")

        self.comboBox = None
        self.lineEdit = None

        if items != None:
            self.comboBox = comboItem(Dialog, items)
            self.comboBox.setGeometry(QtCore.QRect(60, 65, 280, 30))
            self.comboBox.setObjectName("comboBox")
            self.result = self.comboBox.getComboValue()
        else:
            self.lineEdit = QtWidgets.QLineEdit(Dialog)
            self.lineEdit.setGeometry(QtCore.QRect(100, 70, 200, 20))
            self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(135, 30, 130, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
    
    def GetName(self):
        return self.result

class LoadDialog(SuperDialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog, items=glob("*.P"))
        _translate = QtCore.QCoreApplication.translate

        self.label.setText(_translate("Dialog", "Enter packet to open"))
        self.pushButton.setText(_translate("Dialog", "Open"))
        self.pushButton.clicked.connect(lambda : self.FindFile(Dialog))


    def FindFile(self, Dilaog):
        self.result = self.comboBox.getComboValue()
        try:
            file = open(self.result, "r")
            file.close()
        except:
            CallErrorBox("File not found!")
            return
        Dilaog.accept()


class SaveDialog(SuperDialog):
    def setupUi(self, Dialog, parameters):
        super().setupUi(Dialog)
        _translate = QtCore.QCoreApplication.translate

        try:
            if parameters["IP"]['Protocol'] == "TCP":
                del parameters["UDP"]
                del parameters["ICMP"]
            elif parameters["IP"]['Protocol'] == "UDP":
                del parameters["TCP"]
                del parameters["ICMP"]
            elif parameters["IP"]['Protocol'] == "ICMP":
                del parameters["TCP"]
                del parameters["UDP"]
            else:
                del parameters["TCP"]
                del parameters["UDP"]
                del parameters["ICMP"]
        except:
            pass
        
        self.label.setText(_translate("Dialog", "Enter name to save"))
        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton.clicked.connect(lambda : self.SaveFile(Dialog, parameters))

    def SaveFile(self, Dilaog, parameters):
        if not ".P" in self.lineEdit.text() or self.lineEdit.text() == "":
            CallErrorBox("File must have a name and '.P' format")
            return
        self.result = self.lineEdit.text()
        try:
            with open(self.lineEdit.text(), "w") as file:
                json.dump(parameters, file, indent = 4, separators=(',\n', ': '))
        except Exception as e:
            CallErrorBox(f'Saving Error. Exception: {e}')
            return
        Dilaog.accept()


class LoadQueueDialog(SuperDialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog, items=glob("*.Q"))
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Choose queue to open"))
        self.pushButton.setText(_translate("Dialog", "Open"))
        self.pushButton.clicked.connect(lambda : self.FindFile(Dialog))

    def FindFile(self, Dilaog):
        self.result = self.comboBox.getComboValue()
        try:
            file = open(self.result, "r")
            file.close()
        except:
            CallErrorBox("File not found!")
            return
        Dilaog.accept()



class SendDialog(SuperDialog):
    def setupUi(self, Dialog, ifs):
        super().setupUi(Dialog, items=ifs)

        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Choose Interface to send"))
        self.pushButton.setText(_translate("Dialog", "Send"))
        self.pushButton.clicked.connect(lambda : self.ButtonPush(Dialog))
    
    def ButtonPush(self, Dialog):
        self.result = self.comboBox.getComboValue()
        Dialog.accept()
