from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import DetailView, ListView

from .forms import (
    MovieCreateForm,
    GenreForm,
    ReviewForm,
    MovieSearchForm,
    GenreSearchForm,
    ReviewSearchForm,
)
from .models import Movie, Review, Genre, Reviewer


def index(request: HttpRequest) -> HttpResponse:

    num_movies = Movie.objects.count()
    num_genres = Genre.objects.count()
    num_reviews = Review.objects.count()
    num_reviewers = Reviewer.objects.count()

    context = {
        'num_movies': num_movies,
        'num_genres': num_genres,
        'num_reviews': num_reviews,
        'num_reviewers': num_reviewers,
    }

    return render(request, 'review/index.html', context=context)


class AllGenresView(ListView):
    model = Genre
    template_name = 'review/all_genres.html'
    context_object_name = 'genres'
    paginate_by = 5

    def get_queryset(self: View) -> QuerySet:
        queryset = super().get_queryset()
        form = GenreSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self: View,
                         **kwargs: None) -> [str, GenreSearchForm]:
        context = super().get_context_data(**kwargs)
        context['form'] = GenreSearchForm(self.request.GET)
        return context


class GenreMoviesView(DetailView):
    model = Genre
    template_name = 'review/movies_by_genre.html'
    context_object_name = 'genre'

    def get_context_data(self: View, **kwargs: None) -> [str]:
        context = super().get_context_data(**kwargs)
        genre = self.get_object()
        context['movies'] = Movie.objects.filter(genre=genre)
        return context


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy('review:all_genres')


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    form_class = MovieCreateForm
    success_url = reverse_lazy('review:movies-list')

    def form_valid(self: model, form: MovieCreateForm) -> HttpResponse:
        movie = form.save(commit=False)
        movie.save()
        genres = form.cleaned_data.get('genres')
        movie.genre.add(*genres)
        return super().form_valid(form)

    def get_form_kwargs(self: None) -> dict:
        kwargs = super().get_form_kwargs()
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            kwargs['initial'] = {'genres': [genre_id]}  # Preselect genre
        return kwargs


class MovieListView(generic.ListView):
    model = Movie
    queryset = Movie.objects.prefetch_related('genre')
    template_name = 'review/movies_list.html'
    context_object_name = 'movies_list'
    paginate_by = 5

    def get_context_data(self: None,
                         *, object_list: None = None,
                         **kwargs: None) -> dict:
        context = super(MovieListView, self).get_context_data(**kwargs)
        title = self.request.GET.get('title', '')
        context['search_form'] = MovieSearchForm(initial={'title': title})
        return context

    def get_queryset(self: None) -> QuerySet:
        queryset = Movie.objects.prefetch_related('genre')
        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data['title'])
        return queryset


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review/reviews_list.html'
    context_object_name = 'reviews_list'
    paginate_by = 5

    def get_queryset(self: None) -> QuerySet:
        queryset = super().get_queryset()
        title = self.request.GET.get('query')
        if title:
            queryset = queryset.filter(movie__title__icontains=title)
        return queryset

    def get_context_data(self: None, **kwargs: None) -> None:
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewSearchForm(self.request.GET)
        return context


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review


class CreateReviewView(LoginRequiredMixin, View):
    def get_initial_data(self: View, movie_id: int) -> None | dict:
        if movie_id:
            movie = get_object_or_404(Movie, pk=movie_id)
            return {'movie': movie}
        return None

    def get(self: View,
            request: HttpRequest, movie_id: int = None) -> HttpResponse:
        initial_data = self.get_initial_data(movie_id)
        form = ReviewForm(initial=initial_data)
        return render(request, 'review/review_form.html', {'form': form})

    def post(self: View,
             request: HttpRequest, movie_id: int = None) -> HttpResponse:
        initial_data = self.get_initial_data(movie_id)
        form = ReviewForm(request.POST, initial=initial_data)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review:reviews-list')
        return render(request, 'review/review_form.html', {'form': form})


class ReviewerListView(LoginRequiredMixin, ListView):
    model = Reviewer
    template_name = 'review/reviewers_list.html'
    context_object_name = 'reviewer_list'
    paginate_by = 5


class ReviewerDetailView(LoginRequiredMixin, DetailView):
    model = Reviewer
    template_name = 'review/reviewers_detail.html'
    context_object_name = 'reviewer'


class MovieDetailView(LoginRequiredMixin, DetailView):
    def get(self: View,
            request: HttpRequest, movie_id: int = None) -> HttpResponse:
        movie = get_object_or_404(Movie, pk=movie_id)
        user = request.user
        is_favorite = movie in user.favourite_movies.all()
        context = {
            'movie': movie,
            'is_favorite': is_favorite,
        }
        return render(request, 'review/movie_detail.html', context)

    def post(self: View,
             request: HttpRequest, movie_id: int = None) -> HttpResponse:
        movie = get_object_or_404(Movie, pk=movie_id)
        user = request.user

        if 'add_to_favorites' in request.POST:
            user.favourite_movies.add(movie)
        elif 'remove_from_favorites' in request.POST:
            user.favourite_movies.remove(movie)
        return redirect('review:movie-detail', movie_id=movie_id)
