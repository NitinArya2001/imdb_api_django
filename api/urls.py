from django.urls import path
from .views import UploadCSV, MovieListView

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload_csv'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
]
