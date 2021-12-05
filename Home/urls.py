from django.urls import path
from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_admin/', views.user_admin, name='user_admin')
]