from django.urls import path 
from .views import index, user_settings
from . import views 



app_name = "home"

urlpatterns = [
    path("", index, name="index"),
    path("login/", views.loginpage, name="login"),
    path("register/", views.registerpage, name="register"),
    path("logout/", views.logoutpage, name="logout"),
    path("settings/", user_settings, name="settings"),
    path('delete-confirm/', views.delete_account_confirm, name='delete_confirm'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('change-email/', views.change_email, name='change_email'),
    path('email-changed/', views.email_change_done, name='email_change_done'),
]

