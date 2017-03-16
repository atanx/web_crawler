import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = True
	MYSQL_URL ='mysql://root:root@172.16.0.30/spider'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
							'sqlite:///' + os.path.join(basedir, 'data.db')
	ARTICLES_PER_PAGE = 10
	COMMENTS_PER_PAGE = 6
	SECRET_KEY = 'secret key to protect from csrf'
	WTF_CSRF_SECRET_KEY = 'random key for form'

	@staticmethod
	def init_app(app):
		pass
