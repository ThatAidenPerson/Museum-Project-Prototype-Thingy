from flask import Flask, render_template, url_for, request, redirect, session
from forms import LoginForm, HirerForm, InvoiceDetailsForm, DesignatedEvacuationPersonForm, OneOffBookingForm, RecurringBookingForm
from non_forms import login_users, create_db

import bcrypt
from datetime import datetime, date
import matplotlib.pyplot as plt
import base64, io

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

users = {}

class User(UserMixin):
    def __init__(self, user_id, username, password, admin):
        self.id = user_id
        self.username = username
        self.password = password
        self.admin = admin



@login_manager.user_loader
def load_user(user_id):
    engine = create_engine('sqlite:///database.db')
    with engine.connect() as conn:
        a, b, c, d = conn.execute(text(f'SELECT id, username, hash, admin FROM users WHERE id = {user_id}')).fetchone()
        return User(int(a), b, c, d)


@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        bytes = (form.password.data).encode('utf-8')
        user_id, username, password, admin, correct = login_users(form.identification.data, bytes)
        if user_id and correct == True:
            user = User(user_id, username, password, admin)
            users[user.id] = user
            login_user(user, remember=form.remember_user.data)
            print(f'User {user.username} logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form, error='The credentials you have entered is incorrect, please try again.')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/calendar', methods=['GET','POST'])
@login_required
def calendar():
    calendar_data = [
    {
        # General Hire Information
        "hire_name": "John Doe",
        "company_name": "Acme Corp",
        "address": "123 Main St, Anytown, UK",
        "hire_email": "johndoe@example.com",
        "hire_phone": "555-1234",
        "one_off_booking": True,  # This booking is a one-off

        "invoice_name": "John Doe",
        "invoice_address": "123 Main St, Anytown, UK",
        "invoice_email": "invoice@acmecorp.com",
        "invoice_phone": "555-5678",
        "evac_name": "Jane Doe",
        "evac_phone": "555-8765",

        # One-off booking details provided; recurring details set to N/A
        "one_date": "2025-06-20",
        "one_start": "14:00",
        "one_end": "16:00",
        "one_room": "Room 101",
        "one_extra_booking": False,
        "one_booking_type": "meeting",  # meeting, lecture, workshop, performance, class, or other
        "one_notes": "Initial one-off meeting",
        
        "reacurring_date": "N/A",
        "reacurring_start": "N/A",
        "reacurring_end": "N/A",
        "reacurring_pattern": "N/A",  # monthly or weekly
        "reacurring_end_date": "N/A",
        "reacurring_room": "N/A",
        "reacurring_booking_type": "N/A",
        "reacurring_notes": "N/A"
    },
    {
        # General Hire Information
        "hire_name": "Alice Smith",
        "company_name": "Beta Industries",
        "address": "456 Market St, Othertown, UK",
        "hire_email": "alice@betaindustries.com",
        "hire_phone": "555-4321",
        "one_off_booking": False,  # This booking is recurring

        "invoice_name": "Alice Smith",
        "invoice_address": "456 Market St, Othertown, UK",
        "invoice_email": "billing@betaindustries.com",
        "invoice_phone": "555-6789",
        "evac_name": "Bob Smith",
        "evac_phone": "555-9876",

        # One-off booking details set to N/A; recurring details provided
        "one_date": "N/A",
        "one_start": "N/A",
        "one_end": "N/A",
        "one_room": "N/A",
        "one_extra_booking": "N/A",
        "one_booking_type": "N/A",
        "one_notes": "N/A",
        
        "reacurring_date": "2025-06-01",  # start of recurring series
        "reacurring_start": "09:00",
        "reacurring_end": "11:00",
        "reacurring_pattern": "weekly",  # monthly or weekly
        "reacurring_end_date": "2025-12-31",
        "reacurring_room": "Conference Room A",
        "reacurring_booking_type": "workshop",
        "reacurring_notes": "Weekly recurring workshop session"
    }
]
    return render_template('calendar.html', calendar_data=calendar_data)

@app.route('/multi_booking', methods=['GET','POST'])
@login_required
def multi_booking():
    # Determine which step (stage) we are on via a query parameter (default to 1)
    step = int(request.args.get('step', 1))
    booking_data = session.get('booking_data', {})

    # Stage 1: Hirer Details form
    if step == 1:
        form = HirerForm()
        if form.validate_on_submit():
            booking_data['hirer'] = {
                'name': form.name.data,
                'company_name': form.company_name.data,
                'address': form.address.data,
                'email_address': form.email_address.data,
                'phone_number': form.phone_number.data,
                'one_off_booking': form.one_off_booking.data  # Value: 'one_off' or 'recurring'
            }
            session['booking_data'] = booking_data
            return redirect(url_for('multi_booking', step=2))
        return render_template('multi_booking.html', form=form, step=step)

    # Stage 2: Invoice Details form
    elif step == 2:
        form = InvoiceDetailsForm()
        if form.validate_on_submit():
            booking_data['invoice'] = {
                'name': form.name.data,
                'address': form.address.data,
                'email_address': form.email_address.data,
                'phone_number': form.phone_number.data,
            }
            session['booking_data'] = booking_data
            return redirect(url_for('multi_booking', step=3))
        return render_template('multi_booking.html', form=form, step=step)

    # Stage 3: Designated Evacuation Person form
    elif step == 3:
        form = DesignatedEvacuationPersonForm()
        if form.validate_on_submit():
            booking_data['evacuation'] = {
                'name': form.name.data,
                'contact': form.contact.data,
            }
            session['booking_data'] = booking_data
            return redirect(url_for('multi_booking', step=4))
        return render_template('multi_booking.html', form=form, step=step)

    # Stage 4: Booking Details form (one-off or recurring)
    elif step == 4:
        # Select the proper form based on the one_off_booking selection from stage 1
        booking_type = booking_data.get('hirer', {}).get('one_off_booking', 'one_off')
        if booking_type == 'one_off':
            form = OneOffBookingForm()
        else:
            form = RecurringBookingForm()

        if form.validate_on_submit():
            if booking_type == 'one_off':
                booking_data['booking_details'] = {
                    'date': form.date.data.strftime('%Y-%m-%d'),
                    'start_time': form.start_time.data.strftime('%H:%M'),
                    'end_time': form.end_time.data.strftime('%H:%M'),
                    'room': form.room.data,
                    'extra_booking': form.extra_booking.data,
                    'booking_type': form.booking_type.data,
                    'notes': form.notes.data,
                }
            else:
                booking_data['booking_details'] = {
                    'date': form.date.data.strftime('%Y-%m-%d'),
                    'start_time': form.start_time.data.strftime('%H:%M'),
                    'end_time': form.end_time.data.strftime('%H:%M'),
                    'recurring_pattern': form.recurring_pattern.data,
                    'end_date': form.end_date.data.strftime('%Y-%m-%d') if form.end_date.data else None,
                    'room': form.room.data,
                    'booking_type': form.booking_type.data,
                    'notes': form.notes.data,
                }
            session['booking_data'] = booking_data
            # At this point, all data has been collected.
            # You can now use booking_data to setup your SQL or process further.
            print("Final booking data:", booking_data)
            # Clear session data if needed.
            session.pop('booking_data', None)
            return redirect(url_for('dashboard'))
        return render_template('multi_booking.html', form=form, step=step)
    
    else:
        # If an invalid step is provided, reset the process.
        session.pop('booking_data', None)
        return redirect(url_for('multi_booking', step=1))

if __name__ == '__main__':
    create_db()
    app.run(debug=True)