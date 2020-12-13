import os
from datetime import datetime, timedelta
from app import db


class SUPER_USER:
    username = db.Column(db.String(10), nullable=False, index=True, unique=True)
    email = db.Column(db.String, primary_key=True)
    # confirmed = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    # file_path = db.Column(db.String(20), unique=True)  # path to the directory where the files of the users are saved
    dob = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String)  # city and country
    password = db.Column(db.String(60), unique=False, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # set file path, create a directory with the primary key

    def set_file_path(self):
        if not self.email:
            os.chdir(os.getcwd()+'/app/static')
            if not os.path.exists(self.email):
                os.makedirs(self.email)


class User(db.Model, '''UserMixin''', SUPER_USER):
    __tablename__ = 'users'
    cc_number = db.Column(db.String)
    cc_exp = db.Column(db.DateTime)  # the day of expiration is always the last day of the month

    def __repr__(self):
        return 'User %r %r (%r)' % self.name, self.surname, self.email


class Owner(db.Model, '''UserMixin''', SUPER_USER):
    __tablename__ = 'owners'

    def __repr__(self):
        return 'Owner %r %r (%r)' % self.name, self.surname, self.email


class StudyRoom(db.Model):
    __tablename__ = 'studyRooms'
    id = db.Column(db.Integer, primary_key=True)
    owner_id_email = db.Column(db.String, db.ForeignKey('owners.email'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone_num = db.Column(db.String(20))
    address = db.Column(db.String, nullable=False)  # full address, street, city, country, zip code
    bookable = db.Column(db.Boolean, nullable=False, default=True)  # fast check if a studyRoom is bookable, default??
    # what default value is correct for bookable? We need to check continuously the number of seats
    services = db.Column()
    seats_booked = db.Column(db.Integer, nullable=False, default=0)
    seats_max = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Study Room num. %r, %r. Owner contact: %r' % self.id, self.name, self.owner_id_email


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email'), index=True, nullable=False)
    study_room = db.Column(db.Integer, db.ForeignKey('studyRooms.id'), index=True, nullable=False)
    start_datetime = db.Column(db.DateTime, default=datetime.now(), index=True, nullable=False)
    duration = timedelta(hours=1)
    end_datetime = db.Column(db.DateTime, default=datetime.now()+duration, index=True, nullable=False)

    def __repr__(self):
        return 'Reservation num. %r, user %r' % self.id, self.user
