#coding=utf-8

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask.ext.script import Manager
from os import path
import os
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
manager = Manager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		f = request.files['file']
		if not f.filename.endswith('.csv'):
			return "不支持的文件格式，请上传csv文件。"
		basepath = path.abspath(path.dirname(__file__))
		fp = path.join(basepath, 'static/data', secure_filename(f.filename))
		f.save(fp)
		return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/get_result', methods=['GET'])
def get_result():
	data_path = '/static/data/'
	all_files = [i for i in os.listdir('./static/data/') if i.endswith('.csv')]
	raw_files = [i for i in os.listdir('./static/data/') if i.endswith('.csv') and not i.endswith('_m.csv') and not i.endswith('_pc.csv')]
	data_files = []
	for raw_csv in raw_files:
		data = [raw_csv, '-', '-']
		m_csv = raw_csv[:-4] + '_m.csv'
		pc_csv = raw_csv[:-4] + '_pc.csv'
		if m_csv in all_files:
			data[1] = m_csv
		if pc_csv in all_files:
			data[2] = pc_csv
		data_files.append(data)
	#data_files = [('word.csv', 'word-m.csv', 'word-pc.csv'),
	#				('test.csv', 'test-m.csv', 'test-pc.csv')]
	return render_template('result_table.html', data_path=data_path, data_files=data_files)


@manager.command
def dev():
	from livereload import Server
	live_server = Server(app.wsgi_app)
	live_server.watch('**/*.*')
	live_server.serve(open_url=False)


@manager.command
def asyn():
	from gevent import monkey
	from gevent.pywsgi import WSGIServer
	monkey.patch_all()
	http_server = WSGIServer(('', 5500), app)
	http_server.serve_forever()

if __name__ == '__main__':
	manager.run()
	#app.run(debug=True)
