from django.urls import path

from . import views

urlpatterns = [
    path('get_all', views.get_all),
    path('get_games', views.get_games),
    path('get_user_games', views.get_user_games),
    path('game', views.single_game),
    path('collectibles', views.collectibles),
    path('collectibles_owned', views.collectibles_owned),
    path('get_publishers_games', views.get_publishers_games),
    path('purchase', views.purchase)
]