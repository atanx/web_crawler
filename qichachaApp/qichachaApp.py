#!/usr/bin/env python
#coding=utf-8
import os
import sys
from qichacha import Qichacha
from PyQt4 import QtCore, QtGui, uic
qtLoginFile = "login.ui"
qtMainFile = "main_qichacha.ui"  # Enter file here.
Ui_LoginWindow, QtBaseClass = uic.loadUiType(qtLoginFile)
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainFile)


class FrmLogin(QtGui.QDialog, Ui_LoginWindow):
	def __init__(self):
		super(FrmLogin, self).__init__()
		self.setupUi(self)
		self.input_password.setEchoMode(QtGui.QLineEdit.Password)
		self.button_login.clicked.connect(self.doLogin)

	def doLogin(self):
		name = str(self.input_username.text())
		passwd = str(self.input_password.text())
		if name == "admin" and passwd == "admin":
			# self.runIt()
			self.accept()
		else:
			QtGui.QMessageBox.warning(self, u'警告',
										u"用户名或密码错误", QtGui.QMessageBox.Ok)

	def runIt(self):
		app = MyApp()
		app.showMaximized()  # myprogram is


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		# 属性
		self.Qichacha = Qichacha()
		# Callbacks
		self.button_login.clicked.connect(self.callback_login)
		self.button_crawl.clicked.connect(self.callback_crawl)
		self.text_edit.setPlainText(u"王健林\n")

	def initUI(self):
		pass

	def callback_login(self):
		# QtGui.QMessageBox.information(self, "info", os.getcwd())
		self.Qichacha.init_browser()

	def callback_crawl(self):
		names = self.get_name_list()
		for name in names:
			self.Qichacha.execute(name=name, max_pages=10)
		# QtGui.QMessageBox.information(self, 'info', '\n'.join(names))

	def get_name_list(self):
		names = self.text_edit.toPlainText()
		names = unicode(names).split()
		return names

	def set_name_list(self, names):
		name_str = '\n'.join(names)
		self.text_edit.setPlainText(name_str)

# 该类已废弃
class FrmSetting(QtGui.QWidget):
	def __init__(self):
		super(FrmSetting, self).__init__()
		self.initUI()

	def initUI(self):
		# 按钮
		btn_send = QtGui.QPushButton(u"发送", self)
		btn_attach = QtGui.QPushButton(u"添加附件", self)
		title = QtGui.QLabel(u'发件人')
		author = QtGui.QLabel(u'收件人')
		review = QtGui.QLabel(u'附件列表')

		fromEdit = QtGui.QLineEdit()
		toEdit = QtGui.QLineEdit()
		attachEdit = QtGui.QTextEdit()
		fromEdit.setText("from")
		toEdit.setText("to")
		self.fromEdit = fromEdit
		self.toEdit = toEdit
		self.attachEdit = attachEdit

		grid = QtGui.QGridLayout()
		grid.addWidget(title, 1, 0)
		grid.addWidget(fromEdit, 1, 1)
		grid.addWidget(author, 2, 0)
		grid.addWidget(toEdit, 2, 1)
		grid.addWidget(review, 3, 0)
		grid.addWidget(attachEdit, 3, 1, 5, 1)
		grid.addWidget(btn_attach, 8, 0)
		grid.addWidget(btn_send, 8, 1)
		self.setLayout(grid)

		self.setWindowTitle(u'推送工具')
		self.resize(500, 300)
		self.connect(btn_attach, QtCore.SIGNAL('clicked()'), self.attach)
		self.connect(btn_send, QtCore.SIGNAL('clicked()'), self.send)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

	def attach(self):
		import win32ui
		dlg = win32ui.CreateFileDialog(1)
		dlg.SetOFNInitialDir("C:")
		dlg.DoModal()
		f = dlg.GetPathName()
		f = f.decode('gbk')
		_old = str(self.attachEdit.toPlainText()).strip()
		_new = (_old + '\n' + f).strip()
		self.attachEdit.setText(_new)

	def send(self):
		FROM = str(self.fromEdit.text())
		TO = str(self.toEdit.text())
		message = u'推送文档'
		f = tuple(str(self.attachEdit.toPlainText()).split('\n'))
		# main.send(FROM, TO, message, subject=u"推送个人文档", attachments=f)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	if FrmLogin().exec_() == QtGui.QDialog.Accepted:
		window = MyApp()
		window.show()
		sys.exit(app.exec_())
	#window.show()
	#sys.exit(app.exec_())
