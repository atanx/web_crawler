#!/usr/bin/env python
#coding=utf-8
import os
import sys
from taobao import Taobao
from PyQt4 import QtCore, QtGui, uic
import traceback
import time
import base64
import os

qtLoginFile = "login.ui"
qtMainFile = "main_taobao2.ui"  # Enter file here.
Ui_LoginWindow, QtBaseClass = uic.loadUiType(qtLoginFile)
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainFile)

username = ''

class FrmLogin(QtGui.QDialog, Ui_LoginWindow):
	def __init__(self):
		super(FrmLogin, self).__init__()
		self.setupUi(self)
		self.input_password.setEchoMode(QtGui.QLineEdit.Password)
		self.button_login.clicked.connect(self.doLogin)
		self.button_cancel.clicked.connect(self.doCancel)

	def doLogin(self):
		name = str(self.input_username.text())
		passwd = str(self.input_password.text())
		if name == "admin" and passwd == "admin":
			# self.runIt()
			self.accept()
		elif name == 'trial' and passwd == 'trial':
			if not os.path.exists('trial_license.dat'):
				QtGui.QMessageBox.information(self,
											u'提示',
											u"您没有被授权试用，使用请联系作者：QQ1260413896",
											QtGui.QMessageBox.Ok)
			else:
				end_time_encode = open('trial_license.dat').read()
				end_time_decode = base64.b64decode(end_time_encode)
				end_time = time.strptime(end_time_decode, '%Y-%m-%d %H:%M:%S')
				if end_time < time.localtime():
					QtGui.QMessageBox.warning(self,
											u'警告',
											u"试用已于%s过期，请联系作者：QQ1260413896。"%end_time_decode,
											QtGui.QMessageBox.Ok)
				else:
					QtGui.QMessageBox.information(self,
												u'提示',
												u"试用即将于%s过期，继续使用请联系作者：QQ1260413896"%end_time_decode,
												QtGui.QMessageBox.Ok)
					self.accept()
		else:
			QtGui.QMessageBox.warning(self, u'警告',
										u"用户名或密码错误", QtGui.QMessageBox.Ok)
	def doCancel(self):
		self.close()

	def runIt(self):
		app = MyApp()
		app.showMaximized()  # myprogram is


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		# 属性
		self.taobao = Taobao()
		# Callbacks
		self.button_login.clicked.connect(self.btn_browser_clicked)
		self.button_crawl.clicked.connect(self.btn_crawl_clicked)
		self.lineEdit_titleExclued.textEdited.connect(self.set_para)
		self.spinBox.valueChanged.connect(self.set_para)
		self.spinBox_delay.valueChanged.connect(self.set_para)
		self.spinBox_minViewer.valueChanged.connect(self.set_para)
		self.spinBox_maxViewer.valueChanged.connect(self.set_para)
		self.action.triggered.connect(self.about)
		self.action_help.triggered.connect(self.show_help)
		self.action_update.triggered.connect(self.show_update)
		self.para = dict()
		self.set_para()

		# QtGui.QMessageBox.information(self,'aaa',str(self.spinBox.value()))

	def initUI(self):
		pass

	def btn_browser_clicked(self):
		# QtGui.QMessageBox.information(self, "info", os.getcwd())
		self.taobao.init_browser()

	def btn_crawl_clicked(self):
		if self.taobao.chrome is None:
			QtGui.QMessageBox.warning(self, u"警告", u"你尚未启动浏览器!")
			return None
		try:
			self.taobao.execute(**self.para)
			QtGui.QMessageBox.information(self, u'提示', u"恭喜，任务已完成！")
		except Exception,e:
			traceback.print_exc(file='err.log')
			QtGui.QMessageBox.warning(self, u"警告", u"抓取出错！请重试！")


	def set_para(self):
		page_num = self.spinBox.value()
		delay = self.spinBox_delay.value()
		min_viewer = self.spinBox_minViewer.value()
		max_viewer = self.spinBox_maxViewer.value()
		title_exclued = self.lineEdit_titleExclued.text()
		title_exclued = unicode(title_exclued)
		title_exclued = [i.strip() for i in title_exclued.split(u' ') if i.strip()]
		title_exclued = list(set(title_exclued))
		para = {'page_num': page_num,
				'delay': delay,
				'limits': {
					'min_viewer': min_viewer,
					'max_viewer': max_viewer,
					'title_exclued': title_exclued}
			  }
		self.para = para
		#QtGui.QMessageBox.information(self, u"关于", str(para))

	def about(self):
		about_message = u"""
本软件用于抓取淘宝商品。
作者：沃富仁波切 qq:1260413896
		"""
		QtGui.QMessageBox.information(self, u"关于", about_message)

	def show_help(self):
		help_message = u"""
1.使用前请安装chrome浏览器及相应版本的chromedriver。
2.在设置选项卡设置爬取参数，在爬取选项卡进行数据抓取。
		"""
		QtGui.QMessageBox.information(self, u"关于", help_message)

	def show_update(self):
		update_message = u"""
		本软件暂不支持在线升级功能。
		若遇到淘宝系统升级导致数据无法抓取，
		请联系客服qq1260413896咨询付费升级。
				"""
		QtGui.QMessageBox.information(self, u"升级", update_message)
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	if FrmLogin().exec_() == QtGui.QDialog.Accepted:
		window = MyApp()
		window.show()
		sys.exit(app.exec_())
	# window.show()
	# sys.exit(app.exec_())
