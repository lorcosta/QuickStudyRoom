from flask import render_template

from app.auth import auth
from app.auth.forms import SignUpForm


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        pass
    return render_template('signup.html', form=signUpForm)
