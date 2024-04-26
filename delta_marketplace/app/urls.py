from django.urls import path

from . import views

urlpatterns = [
    path('', views.store),
    path('listing', views.listing),
    path('account', views.account),
    path('inventory', views.inventory),
    path('games', views.games),
    path('search', views.search, name='search'),
    path('game/<str:pk>/', views.single_game_view, name="game"),
    path('publisher/<str:pk>/', views.publisher_dashboard, name="publisher_dashboard"),
    path('add_game/', views.add_game_view, name="add_game_view")
]

handler404 = views.custom_404_view