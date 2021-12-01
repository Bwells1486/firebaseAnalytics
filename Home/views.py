from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials, db
import os
import datetime
from datetime import timedelta
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

    # Finding top 10 users by followers
    users_by_followers = ref.child("Users").order_by_child("num_followers").limit_to_last(10).get()
    
    # Formula for creating date certain amounts of months since today
    date_format = '%Y-%m-%d'
    current_date = datetime.date.today()
    current_date_obj = current_date.strftime(date_format)
    n = 12 # Include number of months back to start at here
    past_date = current_date - timedelta(days=30*n)
    past_date_str = past_date.strftime(date_format)
    num_users_since = (len(ref.child("Users").order_by_child("time_created").start_at(past_date_str).get()))

    user1 = ref.child('Users').child('1').get()
    user2 = ref.child('Users').child('2').get()
    user3 = ref.child('Users').child('3').get()
    userlist = [user1, user2, user3]

    # List of variables to send to Render
    context = {
        "users": userlist,
        "user1": user1,
        "user2": user2,
        "user3": user3,
        "total_users": total_users, 
        "non_insta_users": non_insta_users, 
        "users_with_instagram": users_with_instagram, 
        "non_twitter_users": non_twitter_users, 
        "users_with_twitter": users_with_twitter,
        "num_users_since": num_users_since,
        "users_by_followers": users_by_followers,
    }

    return render(request, "Home.html", context)
