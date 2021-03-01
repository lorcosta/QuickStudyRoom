import os

import flask
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app import db, photos
from app.auth.utilities import get_profile_from_db
from app.models import Owner, StudyRoom, User, Reservation
from app.studyrooms import studyrooms
from app.studyrooms.forms import AddStudyroomForm, ModifyStudyroomForm, UploadPhotoForm, SlotAvailabilityForm, \
    SearchStudyRoomForm
from app.studyrooms.utilities import get_studyroom, update_StudyroomInformation, allow_reservation, search_studyroom, \
    available_slots, get_slot


@studyrooms.route('/addStudyroom', methods=['GET', 'POST'])
@login_required
def add_studyroom():
    if current_user.get_type() is Owner:
        addStudyroomForm = AddStudyroomForm()
        if addStudyroomForm.validate_on_submit():
            studyroom = StudyRoom(owner_id_email=current_user.get_id(),
                                  mail_contact=addStudyroomForm.contact_mail.data,
                                  name=addStudyroomForm.name.data,
                                  phone_num=addStudyroomForm.contact_phoneNumber.data,
                                  address=addStudyroomForm.address.data,
                                  city=addStudyroomForm.city.data,
                                  nation=addStudyroomForm.nation.data,
                                  postal_code=addStudyroomForm.postal_code.data,
                                  toilette=addStudyroomForm.toilette.data,
                                  vending_machines=addStudyroomForm.vending_machines.data,
                                  wi_fi=addStudyroomForm.wi_fi.data,
                                  electrical_outlets=addStudyroomForm.electrical_outlets.data,
                                  printer=addStudyroomForm.printer.data,
                                  others=addStudyroomForm.others.data,
                                  seats=addStudyroomForm.seats.data)
            db.session.add(studyroom)
            db.session.commit()
            return redirect(url_for('users.dashboard'))
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
                                    name=modifyStudyroomForm.name.data,
                                    city=modifyStudyroomForm.city.data,
                                    address=modifyStudyroomForm.address.data,
                                    nation=modifyStudyroomForm.nation.data,
                                    postal_code=modifyStudyroomForm.postal_code.data,
                                    seats=modifyStudyroomForm.seats.data,
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
        # TODO remove the last condition and define the right procedure to block rerservations
        allow_reservation(studyroom)
        db.session.commit()
    if studyroom.bookable:
        slotAvailabilityForm.submit.label.text = 'Block reservations on your Study Room'
    return render_template('modify_studyroom.html', title='Modify your Study Room', studyroom=studyroom,
                           form=modifyStudyroomForm,
                           form_upload=uploadPhotoForm, form_slot=slotAvailabilityForm, fileList=fileList)


@studyrooms.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if current_user.get_type() is User:
        searchStudyroomForm = SearchStudyRoomForm()
        results = search_studyroom(city='', postal_code='', name='')
        if searchStudyroomForm.validate_on_submit():
            results = search_studyroom(city=searchStudyroomForm.city.data, postal_code=searchStudyroomForm.postal_code.data,
                                       name=searchStudyroomForm.name.data)
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
    # TODO do we show past slot? If a slot is this morning do we show it in the list?
    return render_template('book_studyroom.html', title='Book A Study Room', studyroom=studyroom, fileList=fileList, slots=slots)


@studyrooms.route('/book_studyroom/<slot_id>')
@login_required
def book_studyroom(slot_id):
    slot = get_slot(slot_id)
    # TODO controlli da fare:current_user ha gia una prenotazione effettuata per questo slot?
    reservation = Reservation(user_email=current_user.get_id(), slot_id=slot_id)
    if getattr(slot, 'available_seats') >= 0:
        setattr(slot, 'available_seats', slot.available_seats-1)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    else:
        flask.abort(401)
