from django.urls import path

from . import views

urlpatterns = [
    path('publisher', views.publisher),
    path('add_game', views.add_game, name='add_game'),
    path('remove_game', views.remove_game, name="remove_game")
]