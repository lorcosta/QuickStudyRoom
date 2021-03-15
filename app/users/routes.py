from datetime import datetime

from flask import render_template, flash
from flask_login import login_required, current_user

from app import db
from app.auth.utilities import get_profile_from_db
from app.models import User, StudyRoom, Reservation, Slot
from app.users import users
from app.users.forms import ModifyInformationForm, ModifyPasswordForm
from app.users.utilities import update_information, update_password, sort_by_date


class Studyroom(object):
    pass


@users.route('/dashboard')
@login_required
def dashboard():
    if current_user.get_type() is User:
        reservations = Reservation.query.filter_by(user_email=current_user.get_id()).all()
        informations = {}
        slots = Slot.query
        for reservation in reservations:
            slot = slots.filter(Slot.id == reservation.slot_id, Slot.date >= datetime.utcnow().date()).first()
            if slot is not None:
                if slot.morning:
                    time = StudyRoom.query.filter_by(id=slot.studyroom_id).first().close_morning
                    close = datetime(year=slot.date.year, month=slot.date.month, day=slot.date.day,
                                     hour=time.hour, minute=time.minute)
                else:
                    time = StudyRoom.query.filter_by(id=slot.studyroom_id).first().close_evening
                    close = datetime(year=slot.date.year, month=slot.date.month, day=slot.date.day,
                                     hour=time.hour, minute=time.minute)
                if datetime.utcnow() < close:
                    studyroom = StudyRoom.query.filter_by(id=slot.studyroom_id).first()
                    informations.update({reservation: [slot, studyroom]})

                    ordered_reservations = sort_by_date(informations)
                    print ordered_reservations
                    print informations.keys()
        return render_template('dashboard_user.html', title='Welcome to your profile', informations=informations, ordered_reservations=ordered_reservations)
    else:
        studyrooms = StudyRoom.query.filter_by(owner_id_email=current_user.get_id()).all()
        return render_template('dashboard_owner.html', title='Welcome to your profile', studyrooms=studyrooms)


@users.route('/modifyInfo', methods=['GET', 'POST'])
@login_required
def modify_information():
    modifyInfoForm = ModifyInformationForm()
    if modifyInfoForm.validate_on_submit():
        update_information(name=modifyInfoForm.name.data, lastName=modifyInfoForm.lastName.data, profile=current_user)
        db.session.commit()
    return render_template('modify_information.html', title='Modify your information', form=modifyInfoForm)


@users.route('/modifyPassword', methods=['GET', 'POST'])
@login_required
def modify_password():
    modifyPasswordForm = ModifyPasswordForm()
    if modifyPasswordForm.validate_on_submit():
        update_password(newPassword=modifyPasswordForm.newPassword.data, profile=current_user)
        db.session.commit()
        flash('Password succesfully changed', 'success')
    return render_template('modify_password.html', title='Modify your information', form=modifyPasswordForm)
