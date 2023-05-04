from flask import Flask
from .database import db
from app.main_server import disp

def init_app():
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///management.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SECRET_KEY'] = 'some_secret'
	app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

	db.init_app(app)

	with app.test_request_context():
		db.create_all()

	app.register_blueprint(disp)

	return app