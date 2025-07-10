from sqlalchemy import create_engine, text
import bcrypt
import base64, io

def create_db():
    engine = create_engine('sqlite:///database.db')
    with engine.connect() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, hash TEXT, admin BOOLEAN)'))

def existing_user(account):
    engine = create_engine('sqlite:///database.db')
    exists = []
    for x in ['username', 'email', 'phone']:
        with engine.connect() as conn:
            result = conn.execute(text(f'SELECT username FROM users WHERE {x} = "{account[x]}"')).fetchone()
            if result:
                exists.append(x)
            else:
                pass
    return exists


def add_user(account):
    engine = create_engine('sqlite:///database.db')
    with engine.connect() as conn:
        conn.execute(text(f'INSERT INTO users (username, email, phone, first_name, last_name, hash, accept_tos, admin) VALUES (:username, :email, :phone, :first_name, :last_name, :hash, :accept_tos, :admin)'), account)
        conn.commit()

def login_users(identification, password):
    engine = create_engine('sqlite:///database.db')
    with engine.connect() as conn:
        try:
            user_id, username, hashed, admin = conn.execute(text(f'SELECT id, username, hash, admin FROM users WHERE username = "{identification}"')).fetchone()
            print(f'User ID: {user_id}, Username: {username}, Admin: {admin}, Hashed Password:{hashed}')
            result = True
        except TypeError:
            result = None
            print("User not found or invalid credentials.")
            
        finally:
            if result:
                return user_id, username, hashed, admin, True
            else:
                return None, None, None, None, False
            
"""
def check_bookings(user_id):
    engine = create_engine('sqlite:///database.db')
    bookings = []
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT * FROM booking WHERE id = {user_id}')).fetchall()
        for x in result:
            if x[2] == 0: 
                booking = {
                    'booking_number': x[0],
                    'user_id': x[1],
                    'booking_type': 'Virtual',
                    'address': x[3],
                    'post_code': x[4],
                    'city': x[5],
                    'county': x[6],
                    'date': x[7],
                    'time': x[8],
                    'subject': x[9],
                    'additional_info': x[10],
                    'assigned_staff': x[11]
                }
                bookings.append(booking)

            elif x[2] == 1:
                booking = {
                    'booking_number': x[0],
                    'user_id': x[1],
                    'booking_type': 'In Person',
                    'address': x[3],
                    'post_code': x[4],
                    'city': x[5],
                    'county': x[6],
                    'date': x[7],
                    'time': x[8],
                    'subject': x[9],
                    'additional_info': x[10],
                    'assigned_staff': x[11]
                }
                bookings.append(booking)

        return bookings"""
    

"""
def submit_answers(calculations):
    engine = create_engine('sqlite:///database.db')
    with engine.connect() as conn:
        conn.execute(text(f'INSERT INTO calculations (id, travel, house, food, lifestyle, overall) VALUES (:id, :travel, :house, :food, :lifestyle, :overall)'), calculations)
        conn.commit()"""