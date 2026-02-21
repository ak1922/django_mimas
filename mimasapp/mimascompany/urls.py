from django.urls import path

from .views.company import index


app_name = 'mimascompany'

urlpatterns = [
    path('', index, name='index'),
]
