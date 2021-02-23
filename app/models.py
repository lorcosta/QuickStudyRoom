import os, random, string
from datetime import datetime, timedelta
from random import randint

from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(email):
    profile = User.query.filter_by(email=email).first() or Owner.query.filter_by(email=email).first()
    return profile


class SuperUser(UserMixin):
    email = db.Column(db.String, primary_key=True, index=True, unique=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    # file_path = db.Column(db.String(20), unique=True)  # path to the directory where the files of the users are saved
    dob = db.Column(db.DateTime, nullable=True)
    city = db.Column(db.String)  # city and country
    password = db.Column(db.String(60), unique=False, nullable=False)
    confirmation_code = db.Column(db.Integer, nullable=True, unique=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # set file path, create a directory with the primary key

    def generate_confirmation_code(self):
        self.confirmation_code = randint(100000, 999999)

    def confirm_account(self):
        self.is_confirmed = True

    def set_file_path(self):
        if not self.email:
            os.chdir(os.getcwd() + '/app/static')
            if not os.path.exists(self.email):
                os.makedirs(self.email)

    def get_id(self):
        return self.email

    def get_type(self):
        if self.__class__ is User:
            return 'U'
        else:
            return 'O'


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email'), index=True, nullable=False)
    study_room_id = db.Column(db.Integer, db.ForeignKey('studyRooms.id'), index=True, nullable=False)
    start_datetime = db.Column(db.DateTime, index=True, nullable=False)
    # TODO change the datetime, it should be time of the reservation not now!!
    duration = timedelta(hours=1)
    end_datetime = db.Column(db.DateTime, default=datetime.now() + duration, index=True, nullable=False)

    def __repr__(self):
        return 'Reservation num. %r, user %r' % self.id, self.user


class User(db.Model, SuperUser):
    __tablename__ = 'users'
    cc_number = db.Column(db.String)
    cc_exp = db.Column(db.DateTime)  # the day of expiration is always the last day of the month
    reservations = db.relationship('Reservation', foreign_keys=[Reservation.user_email], backref=db.backref('user'))

    def __repr__(self):
        return 'User {} {} ({})'.format(self.name, self.surname, self.email)


class StudyRoom(db.Model):
    __tablename__ = 'studyRooms'
    id = db.Column(db.Integer, primary_key=True)
    owner_id_email = db.Column(db.String, db.ForeignKey('owners.email'))
    mail_contact = db.Column(db.String, nullable=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone_num = db.Column(db.String(20))
    address = db.Column(db.String, nullable=False)  # full address, street, city, country, zip code
    city = db.Column(db.String, nullable=False)
    nation = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    bookable = db.Column(db.Boolean, nullable=False, default=True)  # fast check if a studyRoom is bookable
    toilette = db.Column(db.Boolean, nullable=False, default=False)
    vending_machines = db.Column(db.Boolean, nullable=False, default=False)
    wi_fi = db.Column(db.Boolean, nullable=False, default=False)
    electrical_outlets = db.Column(db.Boolean, nullable=False, default=False)
    printer = db.Column(db.Boolean, nullable=False, default=False)
    others = db.Column(db.String)
    seats = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', foreign_keys=[Reservation.study_room_id],
                                   backref=db.backref('study_room_obj'))

    def __repr__(self):
        return 'Study Room num. %r, %r. Owner contact: %r' % self.id, self.name, self.owner_id_email


class Owner(db.Model, SuperUser):
    __tablename__ = 'owners'
    reservations = db.relationship('StudyRoom', foreign_keys=[StudyRoom.owner_id_email], backref=db.backref('owner'))

    def __repr__(self):
        return 'Owner %r %r (%r)' % self.name, self.surname, self.email
