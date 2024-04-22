from django.urls import path

from . import views

urlpatterns = [
    path('', views.store),
    path('listing', views.listing),
    path('account', views.account),
    path('search', views.search, name='search')
]

handler404 = views.custom_404_view