from django.urls import path

from . import views

urlpatterns = [
    path('', views.store),
    path('listing', views.listing),
    path('user', views.user)
]