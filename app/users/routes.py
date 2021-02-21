from flask import render_template
from flask_login import login_required, current_user

from app.auth.utilities import get_profile_from_db
from app.models import User
from app.users import users
from app.users.forms import ModifyInformationForm


@users.route('/dashboard')
@login_required
def dashboard():
    if get_profile_from_db(current_user.get_id()).__class__ is User:
        return render_template('dashboard_user.html', title='Welcome to your profile')
    else:
        return render_template('dashboard_owner.html', title='Welcome to your profile')


@users.route('/modifyInfo')
@login_required
def modify_information():
    modifyInfoForm = ModifyInformationForm()
    return render_template('modify_information.html', title='Modify your information', form=modifyInfoForm)
