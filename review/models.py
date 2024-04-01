from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self: models) -> str:
        return self.name


class Reviewer(AbstractUser):
    favourite_movies = models.ManyToManyField(
        'Movie', related_name='favourite_movies')

    def __str__(self: models) -> str:
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    release_year = models.IntegerField()
    reviewers = models.ManyToManyField(
        Reviewer, through='Review', related_name='reviewed_movies'
    )

    class Meta:
        ordering = (
            'title',
            'release_year',
        )

    def __str__(self: models) -> str:
        return self.title

    def get_absolute_url(self: models) -> HttpResponse:
        return reverse('review:movie-detail', args=[str(self.id)])


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='review_author')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='movie_reviews')
    RATING_CHOICES = [
        (0, '0 - Terrible'),
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating']

    def __str__(self: models) -> str:
        return f'{self.user} - {self.movie.title}'
