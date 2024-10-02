import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .models import Movie
from .serializers import MovieSerializer
from io import TextIOWrapper
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import ast
from rest_framework import generics

class UploadCSV(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process CSV
        try:
            csv_file = TextIOWrapper(file.file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                try:
                    
                    release_date = row.get('release_date', None)
                    if release_date:
                        release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                    else:
                        release_date = None
                    
                    languages = row.get('languages', "[]")
                    try:
                        languages = ast.literal_eval(languages)  # Convert string representation of list to actual list
                    except ValueError:
                        languages = []
                        
                    movie_data = {
                        'budget': float(row['budget']) if row['budget'] else None,
                        'homepage': row.get('homepage'),
                        'original_language': row.get('original_language'),
                        'original_title': row.get('original_title'),
                        'overview': row.get('overview'),
                        'vote_average':row.get('vote_average'),
                        'vote_count':row.get('vote_count'),
                        'release_date': release_date,
                        'revenue': float(row['revenue']) if row['revenue'] else None,
                        'runtime': int(row['runtime']) if row['runtime'] else None,
                        'status': row.get('status'),
                        'title': row.get('title'),
                        'production_company_id':row.get('production_company_id'),
                        'genre_id':row.get('genre_id'),
                        'language': row.get('language').split('|') if row.get('language') else []  # Handling list of languages
                    }
                    serializer = MovieSerializer(data=movie_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError:
                    continue  # Skip duplicate or invalid entries
            
            return Response({"message": "CSV uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MoviePagination(PageNumberPagination):
    page_size = 10  # Limit to 10 items per page

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination  # Add pagination class

    def get_queryset(self):
        queryset = super().get_queryset()

        
        year = self.request.query_params.get('year', None)
        language = self.request.query_params.get('language', None)
        sort = self.request.query_params.get('sort', None)

        
        if year:
            try:
                year = int(year)
                queryset = queryset.filter(release_date__year=year)
            except ValueError:
                pass  

        
        if language:
            queryset = queryset.filter(original_language__icontains=language)

        
        if sort:
            if sort == 'release_date_asc':
                queryset = queryset.order_by('release_date')  
            elif sort == 'release_date_desc':
                queryset = queryset.order_by('-release_date')  
            elif sort == 'vote_average_asc':
                queryset = queryset.order_by('vote_average')  
            elif sort == 'vote_average_desc':
                queryset = queryset.order_by('-vote_average')

        return queryset