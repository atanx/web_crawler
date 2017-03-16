#!/usr/bin/env python
# coding=utf-8


from flask import Flask
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

db = SQLAlchemy()
nav = Nav()
nav.register_element('top', Navbar(u"爬虫系统",
							View(u'百度关键词', 'main.index'),
							View(u'设置', 'main.settings'),
							View(u'帮助', 'main.help'),
							))

bootstrap = Bootstrap()


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	Config.init_app(app)
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	nav.init_app(app)
	bootstrap.init_app(app)
	db.init_app(app)
	return app
