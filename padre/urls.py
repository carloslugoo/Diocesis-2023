from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='director_home'),
]