from django.urls import path
from . import views
from .views import (MovieListView,
                    ReviewListView,
                    MovieDetailView,
                    ReviewDetailView)

app_name = "review"

urlpatterns = [
    path("review/", views.index, name="index"),
    path('genres/', views.all_genres, name='all_genres'),
    path('genre/<int:genre_id>/', views.all_genre_movies, name="all-genre-movies"),
    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("reviews/", ReviewListView.as_view(), name="reviews-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail")
    # path("reviewers/", ReviewerListView.as_view(), name="reviewers-list"),

]
