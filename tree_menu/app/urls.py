from django.urls import path
from app.views import menu_view

urlpatterns = [
    path('menu', menu_view, name='menu')
]