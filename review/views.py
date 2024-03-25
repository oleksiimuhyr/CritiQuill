from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Movie, Review, Genre, Reviewer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_movies = Movie.objects.count()
    num_genres = Genre.objects.count()
    num_reviews = Review.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_movies": num_movies,
        "num_genres": num_genres,
        "num_reviews": num_reviews,
        "num_visits": num_visits + 1,
    }

    return render(request, "review/index.html", context=context)


class GenreListView(generic.ListView):
    model = Genre
    template_name = "review/genres_list.html"
    context_object_name = "genres_list"
    paginate_by = 5


class MovieListView(generic.ListView):
    model = Movie
    template_name = "review/movies_list.html"
    context_object_name = "movies_list"
    paginate_by = 5


class ReviewListView(generic.ListView):
    model = Review
    template_name = "review/reviews_list.html"
    context_object_name = "reviews_list"
    paginate_by = 5


class ReviewerListView(generic.ListView):
    model = Reviewer
    template_name = "review/reviewers_list.html"
    context_object_name = "reviewer_list"
    paginate_by = 5
