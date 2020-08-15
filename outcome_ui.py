from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_outcomeDialog(object):
    def setupUi(self, outcomeDialog):
        outcomeDialog.setObjectName("outcomeDialog")
        outcomeDialog.resize(380, 60)

        self.outcomeLabel = QtWidgets.QLabel(outcomeDialog)
        self.outcomeLabel.setGeometry(QtCore.QRect(15, 10, 350, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.outcomeLabel.setFont(font)
        self.outcomeLabel.setStyleSheet("background-color: rgb(244, 255, 246);")
        self.outcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.outcomeLabel.setObjectName("outcomeLabel")

        self.exitButton = QtWidgets.QPushButton(outcomeDialog)
        self.exitButton.setGeometry(QtCore.QRect(170, 35, 60, 20))
        self.exitButton.setObjectName("exitButton")

        self.retranslateUi(outcomeDialog)
        QtCore.QMetaObject.connectSlotsByName(outcomeDialog)

    def retranslateUi(self, outcomeDialog):
        _translate = QtCore.QCoreApplication.translate
        outcomeDialog.setWindowTitle(_translate("outcomeDialog", "Finished"))
        self.outcomeLabel.setText(_translate("outcomeDialog", "The selected pdf files have been watermarked successfully!"))
        self.exitButton.setText(_translate("outcomeDialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    outcomeDialog = QtWidgets.QDialog()
    ui = Ui_outcomeDialog()
    ui.setupUi(outcomeDialog)
    outcomeDialog.show()
    sys.exit(app.exec_())
