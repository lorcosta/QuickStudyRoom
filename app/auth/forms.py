from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from app import db
from app.models import User, Owner


class SignUpForm(FlaskForm):
    firstName = StringField('Name', validators=[DataRequired(message='You need to insert your firstname')], render_kw={'placeholder': 'Your firstname'})
    lastName = StringField('Surname', validators=[DataRequired(message='You need to insert your lastname')], render_kw={'placeholder': 'Your lastname'})
    email = StringField('Email', validators=[DataRequired(message='You need to insert your email'), Length(min=6, max=64), Email()], render_kw={'placeholder': 'Your email'})
    password = PasswordField('Password', validators=[DataRequired(message='You need to insert your password'), Length(min=8)], render_kw={'placeholder': 'Set your password'})
    confirmPassword = PasswordField('Confirm password', validators=[DataRequired(message='You need to confirm your password'), Length(min=8)], render_kw={'placeholder': 'Confirm your password'})
    cap_choices = [('', '--- Select CAP ---')] + [cap for cap in db.session.query(bind='cities').filter_by('CAP')]
    # 100% the line above is not correct, I want to have the list of the cap inside cap_choices and maybe this has to be done when rendering the form
    cap = SelectField('CAP', validators=[DataRequired(message='Select the CAP of your city')], render_kw={'placeholder': 'Set your CAP'}, choices=cap_choices)
    city_choices = [('', '--- Select City ---')] + [city for city in db.session.query(bind='cities').filter_by('Comune')]
    # 100% the line above is not correct, I want to have the list of the cities inside city_choices and maybe this has to be done when rendering the form, the cities needs to be selected from the cap
    city = SelectField('City', validators=[DataRequired(message='You need to insert your city')], render_kw={'placeholder': 'Set your city'})
    accept_terms = BooleanField('I accept all Terms and Condition agreement', validators=[DataRequired(message='You need to accept Terms and Condition')])
    submit = SubmitField('Register me!')

    def validate_username(self, username):
        if len(self.username.data) > 15:
            raise ValidationError('Choose a shorter username (max length: 15chars)')
        if User.query.filter_by(username=username.data).first() or Owner.query.filter_by(
                username=username.data).first():
            raise ValidationError('This username has been already taken. Choose a different one.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() or Owner.query.filter_by(email=email.data).first():
            raise ValidationError('This email address has been already taken. Choose a different one.')


class SignInForm(FlaskForm):#credential and password
    credential = StringField('Email', validators=[DataRequired(message='Insert your email or username')], render_kw={'placeholder': 'Your email or username'})
    password = PasswordField('Password', validators=[DataRequired(message='Insert your password to access')], render_kw={'placeholder': 'Your password'})
    submit = SubmitField('Log in!')
    remember_me = BooleanField('Remember me!')


class CreateStudyRoomForm(FlaskForm):
    name = StringField('Study Room Name', validators=[DataRequired(message='You need to insert the name of the study room')], render_kw={'placeholder': 'Your study room name'})
    phone_num = IntegerField('Phone number', validators=[DataRequired(message='You need to insert the reference number for the study room')], render_kw={'placeholder': 'Reference number for the study room'})
    address = StringField('Address', validators=[DataRequired(message='You need to insert the full address of the study room')], render_kw={'placeholder': 'Your study room\'s address'})
    services = TextAreaField('Services', render_kw={'placeholder': 'Describe the services offered in the study room'})
    total_seats = IntegerField('Total seats', validators=[DataRequired(message='You need to provide the total seats of the study room')], render_kw={'placeholder': 'Enter total available seats'})
