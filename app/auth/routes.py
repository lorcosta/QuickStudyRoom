from flask import render_template

from app.auth import auth
from app.auth.forms import SignUpForm

# seems auth does not redirect correctly, main works but auth no
from app.auth.utilities import hash_psw
from app.models import User, Owner


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    signUpForm = SignUpForm()
    print 'before validate_on_submit'
    if signUpForm.validate_on_submit():
        if signUpForm.password.data == signUpForm.confirmPassword.data:
            if signUpForm.user_or_owner.data == 'user':
                newProfile = User(name=signUpForm.firstName.data,
                                  surname=signUpForm.lastName.data,
                                  email=signUpForm.email.data,
                                  password=hash_psw(signUpForm.password.data))
                print newProfile.email
            elif signUpForm.user_or_owner.data == 'owner':
                newProfile = Owner(name=signUpForm.firstName.data,
                                   surname=signUpForm.lastName.data,
                                   email=signUpForm.email.data,
                                   password=hash_psw(signUpForm.password.data))
                print newProfile.email
        else:
            print 'errore nella password'
            # change error message
            signUpForm.confirmPassword.errors(message='The password is not the same')
        # commit the newProfile on the database

    return render_template('signup.html', form=signUpForm)


