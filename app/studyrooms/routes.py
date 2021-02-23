from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Owner, StudyRoom
from app.studyrooms import studyrooms
from app.studyrooms.forms import AddStudyroomForm


@studyrooms.route('/addStudyroom', methods=['GET', 'POST'])
@login_required
def add_studyroom():
    if current_user.__class__ is Owner:
        addStudyroomForm = AddStudyroomForm()
        if addStudyroomForm.validate_on_submit():
            studyroom = StudyRoom(owner_id_email=current_user.get_id(),
                                  mail_contact=addStudyroomForm.contact_mail.data,
                                  name=addStudyroomForm.name.data,
                                  phone_num=addStudyroomForm.contact_phoneNumber.data,
                                  address=addStudyroomForm.address.data,
                                  city=addStudyroomForm.city.data,
                                  nation=addStudyroomForm.nation.data,
                                  postal_code=addStudyroomForm.nation.data,
                                  toilette=addStudyroomForm.toilette.data,
                                  vending_machines=addStudyroomForm.vending_machines.data,
                                  wi_fi=addStudyroomForm.wi_fi.data,
                                  electrical_outlets=addStudyroomForm.electrical_outlets.data,
                                  printer=addStudyroomForm.printer.data,
                                  others=addStudyroomForm.others.data,
                                  seats=addStudyroomForm.seats.data)
            db.session.add(studyroom)
            db.session.commit()
        return render_template('add_studyroom.html', title='Add a Study Room', form=addStudyroomForm)
    else:
        return redirect(url_for('errors.error_401'))
