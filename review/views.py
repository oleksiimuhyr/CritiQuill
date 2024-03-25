from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Movie, Review, Reviewer, Genre


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
