from django.urls import path
from . import views
from .views import (
    MovieListView,
    ReviewListView,
    ReviewDetailView,
    MovieCreateView,
    GenreCreateView,
    ReviewerListView,
    ReviewerDetailView,
    MovieDetailView,
    CreateReviewView,
    AllGenresView,
    GenreMoviesView, ReviewDeleteView,
)

app_name = 'review'

urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', AllGenresView.as_view(),
         name='all_genres'),
    path('genres/<int:pk>/',
         GenreMoviesView.as_view(), name='all-genre-movies'),
    path('genres/create/', GenreCreateView.as_view(), name='genre-create'),
    path('movies/', MovieListView.as_view(), name='movies-list'),
    path('movies/<int:movie_id>/',
         MovieDetailView.as_view(), name='movie-detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie-create'),
    path('reviews/',
         ReviewListView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/',
         ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/create/',
         CreateReviewView.as_view(), name='create-review'),
    path('write_review/<int:movie_id>/',
         views.CreateReviewView.as_view(), name='write_review'),
    path('reviews/<int:pk>/delete/',
         ReviewDeleteView.as_view(), name='review-delete'),
    path('reviewers/',
         ReviewerListView.as_view(), name='reviewers-list'),
    path('reviewers/<int:pk>/',
         ReviewerDetailView.as_view(), name='reviewer-detail'),
]
