from django.shortcuts import render


# Main index page
def index(request):
    return render(request, 'index.html')


# Staff room
def staff_room(request):
    return render(request, 'mimascompany/staffroom.html')
