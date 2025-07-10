from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, RadioField, DateField, TimeField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Optional, DataRequired
from datetime import datetime


class LoginForm(FlaskForm):
    identification = StringField('Username or email')
    password = PasswordField('Password')
    remember_user = BooleanField('Remember me')

class HirerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    one_off_booking = RadioField('Booking Type', choices=[
        ('one_off', 'One Off Booking'),
        ('recurring', 'Recurring Booking')
    ], validators=[DataRequired()])

class InvoiceDetailsForm(FlaskForm):
    # Form 2: Invoice Details (Optional if same as hirer)
    name = StringField('Name', validators=[])
    address = StringField('Address', validators=[])
    email_address = StringField('Email Address', validators=[Email(), Optional()])
    phone_number = StringField('Phone Number', validators=[])

class DesignatedEvacuationPersonForm(FlaskForm):
    # Form 3: Designated Evacuation Person
    name = StringField('Name (optional)', validators=[Optional()])
    contact = StringField('Email or Phone (optional)', validators=[Optional()])

class OneOffBookingForm(FlaskForm):
    # Form 4: One Off Booking
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    room = SelectField('Selection of Room', choices=[
        ('teign', 'Teign Room'),
        ('roof', 'Roof Terrace')
    ], validators=[DataRequired()])
    extra_booking = SelectField('Is this an extra booking from a recurring booking?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[DataRequired()])
    booking_type = SelectField('Type of Booking', choices=[
        ('meeting', 'Meeting'),
        ('lecture', 'Lecture'),
        ('workshop', 'Workshop'),
        ('performance', 'Performance'),
        ('class', 'Class'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes/Needed Equipment (e.g., projector, sound system)', validators=[Optional()])

class RecurringBookingForm(FlaskForm):
    # Form 5: Recurring Booking
    date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    recurring_pattern = SelectField('Recurring Pattern', choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], validators=[Optional()])
    end_date = DateField('End Date (optional)', format='%Y-%m-%d', validators=[Optional()])
    room = SelectField('Selection of Room', choices=[
        ('teign', 'Teign Room'),
        ('roof', 'Roof Terrace')
    ], validators=[DataRequired()])
    booking_type = SelectField('Type of Booking', choices=[
        ('meeting', 'Meeting'),
        ('lecture', 'Lecture'),
        ('workshop', 'Workshop'),
        ('performance', 'Performance'),
        ('class', 'Class'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes/Needed Equipment', validators=[Optional()])

class UnavailableDatesForm(FlaskForm):
    # Form 6: Unavailable Dates
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    recurring_pattern = SelectField('Recurring Pattern', choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], validators=[Optional()])
    end_date = DateField('End Date (if applicable)', format='%Y-%m-%d', validators=[Optional()])
    reason = StringField('Reason for Unavailability', validators=[DataRequired()])