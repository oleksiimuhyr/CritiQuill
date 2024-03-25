from django.urls import path
from . import views


app_name = "review"

urlpatterns = [
    path("review/", views.index, name="index"),
]
