from django.shortcuts import render

from app.models import MenuItem


# Create your views here.
def menu_view(request):
    return render(request, 'index.html')
