import os
from datetime import datetime

import flask
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db, photos

from app.models import Owner, StudyRoom, User, Reservation, Slot
from app.studyrooms import studyrooms
from app.studyrooms.forms import AddStudyroomForm, ModifyStudyroomForm, UploadPhotoForm, SlotAvailabilityForm, \
    SearchStudyRoomForm
from app.studyrooms.utilities import get_studyroom, update_StudyroomInformation, allow_reservation, search_studyroom, \
    available_slots, get_slot, update_day_hours_price_seats


@studyrooms.route('/addStudyroom', methods=['GET', 'POST'])
@login_required
def add_studyroom():
    if current_user.get_type() is Owner:
        addStudyroomForm = AddStudyroomForm()
        if addStudyroomForm.validate_on_submit():
            studyroom = StudyRoom(owner_id_email=current_user.get_id(),
                                  mail_contact=addStudyroomForm.contact_mail.data,
                                  name=addStudyroomForm.name.data.upper(),
                                  phone_num=addStudyroomForm.contact_phoneNumber.data,
                                  address=addStudyroomForm.address.data,
                                  city=addStudyroomForm.city.data.upper(),
                                  nation=addStudyroomForm.nation.data,
                                  postal_code=addStudyroomForm.postal_code.data,
                                  toilette=addStudyroomForm.toilette.data,
                                  vending_machines=addStudyroomForm.vending_machines.data,
                                  wi_fi=addStudyroomForm.wi_fi.data,
                                  electrical_outlets=addStudyroomForm.electrical_outlets.data,
                                  printer=addStudyroomForm.printer.data,
                                  others=addStudyroomForm.others.data)
            db.session.add(studyroom)
            db.session.commit()
            return redirect(url_for('studyrooms.modify_studyroom', id=studyroom.id))
        return render_template('add_studyroom.html', title='Add a Study Room', form=addStudyroomForm)
    else:
        return flask.abort(401)


@studyrooms.route('/modifyStudyroom/<id>', methods=['GET', 'POST'])
@login_required
def modify_studyroom(id):
    modifyStudyroomForm = ModifyStudyroomForm()
    uploadPhotoForm = UploadPhotoForm()
    slotAvailabilityForm = SlotAvailabilityForm()
    studyroom = get_studyroom(id)

    if not os.path.exists(os.getcwd()+'/app/static/images/'+str(studyroom.id)):
        os.makedirs(os.getcwd()+'/app/static/images/'+str(studyroom.id))
    fileList = os.listdir(os.getcwd()+'/app/static/images/'+str(studyroom.id))
    fileList = [str(studyroom.id) + "/" + file for file in fileList]
    if uploadPhotoForm.upload.data and uploadPhotoForm.validate_on_submit():
        filename = photos.save(uploadPhotoForm.file.data, name=str(studyroom.name) + '.jpg',
                               folder=os.getcwd()+'/app/static/images/'+str(studyroom.id))
        fileList = os.listdir(os.getcwd() + '/app/static/images/' + str(studyroom.id))
        fileList = [str(studyroom.id) + "/" + file for file in fileList]
        flash("Photo saved successfully.", 'success')
    if modifyStudyroomForm.submit_info.data and modifyStudyroomForm.validate_on_submit():
        update_StudyroomInformation(studyroom=studyroom,
                                    name=modifyStudyroomForm.name.data.upper(),
                                    city=modifyStudyroomForm.city.data.upper(),
                                    address=modifyStudyroomForm.address.data,
                                    nation=modifyStudyroomForm.nation.data,
                                    postal_code=modifyStudyroomForm.postal_code.data,
                                    mail_contact=modifyStudyroomForm.mail_contact.data,
                                    phone_num=modifyStudyroomForm.phone_num.data,
                                    toilette=modifyStudyroomForm.toilette.data,
                                    vending_machines=modifyStudyroomForm.vending_machines.data,
                                    wi_fi=modifyStudyroomForm.wi_fi.data,
                                    electrical_outlets=modifyStudyroomForm.electrical_outlets.data,
                                    printer=modifyStudyroomForm.printer.data,
                                    others=modifyStudyroomForm.others.data)
        db.session.commit()
    if slotAvailabilityForm.submit.data and slotAvailabilityForm.validate_on_submit() and not studyroom.bookable:
        update_day_hours_price_seats(studyroom=studyroom, form=slotAvailabilityForm)
        allow_reservation(studyroom)
        db.session.commit()
    if studyroom.bookable:
        slotAvailabilityForm.submit.label.text = 'This Study Room is already available'
    return render_template('modify_studyroom.html', title='Modify your Study Room', studyroom=studyroom,
                           form=modifyStudyroomForm,
                           form_upload=uploadPhotoForm, form_slot=slotAvailabilityForm, fileList=fileList)


@studyrooms.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if current_user.get_type() is User:
        searchStudyroomForm = SearchStudyRoomForm()
        results = search_studyroom(city='', postal_code='', name='', date=None, toilette=False, wi_fi=False, electrical_outlets=False, printer=False, vending_machines=False)
        if searchStudyroomForm.validate_on_submit():
            results = search_studyroom(city=searchStudyroomForm.city.data.upper(), postal_code=searchStudyroomForm.postal_code.data,
                                       name=searchStudyroomForm.name.data.upper(), date=searchStudyroomForm.date.data, toilette=searchStudyroomForm.toilette.data,
                                       wi_fi=searchStudyroomForm.wi_fi.data, electrical_outlets=searchStudyroomForm.electrical_outlets.data, printer=searchStudyroomForm.printer.data,
                                       vending_machines=searchStudyroomForm.vending_machines.data)
        return render_template('search_studyroom.html', title='Search a Study Room', form=searchStudyroomForm, results=results)
    else:
        return flask.abort(401)


@studyrooms.route('/view_availability/<id>', methods=['GET', 'POST'])
@login_required
def view_availability(id):
    studyroom = get_studyroom(id)
    fileList = os.listdir(os.getcwd() + '/app/static/images/' + str(studyroom.id))
    fileList = [str(studyroom.id) + "/" + file for file in fileList]
    slots = available_slots(studyroom)
    return render_template('view_availability.html', title='Book A Study Room', studyroom=studyroom, fileList=fileList, slots=slots)


@studyrooms.route('/book_studyroom/<slot_id>')
@login_required
def book_studyroom(slot_id):
    slot = get_slot(slot_id)
    existing_reservation = False
    reservations = Reservation.query.filter_by(user_email=current_user.get_id()).all()
    for reservation in reservations:
        reservation_slot = get_slot(reservation.slot_id)
        if reservation_slot.date == slot.date and reservation_slot.morning == slot.morning:
            existing_reservation = True
            break
    if slot.morning:
        time = StudyRoom.query.filter_by(id=slot.studyroom_id).first().close_morning
        close = datetime(year=slot.date.year, month=slot.date.month, day=slot.date.day,
                         hour=time.hour, minute=time.minute)
    else:
        time = StudyRoom.query.filter_by(id=slot.studyroom_id).first().close_evening
        close = datetime(year=slot.date.year, month=slot.date.month, day=slot.date.day,
                         hour=time.hour, minute=time.minute)
    if slot.available_seats > 0 and not existing_reservation and datetime.utcnow() < close:
        reservation = Reservation(user_email=current_user.get_id(), slot_id=slot_id)
        setattr(slot, 'available_seats', slot.available_seats-1)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    else:
        flash('You can\'t reserve this study room: there are not available seats or you already have a reservation or the time is over.', 'error')
        return redirect(url_for('studyrooms.view_availability', id=slot.studyroom_id))


@studyrooms.route('/delete_reservation/<reservation_id>')
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if reservation is not None and current_user.get_id() == reservation.user_email:
        slot = Slot.query.filter_by(id=reservation.slot_id).first()
        db.session.delete(reservation)
        setattr(slot, 'available_seats', slot.available_seats+1)
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    else:
        flask.abort(401)


@studyrooms.route('/view_reservations/<studyroom_id>')
@login_required
def view_reservations(studyroom_id):
    studyroom = get_studyroom(studyroom_id)
    slots = available_slots(studyroom)
    return render_template('view_reservations.html', title='View Reservations', slots=slots, studyroom=studyroom)
