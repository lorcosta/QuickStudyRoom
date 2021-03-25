from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from wtforms import ValidationError

from app import db
from app.auth import auth
from app.auth.forms import SignUpForm, SignInForm, ConfirmationForm, ForgotPasswordForm

from app.auth.utilities import hash_psw, send_confirm_email, get_profile_from_db, verify_psw, is_user_confirmed, \
    send_reset_password_email
from app.models import User, Owner


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        if signUpForm.user_or_owner.data == 'user':
            newProfile = User(name=signUpForm.firstName.data,
                              surname=signUpForm.lastName.data,
                              email=signUpForm.email.data,
                              password=hash_psw(signUpForm.password.data))
        elif signUpForm.user_or_owner.data == 'owner':
            newProfile = Owner(name=signUpForm.firstName.data,
                               surname=signUpForm.lastName.data,
                               email=signUpForm.email.data,
                               password=hash_psw(signUpForm.password.data))
        newProfile.generate_confirmation_code()
        db.session.add(newProfile)
        db.session.commit()
        send_confirm_email(destination_profile=newProfile, confirmation_code=newProfile.confirmation_code)
        return redirect(url_for('auth.confirm', email=newProfile.email))
    return render_template('signup.html', form=signUpForm, title='Sign Up')


@auth.route('/signin',  methods=['GET', 'POST'])
def sign_in():
    signInForm = SignInForm()
    if signInForm.validate_on_submit():
        if verify_psw(psw=signInForm.password.data, email=signInForm.email.data):
            if is_user_confirmed(email=signInForm.email.data):
                login_user(get_profile_from_db(signInForm.email.data))
                return redirect(url_for('users.dashboard'))
            else:
                signInForm.password.errors.append('Your profile is not yet verified! Check your email and follow instructions')
        else:
            signInForm.password.errors.append('Wrong password!')
    return render_template('signin.html', form=signInForm, title='Sign In')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/confirm_account/<email>', methods=['GET', 'POST'])
def confirm(email):
    confirmationForm = ConfirmationForm()
    if confirmationForm.validate_on_submit():
        try:
            confirmationForm.code_confirmation(email=email, code=confirmationForm.code.data)
            # return redirect(url_for('main.dashboard'))
            return redirect(url_for('auth.sign_in'))
        except ValidationError:
            confirmationForm.code.errors.append('The code inserted is wrong, check your email.')
    return render_template('confirm.html', form=confirmationForm, title='Confirm your account')


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgotPasswordForm = ForgotPasswordForm()
    if forgotPasswordForm.validate_on_submit():
        profile = get_profile_from_db(forgotPasswordForm.email.data)
        newPassword = forgotPasswordForm.password_reset(email=profile.email)
        send_reset_password_email(destination_profile=profile, new_password=newPassword)
        db.session.commit()
        return redirect(url_for('auth.sign_in'))
    return render_template('forgot_password.html', form=forgotPasswordForm, title='Reset your password')
