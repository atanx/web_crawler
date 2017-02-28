#!/usr/bin/env python
#coding=utf-8
import sys
from PyQt4 import QtCore, QtGui, uic

class Login(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_dlgLogovanje()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.buttonLogin, QtCore.SIGNAL("clicked()"), self.doLogin)

    def doLogin(self):
        name = str(self.ui.lineKorisnik.text())
        passwd = str(self.ui.lineSifra.text())
        if name == "john" and passwd =="doe":
            self.runIt()
        else:
            QtGui.QMessageBox.warning(self, 'Greška',
        "Bad user or password", QtGui.QMessageBox.Ok)

    def runIt(self):
        myprogram = Window()
        myprogram.showMaximized() #myprogram is

class Window(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)


if __name__=="__main__":
    program = QtGui.QApplication(sys.argv)
    myprogram = Window()
    if Login().exec_() == QtGui.QDialog.Accepted:
        sys.exit(program.exec_())