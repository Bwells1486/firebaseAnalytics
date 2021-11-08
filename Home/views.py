from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials, db
import os
CERT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'authentication_files\\rogue-media-project-firebase-adminsdk-kv4p4-6c60a69824.json')
print(CERT_FILE)
cred = credentials.Certificate(CERT_FILE)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://rogue-media-project-default-rtdb.firebaseio.com/'})
ref = db.reference('/')


def home(request):
    user1 = ref.child('Users').child('1').get()
    user2 = ref.child('Users').child('2').get()
    user3 = ref.child('Users').child('3').get()
    print(user1, user2, user3)
    return render(request, "Home.html", {"user1": user1, "user2": user2, "user3": user3})