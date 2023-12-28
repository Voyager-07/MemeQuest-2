from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.meme_search , name="meme_search")
]

#username voyager password admin123