from flask import Blueprint

users = Blueprint('users', __name__)

from app.main import routes
