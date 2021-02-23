from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired


class AddStudyroomForm(FlaskForm):
    name = StringField('Study Room Name', validators=[Length(min=3, max=30), DataRequired(message='You need to insert the study room name')], render_kw={'placeholder': 'Study Room Name'})
    city = StringField('City', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the city')], render_kw={'placeholder': 'City'})
    address = StringField('Address', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the address')], render_kw={'placeholder': 'Address'})
    nation = StringField('Nation', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the nation')], render_kw={'placeholder': 'Nation'})
    postal_code = StringField('Postal Code', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the postal code')], render_kw={'placeholder': 'Postal Code'})
    seats = IntegerField('Number of Seats', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the number of seats of the study room')], render_kw={'placeholder': 'Number of seats'})
    contact_mail = StringField('Mail Contact', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the mail to contact you for this study room')], render_kw={'placeholder': 'Mail Contact'})
    contact_phoneNumber = StringField('Phone number Contact', validators=[Length(min=2, max=30), DataRequired(message='You need to insert the phone number to contact you fot this study room')], render_kw={'placeholder': 'Phone number Contact'})
    toilette = BooleanField('Toilettes')
    vending_machines = BooleanField('Vending Machines')
    wi_fi = BooleanField('Wi-Fi')
    electrical_outlets = BooleanField('Electrical Outlets')
    printer = BooleanField('Printers')
    others = StringField('Others...', render_kw={'placeholder': 'Add your services not listed'})
    submit = SubmitField('Put the right name')
