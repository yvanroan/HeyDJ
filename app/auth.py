import pyrebase

firebase_config = {
    'apiKey': "AIzaSyDUrmUKQ6Ql-7K1PJtrWQPEwKt6hhz6ZOo",
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
    print("login in ...")
    ans = False

    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print('login sucessful')
        ans = True
    except:
        print('login did not work')

    return ans

def signup(email, password):
    print('signup..')
    ans = False

    try:
        sign = auth.create_user_with_email_and_password(email, password)
        print('sign up sucessful')
        ans = True
    except:
        print('sign up not sucessful')

    return ans

# if __name__ == "__main__":

#     signup('yvanrich@gmail.com','Abcd1234')




