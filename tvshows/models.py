from django.db import models

# Create your models here.
class Show(models.Model):
    show_id=models.CharField(max_length=10)
    show_title=models.CharField(max_length=100)
    show_genre=models.CharField(max_length=100)
    show_plot=models.CharField(max_length=100)
    show_link=models.CharField(max_length=100)
    show_rating=models.CharField(max_length=100)

    def __str__(self):
        return self.show_title

class Show_Rating(models.Model):
    username = models.CharField(max_length=100)
    show_id = models.CharField(max_length=100)
    rating=models.FloatField()