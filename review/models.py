from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    genre = models.ManyToManyField("Genre")
    release_year = models.IntegerField()

    def __str__(self):
        return self.title


class Reviewer(AbstractUser):
    review_history = models.ManyToManyField(Movie, related_name="reviewed_by")

    def __str__(self):
        return self.username


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    RATING_CHOICES = [
        (0, "0 - Terrible"),
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie.title}"
