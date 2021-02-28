import os
from datetime import time
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

    def get_id(self):
        return self.email

    def get_type(self):
        return self.__class__

    def get_type_str(self):
        if self.__class__ is User:
            return 'User'
        else:
            return 'Owner'


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email'))
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'))


class User(db.Model, SuperUser):
    __tablename__ = 'users'
    cc_number = db.Column(db.String)
    cc_exp = db.Column(db.DateTime)  # the day of expiration is always the last day of the month
    reservations = db.relationship('Reservation', foreign_keys=[Reservation.user_email], backref=db.backref('user'))

    def __repr__(self):
        return 'User {} {} ({})'.format(self.name, self.surname, self.email)


class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    morning = db.Column(db.Boolean, nullable=False)
    afternoon = db.Column(db.Boolean, nullable=False)
    studyroom_id = db.Column(db.Integer, db.ForeignKey('studyRooms.id'))
    reservations = db.relationship('Reservation', foreign_keys=[Reservation.slot_id], backref=db.backref('slot'))
    available_seats = db.Column(db.Integer)

    def __repr__(self):
        return 'Reservation num. %r, user %r' % self.id, self.user


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
    bookable = db.Column(db.Boolean, nullable=False, default=False)  # fast check if a studyRoom is bookable
    toilette = db.Column(db.Boolean, nullable=False, default=False)
    vending_machines = db.Column(db.Boolean, nullable=False, default=False)
    wi_fi = db.Column(db.Boolean, nullable=False, default=False)
    electrical_outlets = db.Column(db.Boolean, nullable=False, default=False)
    printer = db.Column(db.Boolean, nullable=False, default=False)
    others = db.Column(db.String)
    seats = db.Column(db.Integer, nullable=False)
    open_morning = db.Column(db.Time, default=time(hour=8, minute=0))
    close_morning = db.Column(db.Time, default=time(hour=13, minute=0))
    open_evening = db.Column(db.Time, default=time(hour=14, minute=0))
    close_evening = db.Column(db.Time, default=time(hour=20, minute=0))
    monday = db.Column(db.Boolean, nullable=False, default=True)  # True=open
    tuesday = db.Column(db.Boolean, nullable=False, default=True)
    wednesday = db.Column(db.Boolean, nullable=False, default=True)
    thursday = db.Column(db.Boolean, nullable=False, default=True)
    friday = db.Column(db.Boolean, nullable=False, default=True)
    saturday = db.Column(db.Boolean, nullable=False, default=True)
    sunday = db.Column(db.Boolean, nullable=False, default=False)
    slots = db.relationship('Slot', foreign_keys=[Slot.studyroom_id], backref=db.backref('studyRoom'))
    # TODO add photos??

    def set_file_path(self):
        if not self.id:
            os.chdir(os.getcwd() + '/app/static')
            if not os.path.exists(str(self.id)):
                os.makedirs(str(self.id))
    # def __repr__(self):
        # return 'Study Room num. %r, %r. Owner contact: %r' % self.id, self.name, self.owner_id_email


class Owner(db.Model, SuperUser):
    __tablename__ = 'owners'
    studyrooms = db.relationship('StudyRoom', foreign_keys=[StudyRoom.owner_id_email], backref=db.backref('owner'))

    def __repr__(self):
        return 'Owner %r %r (%r)' % self.name, self.surname, self.email
