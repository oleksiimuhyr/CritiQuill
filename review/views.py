from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
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


def all_genres(request):
    genres = Genre.objects.all()
    return render(request, 'review/all_genres.html', {'genres': genres})


def all_genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'review/movies_by_genre.html', {'genre': genre, 'movies': movies})


class MovieDetailView(generic.DetailView):
    model = Movie


class MovieListView(generic.ListView):
    model = Movie
    queryset = Movie.objects.prefetch_related("genre")
    template_name = "review/movies_list.html"
    context_object_name = "movies_list"
    paginate_by = 5


class ReviewListView(generic.ListView):
    model = Review
    template_name = "review/reviews_list.html"
    context_object_name = "reviews_list"
    paginate_by = 5


class ReviewDetailView(generic.DetailView):
    model = Review


# class ReviewerListView(generic.ListView):
#     model = Reviewer
#     template_name = "review/reviewers_list.html"
#     context_object_name = "reviewer_list"
#     paginate_by = 5
