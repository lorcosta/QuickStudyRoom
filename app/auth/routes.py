from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from wtforms import ValidationError

from app import db
from app.auth import auth
from app.auth.forms import SignUpForm, SignInForm, ConfirmationForm

# seems auth does not redirect correctly, main works but auth no
from app.auth.utilities import hash_psw, send_confirm_email, get_profile_from_db
from app.models import User, Owner


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    #check if user is authenticated
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
        #controllare credenziali per l'accesso
        login_user(get_profile_from_db(signInForm.email.data))
        # remember_me
        # forgot_password
        return redirect(url_for('main.dashboard'))
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
            return redirect(url_for('login'))
        except ValidationError:
            confirmationForm.code.errors.append('The code inserted is wrong, check your email.')
    return render_template('confirm.html', form=confirmationForm, title='Confirm your account')



