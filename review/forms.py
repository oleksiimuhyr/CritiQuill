from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from review.models import Movie, Genre, Review, Reviewer


class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'release_year']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'review_text']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['movie'].queryset = Movie.objects.all()
