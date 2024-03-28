from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from review.models import Movie, Genre, Review, Reviewer


class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'release_year']

    def clean_release_year(self):
        release_year = self.cleaned_data.get('release_year')
        current_year = timezone.now().year
        if release_year < 1888 or release_year > current_year:
            raise ValidationError("Release year must be between 1888 and the current year.")
        return release_year


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
