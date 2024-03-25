from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from review.models import Review, Genre, Movie, Reviewer


@admin.register(Reviewer)
class ReviewerAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("reviewed_by",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("reviewed_by",)}),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "rating", )
    list_filter = ("rating", )
    search_fields = ["movie__title"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["title"]


admin.site.register(Genre)
admin.site.unregister(Group)
