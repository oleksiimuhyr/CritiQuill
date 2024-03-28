from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import (MovieCreateForm, GenreForm, ReviewForm,
                    MovieSearchForm, GenreSearchForm)
from .models import Movie, Review, Genre, Reviewer


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
    form = GenreSearchForm(request.GET)
    genres_list = Genre.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            genres_list = genres_list.filter(name__icontains=query)

    paginator = Paginator(genres_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request,
                  'review/all_genres.html',
                  {'genres': page_obj, 'paginator': paginator, 'page_obj': page_obj, 'is_paginated': is_paginated,
                   'form': form})


def all_genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'review/movies_by_genre.html', {'genre': genre, 'movies': movies})


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy("review:all_genres")


class MovieDetailView(generic.DetailView):
    model = Movie


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    form_class = MovieCreateForm
    success_url = reverse_lazy("review:movies-list")

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.save()
        genres = form.cleaned_data.get('genres')
        movie.genre.add(*genres)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            kwargs['initial'] = {'genres': [genre_id]}  # Preselect genre
        return kwargs


class MovieListView(generic.ListView):
    model = Movie
    queryset = Movie.objects.prefetch_related("genre")
    template_name = "review/movies_list.html"
    context_object_name = "movies_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = MovieSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Movie.objects.prefetch_related("genre")
        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return queryset


class ReviewListView(generic.ListView):
    model = Review
    template_name = "review/reviews_list.html"
    context_object_name = "reviews_list"
    paginate_by = 5


class ReviewDetailView(generic.DetailView):
    model = Review


@login_required
def create_review(request, movie_id=None):
    if movie_id:
        movie = get_object_or_404(Movie, pk=movie_id)
        initial_data = {'movie': movie}
    else:
        initial_data = None

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review:reviews-list')
    else:
        form = ReviewForm(initial=initial_data)
    return render(request, 'review/review_form.html', {'form': form})


class ReviewerListView(generic.ListView):
    model = Reviewer
    template_name = "review/reviewers_list.html"
    context_object_name = "reviewer_list"
    paginate_by = 5
