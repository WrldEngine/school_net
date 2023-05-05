from flask import Flask
from app.main_server import disp
from .database import db

from conf import config_dir
import os

def init_app():
	app = Flask(__name__)
	app.config.from_object('conf.BaseConfig')

	db.init_app(app)

	with app.test_request_context():
		db.create_all()

	app.register_blueprint(disp)

	return app