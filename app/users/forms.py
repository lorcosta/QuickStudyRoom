from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.auth.utilities import verify_psw


class ModifyInformationForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(message='You need to insert your firstname')],
                            render_kw={'placeholder': 'Your firstname'})
    lastName = StringField('Surname', validators=[DataRequired(message='You need to insert your lastname')],
                           render_kw={'placeholder': 'Your surname'})
    submit = SubmitField('Save changes!')


class ModifyPasswordForm(FlaskForm):
    oldPassword = PasswordField('Old Password', validators=[DataRequired(message='You need to insert the old password')], render_kw={'placeholder': 'Insert your old password'})
    newPassword = PasswordField('New Password', validators=[Length(min=8), DataRequired(message='You need to insert the new password')], render_kw={'placeholder': 'Insert your new password'})
    confirmNewPassword = PasswordField('Repeat New Password', validators=[Length(min=8), EqualTo('newPassword'), DataRequired(message='You need to repeat the new password')],
                                       render_kw={'placeholder': 'Repeat your new password'})
    submit = SubmitField('Save changes!')

    def validate_oldPassword(self, oldPassword):
        if not verify_psw(email=current_user.get_id(), psw=oldPassword.data):
            raise ValidationError('The old password is wrong!')


class CreateStudyRoomForm(FlaskForm):
    name = StringField('Study Room Name',
                       validators=[DataRequired(message='You need to insert the name of the study room')],
                       render_kw={'placeholder': 'Your study room name'})
    phone_num = IntegerField('Phone number', validators=[
        DataRequired(message='You need to insert the reference number for the study room')],
                             render_kw={'placeholder': 'Reference number for the study room'})
    contact_mail = StringField('Email',
                        validators=[DataRequired(message='You need to insert the email'), Length(min=6, max=64),
                                    Email()], render_kw={'placeholder': 'StudyRoom email'})
    address = StringField('Address',
                          validators=[DataRequired(message='You need to insert the full address of the study room')],
                          render_kw={'placeholder': 'Your study room\'s address'})
    services = TextAreaField('Services', render_kw={'placeholder': 'Describe the services offered in the study room'})
    total_seats = IntegerField('Total seats', validators=[
        DataRequired(message='You need to provide the total seats of the study room')],
                               render_kw={'placeholder': 'Enter total available seats'})
    toilettes = BooleanField('Toilettes')
    vending_machines = BooleanField('Vending Machines')
    wi_fi = BooleanField('Wi-Fi')
    electrical_outlets = BooleanField('Electrical Outlets')
    printer = BooleanField('Printers')
    others = StringField('Others...', render_kw={'placeholder': 'Add your services not listed'})
    submit = SubmitField('Put the right name')
