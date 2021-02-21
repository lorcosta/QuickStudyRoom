from flask import render_template, current_app
from flask_mail import Message

from app import pswManager, mail
from app.models import User, Owner


def hash_psw(psw):
    return pswManager.generate_password_hash(psw).decode('utf-8')


def verify_psw(psw, email):
    profile = get_profile_from_db(email=email)
    psw_hash = getattr(profile, 'password')
    return pswManager.check_password_hash(psw_hash, psw)


def send_confirm_email(destination_profile, confirmation_code):
    message = Message('Welcome to Quick Study Room! Confirm your account',
                      recipients=[destination_profile.email],
                      sender=current_app.config['MAIL_USERNAME'])
    message.body = render_template('email_template/email_confirmation.txt', name=destination_profile.name,
                                   surname=destination_profile.surname, email=destination_profile.email,
                                   code=confirmation_code)
    mail.send(message)


def send_reset_password_email(destination_profile, new_password):
    message = Message('Reset your Quick Study Room password',
                      recipients=[destination_profile.email],
                      sender=current_app.config['MAIL_USERNAME'])
    message.body = render_template('email_template/password_reset.txt', name= destination_profile.name, newPassword=new_password)
    mail.send(message)


def get_profile_from_db(email):
    if User.query.filter_by(email=email).first() is None:
        profile = Owner.query.filter_by(email=email).first()
    else:
        profile = User.query.filter_by(email=email).first()
    # profile = User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first()
    return profile


def is_user_confirmed(email):
    profile = get_profile_from_db(email)
    if profile.is_confirmed == 1:
        return True
    else:
        return False
