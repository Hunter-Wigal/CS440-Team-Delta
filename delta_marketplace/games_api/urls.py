from django.urls import path

from . import views

urlpatterns = [
    path('get_all', views.get_all),
    path('get_games', views.get_games)
]