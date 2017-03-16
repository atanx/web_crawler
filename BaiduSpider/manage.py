#!/usr/bin/env python
#coding=utf-8

from flask.ext.script import Manager
from CrawlWeb import create_app, db, models
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
	from flask.ext.migrate import upgrade
	from CrawlWeb.models import Site
	upgrade()
	Site.seed()


@manager.command
def dev():
	from livereload import Server
	live_server = Server(app.wsgi_app)
	live_server.watch('**/*.*')
	live_server.serve(open_url=False, debug=True)


@manager.command
def asyn():
	from gevent import monkey
	from gevent.pywsgi import WSGIServer
	monkey.patch_all()
	http_server = WSGIServer(('0.0.0.0', 5500), app)
	http_server.serve_forever()


@manager.command
def default():
	app.run(host='0.0.0.0', port=5500, debug=True)


if __name__ == '__main__':
	manager.run()
