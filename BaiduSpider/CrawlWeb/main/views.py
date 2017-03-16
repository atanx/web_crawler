#!/usr/bin/env python
# coding=utf-8

from . import main
from flask import render_template, request, redirect, url_for
import os
from os import path
from ..models import Site, CrawlTask
from .. import db
from .forms import AddSiteForm, SiteForm
import platform

ALLOWED_EXTENSIONS = set(['txt', 'csv'])
OS_TYPE = platform.system()

def allowd_file(filename):
	'Function to check wether filename is allowd or not'
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		site_id = int(request.form.get('group_names'))
		f = request.files['file']
		if allowd_file(f.filename):
			return u"不支持的文件格式，请上传csv文件。"
		basepath = path.abspath(path.dirname(__file__))
		fp = path.join(basepath, '../static/data', f.filename)
		f.save(fp)
		ct_list = CrawlTask.query.filter(CrawlTask.raw_file == f.filename).all()
		if len(ct_list) > 0:
			ct = ct_list[0]
			ct.site_id = site_id
		else:
			ct = CrawlTask(raw_file=f.filename, site_id=site_id)
		db.session.add(ct)
		db.session.commit()
		return redirect(url_for('main.index'))

	form = SiteForm()
	sites = Site.query.all()
	group_names = [(s.id, s.name) for s in sites]
	form.group_names.choices = [(0, u'--请选择--')] + group_names
	return render_template('index.html',
						    form=form,
							data_path=os.getcwd())


@main.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		id = int(request.form.get('group_names'))
		new_site_list = request.form.get('new_site_list')
		site = Site.query.filter(Site.id == id).first()
		site.site_list = new_site_list
		db.session.add(site)
		db.session.commit()

	form = SiteForm()
	add_site_form = AddSiteForm()
	sites = Site.query.all()
	group_names = [s.name for s in sites]
	group_names2 = [(s.id, s.name) for s in sites]
	form.group_names.choices = [(0, u'--请选择--')] + group_names2
	return render_template('settings.html',
							form=form,
							form2=add_site_form,
							group_names=group_names)


@main.route('/query_site_list', methods=['POST'])
def query_site_list():
	name = request.form.get('name', '')
	site = Site.query.filter(Site.name == name).first()
	if site:
		return site.site_list or ""
	else:
		return u""


@main.route('/add_group_name', methods=['POST'])
def add_group_name():
	group_name = request.form['group_name'].strip()
	if not group_name:
		return u"未指定新分组名。"
	s = Site.query.filter(Site.name == group_name).count()
	if s:
		return u"新增分组已存在！"
	else:
		s = Site(name=group_name)
		db.session.add(s)
		db.session.commit()
		return u"新增分组成功！"

@main.route('/help')
def help():
	return render_template('help.html')


@main.route('/get_result', methods=['GET'])
def get_result():
	STATIC_DATA_PATH = 'static/data/'
	FILE_PATH        = './CrawlWeb/static/data/'
	if OS_TYPE == 'Windows':
		all_files = [i.decode('gbk') for i in os.listdir(FILE_PATH)]
		all_csv_files = [i.decode('gbk') for i in os.listdir(FILE_PATH) if i.endswith('.csv') or i.endswith('.txt')]
		raw_csv_files = [i.decode('gbk') for i in os.listdir(FILE_PATH) if
						i.endswith('.csv') and not i.endswith('_m.csv') and not i.endswith('_pc.csv')]
	else:
		all_files = [i for i in os.listdir(FILE_PATH)]
		all_csv_files = [i for i in os.listdir(FILE_PATH) if
						i or i.endswith('.txt')]
		raw_csv_files = [i for i in os.listdir(FILE_PATH) if
						i.endswith('.csv') and not i.endswith('_m.csv') and not i.endswith('_pc.csv')]
	data_files = []
	for raw_csv in raw_csv_files:
		data = [raw_csv, '-', '-', '-', '-']
		m_csv = raw_csv[:-4] + '_m.csv'
		m_tmp = m_csv[:-3] + 'tmp'
		pc_csv = raw_csv[:-4] + '_pc.csv'
		pc_tmp = pc_csv[:-3] + 'tmp'
		if m_csv in all_csv_files:
			data[1] = m_csv
		if pc_csv in all_csv_files:
			data[2] = pc_csv
		data[3] = m_tmp in all_files
		data[4] = pc_tmp in all_files
		data_files.append(data)
	return render_template('result_table.html', data_path=STATIC_DATA_PATH, data_files=data_files)
