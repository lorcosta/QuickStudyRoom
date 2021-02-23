from app.auth.utilities import verify_psw, hash_psw


def update_information(name, lastName, profile):
    setattr(profile, 'name', name)
    setattr(profile, 'surname', lastName)


def update_password(newPassword, profile):
    setattr(profile, 'password', hash_psw(newPassword))
