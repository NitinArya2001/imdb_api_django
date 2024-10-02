from django.db import models
import json

class Movie(models.Model):
    budget = models.FloatField(null=True, blank=True)  # Float field for budget
    homepage = models.TextField(null=True, blank=True) # URL field for homepage
    original_language = models.CharField(max_length=50,null=True, blank=True)  # Language field
    original_title = models.CharField(max_length=255)  # Original title
    overview = models.TextField(null=True, blank=True)  # Overview can be text
    release_date = models.DateField(null=True, blank=True)  # Date field for release date
    revenue = models.FloatField(null=True, blank=True)  # Float field for revenue
    runtime = models.IntegerField(null=True, blank=True)  # Integer field for runtime
    status = models.CharField(max_length=50,null=True, blank=True)  # Status of the movie
    title = models.CharField(max_length=255)  # Title of the movie
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.FloatField(null=True, blank=True)
    production_company_id =  models.IntegerField(null=True, blank=True)
    genre_id = models.IntegerField(null=True, blank=True)
    languages = models.JSONField(default=list)

    def __str__(self):
        return self.title
    
    def set_language(self, lang_list):
        self.language = json.dumps(lang_list)

    def get_language(self):
        return json.loads(self.language)
