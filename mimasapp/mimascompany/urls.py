from django.urls import path

from .views.company import index, staff_room


app_name = 'mimascompany'

urlpatterns = [
    path('', index, name='index'),
    path('staffroom/', staff_room, name='staffroom'),
]
