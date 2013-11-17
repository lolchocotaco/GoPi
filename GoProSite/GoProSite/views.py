from django.shortcuts import render

# Create your views here.
# For more information on this file, see
# https://docs.djangoproject.com/en//intro/tutorial03/

def home(request):
    context = {
        'active_nav': 'home',
    }
    return render(request, 'home.html', context)