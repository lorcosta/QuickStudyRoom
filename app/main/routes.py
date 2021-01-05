from datetime import datetime

from flask import render_template
from flask_login import current_user

from app import db
from app.main import main
from app.models import User


@main.before_app_request
def database_creation():
    db.create_all()
    #user_test = User(name='Lorenzo', surname='Costa', email='costalorenzo@mail.com',
                # dob=datetime(year=1998, month=5, day=21), city='Turin', password='test')
    #db.session.add(user_test)
    db.session.commit()


@main.route('/home')
def home():
    if current_user.is_anonymous:
        return render_template('template_homepage.html')
    return render_template('template_dashboard.html')


@main.route('/dashboard')
def dashboard():
    return render_template('template_dashboard.html')





