import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.routes import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config.config import Config
import os
from dotenv import load_dotenv

# load env
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI_DEV")
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_COOKIE_SECURE'] = os.environ.get('JWT_COOKIE_SECURE')
app.config['JWT_TOKEN_LOCATION'] = os.environ.get('JWT_TOKEN_LOCATION')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=5)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)