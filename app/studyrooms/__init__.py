from flask import Blueprint

studyrooms = Blueprint('studyrooms', __name__)

from app.studyrooms import routes
