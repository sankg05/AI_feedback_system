from flask import Flask
import os
from dotenv import load_dotenv
from app.init_db import init_db

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
flask_app = os.getenv('FLASK_APP')

with app.app_context():
    init_db()

from app import routes