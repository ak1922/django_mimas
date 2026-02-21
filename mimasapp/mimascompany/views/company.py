from django.shortcuts import render


# Main index page
def index(request):
    return render(request, 'index.html')
