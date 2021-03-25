import string
import random

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app import db
from app.auth.utilities import hash_psw
from app.models import User, Owner


class SignUpForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(message='You need to insert your firstname')],
                            render_kw={'placeholder': 'Your firstname'})
    lastName = StringField('Surname', validators=[DataRequired(message='You need to insert your lastname')],
                           render_kw={'placeholder': 'Your surname'})
    email = StringField('Email',
                        validators=[DataRequired(message='You need to insert your email'), Length(min=6, max=64),
                                    Email()], render_kw={'placeholder': 'Your email'})
    password = PasswordField('Password',
                             validators=[DataRequired(message='You need to insert your password'), Length(min=8)],
                             render_kw={'placeholder': 'Set your password'})
    confirmPassword = PasswordField('Confirm password',
                                    validators=[DataRequired(message='You need to confirm your password'),
                                                Length(min=8), EqualTo('password')],
                                    render_kw={'placeholder': 'Confirm your password'})
    user_or_owner = RadioField('Select your profile type',
                               validators=[DataRequired(message='You need to select your profile type')],
                               choices=[('user', 'User'), ('owner', 'Owner')])
    accept_terms = BooleanField(' I accept all Terms and Condition agreement',
                                validators=[DataRequired(message='You need to accept Terms and Condition')])
    submit = SubmitField('Create account!')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() or Owner.query.filter_by(email=email.data).first():
            raise ValidationError('This email address has been already taken. Choose a different one.')


class SignInForm(FlaskForm):
    email = StringField('Email Form', validators=[DataRequired(message='Insert your email')],
                        render_kw={'placeholder': 'Your email or username'})
    password = PasswordField('Password', validators=[DataRequired(message='Insert your password to access')],
                             render_kw={'placeholder': 'Your password'})
    submit = SubmitField('Log in!')
    remember_me = BooleanField('Remember me!')

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first() and not Owner.query.filter_by(email=email.data).first():
            raise ValidationError('This email does not exist in the database. Insert your email')


class ConfirmationForm(FlaskForm):
    code = IntegerField('Confirmation Code', validators=[DataRequired(message='You need to insert your confirmation code received by email')], render_kw={'placeholder': 'Insert confirmation code'})
    submit = SubmitField('Confirm')

    def code_confirmation(self, code, email):
        if User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first():
            profile = User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first()
            if code == profile.confirmation_code:
                setattr(profile, 'is_confirmed', True)
                db.session.commit()
                return True
            else:
                raise ValidationError('Your confirmation code is wrong! Check your email.')


class ForgotPasswordForm(FlaskForm):
    email = email = StringField('Email Form', validators=[DataRequired(message='Insert your email')],
                        render_kw={'placeholder': 'Your email'})
    submit = SubmitField('Send password reset')

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first() and not Owner.query.filter_by(email=email.data).first():
            raise ValidationError('This email does not exist in the database. Insert the email used to sign up.')

    def password_reset(self, email):
        if User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first():
            profile = User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first()
            newPassword = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
            setattr(profile, 'password', hash_psw(newPassword))
            return newPassword
