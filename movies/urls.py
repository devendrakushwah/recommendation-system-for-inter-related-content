from django.urls import path
from movies.views import *

app_name='movies'

urlpatterns = [
    path('',movie_home,name='home'),
    path('detail',movie_detail,name='detail'),
    path('rate',rate_movie,name='rate'),
]