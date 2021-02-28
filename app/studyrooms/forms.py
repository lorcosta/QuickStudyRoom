from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, FileField, DateField, TimeField
from wtforms.validators import Length, DataRequired, ValidationError

from app.models import StudyRoom


class AddStudyroomForm(FlaskForm):
    name = StringField('Study Room Name', validators=[Length(min=3, max=30), DataRequired(message='You need to insert the study room name')], render_kw={'placeholder': 'Study Room Name'})
    city = StringField('City', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the city')], render_kw={'placeholder': 'City'})
    address = StringField('Address', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the address')], render_kw={'placeholder': 'Address'})
    nation = StringField('Nation', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the nation')], render_kw={'placeholder': 'Nation'})
    postal_code = StringField('Postal Code', validators=[DataRequired(message='You need to insert the postal code')], render_kw={'placeholder': 'Postal Code'})
    seats = IntegerField('Number of Seats', validators=[DataRequired(message='You need to insert the number of seats of the study room')], render_kw={'placeholder': 'Number of seats'})
    contact_mail = StringField('Mail Contact', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the mail to contact you for this study room')], render_kw={'placeholder': 'Mail Contact'})
    contact_phoneNumber = StringField('Phone number Contact', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the phone number to contact you for this study room')], render_kw={'placeholder': 'Phone number Contact'})
    toilette = BooleanField('Toilettes')
    vending_machines = BooleanField('Vending Machines')
    wi_fi = BooleanField('Wi-Fi')
    electrical_outlets = BooleanField('Electrical Outlets')
    printer = BooleanField('Printers')
    others = StringField('Others...', render_kw={'placeholder': 'Add your services not listed'})
    submit = SubmitField('Create Study Room')

    def validate_name(self, name):
        if StudyRoom.query.filter_by(name=name.data).first():
            raise ValidationError('This name has been already taken. Choose a different one.')


class ModifyStudyroomForm(FlaskForm):
    name = StringField('Study Room Name', validators=[Length(min=3, max=30),
                                                      DataRequired(message='You need to insert the study room name')],
                       render_kw={'placeholder': 'Study Room Name'})
    city = StringField('City', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the city')],
                       render_kw={'placeholder': 'City'})
    address = StringField('Address',
                          validators=[Length(min=2, max=30), DataRequired(message='You need to insert the address')],
                          render_kw={'placeholder': 'Address'})
    nation = StringField('Nation',
                         validators=[Length(min=2, max=30), DataRequired(message='You need to insert the nation')],
                         render_kw={'placeholder': 'Nation'})
    postal_code = StringField('Postal Code', validators=[DataRequired(message='You need to insert the postal code')],
                              render_kw={'placeholder': 'Postal Code'})
    seats = IntegerField('Number of Seats',
                         validators=[DataRequired(message='You need to insert the number of seats of the study room')],
                         render_kw={'placeholder': 'Number of seats'})
    mail_contact = StringField('Mail Contact', validators=[Length(min=2, max=30), DataRequired(
        message='You need to insert the mail to contact you for this study room')],
                               render_kw={'placeholder': 'Mail Contact'})
    phone_num = StringField('Phone number Contact', validators=[Length(min=2, max=30), DataRequired(
        message='You need to insert the phone number to contact you for this study room')],
                                      render_kw={'placeholder': 'Phone number Contact'})
    toilette = BooleanField('Toilettes')
    vending_machines = BooleanField('Vending Machines')
    wi_fi = BooleanField('Wi-Fi')
    electrical_outlets = BooleanField('Electrical Outlets')
    printer = BooleanField('Printers')
    others = StringField('Others...', render_kw={'placeholder': 'Add your services not listed'})
    submit_info = SubmitField('Modify Study Room')


class UploadPhotoForm(FlaskForm):
    file = FileField('Upload a photo for the Study Room', validators=[DataRequired()])
    upload = SubmitField('Upload')


class SlotAvailabilityForm(FlaskForm):
    # TODO we need to use correct timefield and think how to manage the times
    open_morning = StringField('Open Morning', validators=[DataRequired(message='Insert the hour the study room will be opened in the morning')])
    close_morning = StringField('Close Morning', validators=[DataRequired(message='Insert the hour the study room will be closed for lunch')])
    open_evening = StringField('Open evening', validators=[DataRequired(message='Insert the hour the study room will be opened after lunch')])
    close_evening = StringField('Close evening', validators=[DataRequired(message='Insert the hour the study room will be closed in the evenings')])

    monday = BooleanField('Monday')
    tuesday = BooleanField('Tuesday')
    wednesday = BooleanField('Wednesday')
    thursday = BooleanField('Thursday')
    friday = BooleanField('Friday')
    saturday = BooleanField('Saturday')
    sunday = BooleanField('Sunday')
    submit = SubmitField('Allow reservations on your Study Room')


class SearchStudyRoomForm(FlaskForm):
    city = StringField('City')
    postal_code = StringField('Postal Code')
    name = StringField('Name')
    date = StringField('Date')
    toilette = BooleanField('Toilettes')
    vending_machines = BooleanField('Vending Machines')
    wi_fi = BooleanField('Wi-Fi')
    electrical_outlets = BooleanField('Electrical Outlets')
    printer = BooleanField('Printers')
    submit = SubmitField('Search')
