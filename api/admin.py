from django.contrib import admin
from api.models import Movie
# Register your models here.

@admin.register(Movie)
class ProspectAdmin(admin.ModelAdmin):
    search_fields = ("title",)