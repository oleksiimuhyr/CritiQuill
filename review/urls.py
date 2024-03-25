from django.urls import path
from . import views
from .views import GenreListView, MovieListView, ReviewListView, ReviewerListView

app_name = "review"

urlpatterns = [
    path("review/", views.index, name="index"),
    path("genres/", GenreListView.as_view(), name="genres-list"),
    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("reviews/", ReviewListView.as_view(), name="reviews-list"),
    path("reviewers/", ReviewerListView.as_view(), name="reviewers-list"),
]
