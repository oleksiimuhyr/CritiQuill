from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from review.models import Movie, Genre, Review


class MovieCreateForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'release_year']

    def clean_release_year(self: forms.ModelForm) -> forms.ModelForm:
        release_year = self.cleaned_data.get('release_year')
        current_year = timezone.now().year
        if release_year < 1888 or release_year > current_year:
            raise forms.ValidationError(
                'Release year must be between 1888 and the current year.'
            )
        return release_year


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

    def clean_name(self: forms.ModelForm) -> forms.ModelForm:
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError(
                'Genre name should only contain alphabetic characters.'
            )
        return name


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'review_text']

    def __init__(self: forms, *args: None, **kwargs: None) -> None:
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['movie'].queryset = Movie.objects.all()


class MovieSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'search by title'}),
    )


class GenreSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'search by genre'}),
    )


class ReviewSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'search by movie'}),
    )
