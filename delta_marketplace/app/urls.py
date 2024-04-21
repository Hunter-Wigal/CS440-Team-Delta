from django.urls import path

from . import views

urlpatterns = [
    path('', views.store),
    path('listing', views.listing),
    path('account', views.account),
    path('inventory', views.inventory),
    path('search', views.search, name='search')
]