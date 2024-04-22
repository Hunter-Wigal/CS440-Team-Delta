from django.urls import path

from . import views

urlpatterns = [
    path('get_user', views.get_user),
    path('get_ownedGames', views.get_owned_games),
    path('get_ownedCollectibles', views.get_owned_coll)
]