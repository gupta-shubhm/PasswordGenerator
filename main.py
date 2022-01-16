import random
import sys
from functools import partial
from string import ascii_letters, digits, punctuation, ascii_lowercase, ascii_uppercase
import pyperclip
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from passgen import Ui_PassGenerator
from passgen_dialog import Ui_Dialog


class PassGenDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_ok.clicked.connect(self.close)
        self.ui.button_closedialog.clicked.connect(self.close)

        def moveWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_top_btns.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_PassGenerator()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.dialog = PassGenDialog()
        self.ui.setupUi(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropshadowFrame.setGraphicsEffect(self.shadow)

        # SELF VARIABLES
        self.characters = ascii_letters + digits + punctuation

        self.password = None
        self.defaultLength = 8
        self.flagUpperCase = False
        self.flagLowerCase = False
        self.flagNumber = False
        self.flagSymbol = False

        # BUTTON ACTIONS
        self.ui.checkBox_uppercase.stateChanged.connect(partial(self.state_changed, self.ui.checkBox_uppercase))
        self.ui.checkBox_lowercase.stateChanged.connect(partial(self.state_changed, self.ui.checkBox_lowercase))
        self.ui.checkBox_numbers.stateChanged.connect(partial(self.state_changed, self.ui.checkBox_numbers))
        self.ui.checkBox_symbols.stateChanged.connect(partial(self.state_changed, self.ui.checkBox_symbols))
        self.ui.button_copy_password.clicked.connect(self.copyPassword)
        self.ui.window_close_button.clicked.connect(self.close)
        self.ui.button_generate_password.clicked.connect(self.generatePassword)

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.dropshadowFrame.mouseMoveEvent = moveWindow
        self.ui.label_main.mouseMoveEvent = moveWindow
        self.ui.generated_password.mouseMoveEvent = moveWindow
        self.ui.frame_params.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def copyPassword(self):
        passwd = self.password
        pyperclip.copy(passwd)

    def checkFlags(self):
        passSet = ""
        passList = [self.flagUpperCase, self.flagLowerCase, self.flagNumber, self.flagSymbol]
        for value in range(len(passList)):
            if value == 0:
                if passList[0]:
                    passSet += ascii_uppercase
            if value == 1:
                if passList[1]:
                    passSet += ascii_lowercase

            if value == 2:
                if passList[2]:
                    passSet += digits

            if value == 3:
                if passList[3]:
                    passSet += punctuation

        return passSet

    def generatePassword(self):
        characterSet = self.checkFlags()
        if self.ui.lineEdit_passLength.text() != "":
            if int(self.ui.lineEdit_passLength.text()) > 40 or int(self.ui.lineEdit_passLength.text()) < 4:
                self.dialog.show()
                return
            self.defaultLength = int(self.ui.lineEdit_passLength.text())
        else:
            self.defaultLength = 8

        if characterSet != "":
            self.password = "".join(random.sample(characterSet, self.defaultLength))
        else:
            self.password = "".join(random.sample(self.characters, self.defaultLength))

        self.ui.generated_password.setText(self.password)

    def state_changed(self, checkbox: QCheckBox):
        checkboxText = str(checkbox.objectName()).strip()
        if checkboxText == "checkBox_uppercase":
            self.flagUpperCase = checkbox.isChecked()
        if checkboxText == "checkBox_lowercase":
            self.flagLowerCase = checkbox.isChecked()
        if checkboxText == "checkBox_numbers":
            self.flagNumber = checkbox.isChecked()
        if checkboxText == "checkBox_symbols":
            self.flagSymbol = checkbox.isChecked()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
