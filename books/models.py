from django.db import models

# Create your models here.
class Book(models.Model):
    book_id=models.CharField(max_length=10)
    book_title=models.CharField(max_length=100)
    book_genre=models.CharField(max_length=100)
    book_plot=models.CharField(max_length=10000)
    book_link=models.CharField(max_length=100)
    book_rating=models.CharField(max_length=100)

    def __str__(self):
        return self.book_title

class Book_Rating(models.Model):
    username = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100)
    rating=models.FloatField()