
from datetime import datetime

from flask import render_template, current_app
from flask_login import current_user, login_required
from flask_mail import Message

from app import db, mail
from app.auth.utilities import get_profile_from_db
from app.main import main
from app.models import User


@main.before_app_request
def database_creation():
    db.create_all()
    db.session.commit()


@main.route('/')
@main.route('/home')
def home():
    return render_template('homepage.html')
