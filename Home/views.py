from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials, db
import os
CERT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'authentication_files/rogue-media-project-firebase-adminsdk-kv4p4-2a0cb5f100.json')
print(CERT_FILE)
cred = credentials.Certificate(CERT_FILE)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://rogue-media-project-default-rtdb.firebaseio.com/'})
ref = db.reference('/')


def home(request):

    # Total number of users for reference
    total_users = (len(ref.child("Users").get()))

    # Finding number of users with and without connected instagram accounts
    non_insta_users = (len(ref.child("Users").order_by_child("instagram").equal_to('null').get()))
    users_with_instagram = total_users - non_insta_users

    # Finding number of users with and without connected twitter accounts
    non_twitter_users = (len(ref.child("Users").order_by_child("twitter").equal_to('null').get()))
    users_with_twitter = total_users - non_twitter_users

    print(total_users, non_insta_users, users_with_instagram, non_twitter_users, users_with_twitter)

    user1 = ref.child('Users').child('1').get()
    user2 = ref.child('Users').child('2').get()
    user3 = ref.child('Users').child('3').get()
    print(user1, user2, user3)

    # List of variables to send to Render
    context = {
        "users": user[user1, user2, user3],
        "user1": user1,
        "user2": user2,
        "user3": user3,
        "total_users": total_users, 
        "non_insta_users": non_insta_users, 
        "users_with_instagram": users_with_instagram, 
        "non_twitter_users": non_twitter_users, 
        "users_with_twitter": users_with_twitter,
    }

    return render(request, "Home.html", context)