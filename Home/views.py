from django.shortcuts import render
import datetime
from dbfire.users import get_all_users, get_social_users, get_filtered_users
# from datetime import timedelta


def home(request):
    """
    Dashboard View. Consists summary statics of App
    """
    # Old Logic Commented
    # # Total number of users for reference
    # total_users = (len(ref.child("Users").get()))
    #
    # # Finding number of users with and without connected instagram accounts
    # non_insta_users = (len(ref.child("Users").order_by_child("instagram").equal_to('null').get()))
    # users_with_instagram = total_users - non_insta_users
    #
    # # Finding number of users with and without connected twitter accounts
    # non_twitter_users = (len(ref.child("Users").order_by_child("twitter").equal_to('null').get()))
    # users_with_twitter = total_users - non_twitter_users
    #
    # # Finding top 10 users by followers
    # users_by_followers = ref.child("Users").order_by_child("num_followers").limit_to_last(10).get()
    #
    # # Formula for creating date certain amounts of months since today
    # date_format = '%Y-%m-%d'
    # current_date = datetime.date.today()
    # current_date_obj = current_date.strftime(date_format)
    # n = 12 # Include number of months back to start at here
    # past_date = current_date - timedelta(days=30*n)
    # past_date_str = past_date.strftime(date_format)
    # num_users_since = (len(ref.child("Users").order_by_child("time_created").start_at(past_date_str).get()))
    #
    # user1 = ref.child('Users').child('1').get()
    # user2 = ref.child('Users').child('2').get()
    # user3 = ref.child('Users').child('3').get()
    # userlist = [user1, user2, user3]
    #
    # # List of variables to send to Render
    # context = {
    #     "users": userlist,
    #     "user1": user1,
    #     "user2": user2,
    #     "user3": user3,
    #     "total_users": total_users,
    #     "non_insta_users": non_insta_users,
    #     "users_with_instagram": users_with_instagram,
    #     "non_twitter_users": non_twitter_users,
    #     "users_with_twitter": users_with_twitter,
    #     "num_users_since": num_users_since,
    #     "users_by_followers": users_by_followers,
    # }

    # New Logic
    # Getting All Users
    total_users, all_users = get_all_users()

    # Num of Users with Instagram Account
    users_with_insta = len(get_social_users(('instagram',)))

    # Num of Users without Instagram Account
    non_insta_users = total_users - users_with_insta

    # Num of Users with Twitter Account
    users_with_twitter = len(get_social_users(('twitter',)))

    # Num of Users without Twitter Account
    non_twitter_users = total_users - users_with_twitter

    # Users with insta or twitter accounts
    users_with_twitter_or_insta = len(get_social_users(('instagram', 'twitter')))

    # Users with insta only accounts, no twitter
    users_with_insta_only = len(get_social_users(('instagram',), True))

    # Users with twitter only accounts, no insta
    users_with_twitter_only = len(get_social_users(('twitter',), True))

    # Top 10 Users with highest number of followers
    users_by_followers = get_filtered_users({}, 10, 'desc', 'num_followers')

    # Num of Users joined since a specified date
    time_since = datetime.datetime(2020, 5, 1, 0, 0, 0, 0,
                                   tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    time_since = time_since[:-2] + ":" + time_since[-2:]
    num_users_since = len(get_filtered_users({'time_created': (time_since, 'gte')}))

    # List of variables to send to Render
    context = {
        "total_users": total_users,
        "non_insta_users": non_insta_users,
        "users_with_insta": users_with_insta,
        "non_twitter_users": non_twitter_users,
        "users_with_twitter": users_with_twitter,
        "num_users_since": num_users_since,
        # "users_by_followers": users_by_followers,
        # "twitter_insta_users": users_with_twitter_or_insta,
        # "users_insta_only": users_with_insta_only,
        # "users_twitter_only": users_with_twitter_only
    }
    return render(request, "Home.html", context=context)


def user_admin(request):
    """
    User Admin View. User statistics, user search etc.
    """
    return render(request, 'users_admin.html', context={})
