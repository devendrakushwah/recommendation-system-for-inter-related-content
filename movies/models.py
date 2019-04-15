from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id=models.CharField(max_length=10)
    movie_title=models.CharField(max_length=100)
    movie_genre=models.CharField(max_length=100)
    movie_plot=models.CharField(max_length=10000)
    movie_link=models.CharField(max_length=100)
    imdb_rating=models.CharField(max_length=100)

    def __str__(self):
        return self.movie_title

class Movie_Rating(models.Model):
    username = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=100)
    rating=models.FloatField()