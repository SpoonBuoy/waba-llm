from flask import Blueprint

# /api would be main blueprint
api = Blueprint('api', __name__)


chat = Blueprint('chat', __name__)
