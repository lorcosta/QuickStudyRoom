
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
    # user_test = User(name='Lorenzo', surname='Costa', email='costalorenzo@mail.com',
                # dob=datetime(year=1998, month=5, day=21), city='Turin', password='test')
    # db.session.add(user_test)
     db.session.commit()


@main.route('/')
def home():
    return render_template('template_homepage.html')


@main.route('/dashboard')
@login_required
def dashboard():
    if get_profile_from_db(current_user.get_id()).__class__ is User:
        return render_template('dashboard_user.html')
    else:
        return render_template('dashboard_owner.html')




