from django.contrib import admin
from django.urls import path,include
from movies.views import movie_home
urlpatterns = [
    path('',movie_home,name='home'),
    path('admin/', admin.site.urls),
    path('movies/',include('movies.urls')),
    path('tvshows/',include('tvshows.urls')),
    path('books/',include('books.urls')),
    path('api/',include('api.urls')),
    path('accounts/',include('accounts.urls')),
]