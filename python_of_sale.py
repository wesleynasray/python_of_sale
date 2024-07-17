import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def main():
    initialize_firebase()

    test = db.reference("/test").get()
    print(test)
    
    return

def initialize_firebase():
    cred = credentials.Certificate("./python-of-sale-firebase-adminsdk-pgjxf-92ea74ad68.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://python-of-sale-default-rtdb.firebaseio.com/"
    })

if __name__ == "__main__":
    main()