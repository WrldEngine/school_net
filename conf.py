import os

config_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
	SECRET_KEY = 'some_secret'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///management.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAX_CONTENT_LENGTH = 1024 * 1024