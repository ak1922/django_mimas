from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('registeruser/', views.register_user, name='registeruser'),
    path('accountlogin/', views.account_login, name='accountlogin'),
    path('accountlogout/<int:usr_id>/logout/', views.account_logout, name='accountlogout'),
]
