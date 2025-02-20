import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

api = os.environ.get('fire_apiKey')

firebase_config = {
    'apiKey': api,
    'authDomain': "auth-dj.firebaseapp.com",
    'projectId': "auth-dj",
    'storageBucket': "auth-dj.appspot.com",
    'databaseURL':"",
    'messagingSenderId': "982248478421",
    'appId': "1:982248478421:web:603a24ce765d8550c3745c",
    'measurementId': "G-6JP5RB16P2"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login(email, password):
    print("logging in...")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print('Login successful')
        return True
    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            print('Error: Invalid password')
        elif "EMAIL_NOT_FOUND" in error_message:
            print('Error: Email not found')
        elif "INVALID_EMAIL" in error_message:
            print('Error: Invalid email format')
        else:
            print(f'Login error: {error_message}')
        return False

def signup(email, password):
    print('Signing up...')
    try:
        sign = auth.create_user_with_email_and_password(email, password)
        print('Signup successful')
        return True
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            print('Error: Email already exists')
        elif "WEAK_PASSWORD" in error_message:
            print('Error: Password should be at least 6 characters')
        elif "INVALID_EMAIL" in error_message:
            print('Error: Invalid email format')
        else:
            print(f'Signup error: {error_message}')
        return False
