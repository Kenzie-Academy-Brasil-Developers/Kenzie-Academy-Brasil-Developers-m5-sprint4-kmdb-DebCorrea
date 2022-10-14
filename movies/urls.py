from rest_framework.urls import path

from . import views

urlpatterns = [
    path("movies/", views.MovieViews.as_view()),
]
