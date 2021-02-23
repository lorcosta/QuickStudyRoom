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
    # email = StringField('Email',
                        #validators=[DataRequired(message='You need to insert your email'), Length(min=6, max=64),
                                    #Email()], render_kw={'placeholder': 'Your email'})
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
    # cap_choices = [('', '--- Select CAP ---')] + [cap for cap in db.session.query(bind='cities').filter_by('CAP')]
    # 100% the line above is not correct, I want to have the list of the cap inside cap_choices and maybe this has to be done when rendering the form
    # cap = SelectField('CAP', validators=[DataRequired(message='Select the CAP of your city')], render_kw={'placeholder': 'Set your CAP'}, choices=cap_choices)
    # city_choices = [('', '--- Select City ---')] + [city for city in db.session.query(bind='cities').filter_by('Comune')]
    # 100% the line above is not correct, I want to have the list of the cities inside city_choices and maybe this has to be done when rendering the form, the cities needs to be selected from the cap
    # city = SelectField('City', validators=[DataRequired(message='You need to insert your city')], render_kw={'placeholder': 'Set your city'})
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
