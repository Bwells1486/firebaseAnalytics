from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import datetime
from dbfire.users import get_all_users, get_social_users, get_filtered_users
from datetime import timedelta



def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('signin')


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('signin')


def home(request):
    """
    Dashboard View. Consists summary statics of App
    """

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

    # Users without any Social Account
    non_social_users = len(get_social_users(tuple()))

    # Users in past 6 months
    month_start = datetime.datetime.today().replace(day=1).strftime("%Y-%m-%d").split('-')
    month_start = datetime.datetime(*list(map(int, month_start)),
                      tzinfo=datetime.timezone.utc)
    months_ago = {}
    for i in range(7):
        month_ago_date = (month_start - timedelta(days=430+30*(6-i)))
        month_ago_month = month_ago_date.strftime('%B-%y')
        month_ago_date = month_ago_date.strftime("%Y-%m-%dT%H:%M:%S%z")
        month_ago_date = month_ago_date[:-2] + ":" + month_ago_date[-2:]
        months_ago[month_ago_month] = len(get_filtered_users({'time_created': (month_ago_date, 'lte')}))

    # Top 10 Users with highest number of followers
    users_by_followers = get_filtered_users({}, 10, 'desc', 'num_followers')

    # Users joined through referrals
    referred_users = len(get_filtered_users({'invited_by_user_profile': ('null', 'eq')}))
    direct_users = total_users - referred_users

    # Num of Users joined since a specified date
    time_since = datetime.datetime(2020, 5, 1, 0, 0, 0, 0,
                                   tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    time_since = time_since[:-2] + ":" + time_since[-2:]
    time_since_str = datetime.datetime(2020, 5, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc).strftime("%m-%d-%y")
    num_users_since = len(get_filtered_users({'time_created': (time_since, 'gte')}))

    # List of variables to send to Render
    context = {
        "total_users": total_users,
        "non_insta_users": non_insta_users,
        "users_with_insta": users_with_insta,
        "non_twitter_users": non_twitter_users,
        "users_with_twitter": users_with_twitter,
        "num_users_since": num_users_since,
        "time_since": time_since_str,
        "direct_users": direct_users,
        "referred_users": referred_users,
        "non_social_users": non_social_users,
        "months_ago": months_ago,
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
